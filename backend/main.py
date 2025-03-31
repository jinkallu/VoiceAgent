from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
import datetime
import random
from database import SessionLocal, engine, Base, User
from azure_ops import AzureOps
import os
from process_pdf import ProcessPDF
import base64
import json
from PIL import Image
import io


azureOps = AzureOps()
processPDF = ProcessPDF()

# JWT settings
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

# Enable CORS (React Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database models
Base.metadata.create_all(bind=engine)

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Assistant(BaseModel):
    res_name: str
class ProductRequest(BaseModel):
    rg_name: str  # Expected data key (resource group name)

class ProductDataRequest(BaseModel):
    product_name: str  # Expected data key (resource group name)

class ProductResourceRequest(BaseModel):
    product_name: str  # Expected data key (resource group name)
    file_name:str
    type:str

class ProductData(BaseModel):
    product_name:str
    data:list

class ProductName(BaseModel):
    product_name:str
class ProductImgDataRequest(BaseModel):
    img_url: str  # Expected data key (resource group name)

# Helper function to create a JWT token
def create_access_token(data):
    expires_delta = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    to_encode = {"sub": json.dumps(data), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def getUserData():
    try:
        blob_storage = azureOps.resourceManagement.get_blobstorage_from_resource_group(os.getenv("AZURE_ADMIN_RESOURCE_GROUP"))
        print(blob_storage)
        if(len(blob_storage)>0):
            storageName=blob_storage[0]["name"]
            azureOps.blobOps.setBlobServiceClient(storage_name=storageName)
            azureOps.blobOps.setContainerClient(os.getenv("AZURE_ADMIN_CONTAINER_NAME"))

            userData=azureOps.blobOps.getStorageMappingAsJson(os.getenv("AZURE_ADMIN_BLOB_NAME"))
            return userData
    except Exception as e:
        print("error in accessing userdata", e)

@app.post("/register/")
def register(user_data: UserRegister):
    # Log the received data
    print(f"*Received user data: {user_data}")

    # Check if the username already exists
    userData = getUserData()
    print(userData)
    user_exists = any(user["username"] == user_data.username for user in userData)

    if user_exists:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password
    hashed_password = pwd_context.hash(user_data.password)    
    user ={
        "username":user_data.username, 
        "hashed_password":hashed_password,
        "resourceGroups": []
        }
    userData.append(user)
    print(userData)
    try:
        res=azureOps.blobOps.createOrReplaceBlobFromPyDict(os.getenv("AZURE_ADMIN_BLOB_NAME"), userData)
        print(res)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not register the user")


    return {"message": "User registered successfully"}


@app.post("/login/")
def login(user_data: UserLogin,):
    print('login called',user_data)
    # user = db.query(User).filter(User.username == user_data.username).first()
    # if not user or not pwd_context.verify(user_data.password, user.hashed_password):
    #     raise HTTPException(status_code=401, detail="Invalid credentials")
    try:
            userData = getUserData()
            if(len(userData)>0):
                for item in userData:
                    if(item['username']==user_data.username and pwd_context.verify(user_data.password, item["hashed_password"])):
                        user=item
                        access_token = create_access_token({"username":user_data.username,"resourceGroups":item["resourceGroups"] or []})
                        return {"access_token": access_token, "resourceGroups":item["resourceGroups"] or []}

    except Exception as e:
        print(e)
        return None  

@app.get("/loadresourcegroups/")
def loadResourceGroups(authorization: str = Header(...)):
    payload = authorised(authorization)
    username = payload.get("sub")
   
    try:
        blob_storage = azureOps.resourceManagement.get_blobstorage_from_resource_group(os.getenv("AZURE_ADMIN_RESOURCE_GROUP"))
        if(len(blob_storage)>0):
            storageName=blob_storage[0]["name"]
            azureOps.blobOps.setBlobServiceClient(storage_name=storageName)
            azureOps.blobOps.setContainerClient(os.getenv("AZURE_ADMIN_CONTAINER_NAME"))

            userData=azureOps.blobOps.getStorageMappingAsJson(os.getenv("AZURE_ADMIN_BLOB_NAME"))
            user={}
            if(len(userData)>0):
                for item in userData:
                    if(item['username']==username):
                        return {"resource_groups":item.get('resourceGroups') or []}

    except Exception as e:
        print(e)
        return None    
  

    
def authorised(authorization):
    try:
        # Expecting header: "Bearer <token>"
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("payload", payload)
        return payload
    except JWTError as e:
        print(e)
        if 'exp' in str(e):
            raise HTTPException(status_code=401, detail="Token expired")
        else:
            raise HTTPException(status_code=401, detail="Invalid token")
    
@app.post("/createresourcegroup/")
def createresourcegroup( res: Assistant, authorization: str = Header(...)):
    #payload = authorised(authorization)
    #userData = payload.get("sub")
    #print("....userdata",userData)
    res_name = res.res_name
    print(res_name)
    azureOps.provision_resources(res_name)


@app.get("/products/")
def products( authorization: str = Header(...)):
    payload = authorised(authorization)
    userData = payload.get("sub")
    print("....userdata",userData)
    tokenData=json.loads(userData)

    prdContainers=[]
    
    try:
        if len(tokenData["resourceGroups"]) > 0:
            blob_storage = azureOps.resourceManagement.get_blobstorage_from_resource_group(tokenData["resourceGroups"][0]["rg-name"])
            print(blob_storage[0]["name"])
            if len(blob_storage) == 0:
                return
            
            azureOps.blobOps.setBlobServiceClient(storage_name=blob_storage[0]["name"])

            containers=azureOps.blobOps.getContainersList()
            
            for container in containers:
                nameArray=container["name"].split("-")
                if(nameArray[0]=="prd"):
                    prdContainers.append("-".join(nameArray[1:]))
                    
            print("containers",prdContainers)  

    except Exception as e:
        return {"products": [], "detail": "Error"}

    return {"products": prdContainers}

@app.post("/product_data/")
def product_data(request_data: ProductDataRequest, authorization: str = Header(...)):
    try:
        payload = authorised(authorization)
        userData = payload.get("sub")
        tokenData=json.loads(userData)
        
        blob_storage = azureOps.resourceManagement.get_blobstorage_from_resource_group(tokenData["resourceGroups"][0]["rg-name"])
        if len(blob_storage) == 0:
            return
        
        azureOps.blobOps.setBlobServiceClient(storage_name=blob_storage[0]["name"])
        container_name=f"prd-{request_data.product_name}"
        azureOps.blobOps.setContainerClient(container_name=container_name)


        product_data = azureOps.blobOps.getProductData(os.getenv("PRODUCT_DATA_FILE_NAME"))
        #print(azureOps.blobOps.createContainerIfNotExists("test"))
        

        return {"product_data":json.loads(product_data),"status":200}
    except Exception as e:
        print(e)
        return {"product_data": [],"status":400}
    
@app.post("/product_resource/")
def product_data(request_data: ProductResourceRequest, authorization: str = Header(...)):
    try:
        payload = authorised(authorization)
        userData = payload.get("sub")
        tokenData=json.loads(userData)
        
        blob_storage = azureOps.resourceManagement.get_blobstorage_from_resource_group(tokenData["resourceGroups"][0]["rg-name"])
        if len(blob_storage) == 0:
            return
        
        azureOps.blobOps.setBlobServiceClient(storage_name=blob_storage[0]["name"])
        container_name=f"prd-{request_data.product_name}"
        azureOps.blobOps.setContainerClient(container_name=container_name)
        folder_prefix=""
        if(request_data.type=="image"):
            folder_prefix="images"




        image_data = azureOps.blobOps.getProductData(f"{folder_prefix}/{request_data.file_name}")
        image=Image.open(io.BytesIO(image_data))
        #print(azureOps.blobOps.createContainerIfNotExists("test"))
        # create a thumbnail image
        # image.thumbnail((100, 100))
        imgio = io.BytesIO()
        image.save(imgio, 'JPEG') 
        imgio.seek(0)
        return StreamingResponse(content=imgio, media_type="image/jpeg")
        

        # return send_file(io.BytesIO(obj.logo.read()),download_name=request_data.file_name,mimetype='image/jpeg' )
    except Exception as e:
        print(e)
        return {"product_resource": None,"status":400}


@app.post("/upload_productdata/")
async def uploadProductdata(request_data:ProductData, authorization: str = Header(...)):
    try:
        payload = authorised(authorization)
        # Check if it's a PDFuserData = payload.get("sub")
        
        payload = authorised(authorization)
        userData = payload.get("sub")
        tokenData=json.loads(userData)
            
        blob_storage = azureOps.resourceManagement.get_blobstorage_from_resource_group(tokenData["resourceGroups"][0]["rg-name"])
        if len(blob_storage) == 0:
            return
            
        azureOps.blobOps.setBlobServiceClient(storage_name=blob_storage[0]["name"])
        container_name=f"prd-{request_data.product_name}"
        azureOps.blobOps.setContainerClient(container_name=container_name)
        

        res=azureOps.blobOps.createOrReplaceBlobFromPyDict(os.getenv("PRODUCT_DATA_FILE_NAME"), request_data.data)
        return res
    except Exception as e:
        print(e)
        return 


@app.post("/add_product/")
async def uploadProductdata(request_data:ProductName, authorization: str = Header(...)):
    try:
        payload = authorised(authorization)
        # Check if it's a PDFuserData = payload.get("sub")
        
        payload = authorised(authorization)
        userData = payload.get("sub")
        tokenData=json.loads(userData)
            
        blob_storage = azureOps.resourceManagement.get_blobstorage_from_resource_group(tokenData["resourceGroups"][0]["rg-name"])
        if len(blob_storage) == 0:
            return
            
        azureOps.blobOps.setBlobServiceClient(storage_name=blob_storage[0]["name"])
        container_name=f"prd-{request_data.product_name}"
        res=azureOps.blobOps.createContainerIfNotExists(container_name=container_name)
        return {"result":res}
    except Exception as e:
        print(e)
        return {"result":False}
        


@app.post("/upload_pdf/")
async def uploadPdf(file: UploadFile = File(...), authorization: str = Header(...)):
    try:
        payload = authorised(authorization)
        print("upload pdf called...",payload)
        # Check if it's a PDF
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are accepted."
            )

        pdf_bytes = await file.read()
        problems_data, images = processPDF.process(file_data = pdf_bytes)
        # azureOps.blobOps.setBlobServiceClient("tralpinestorage1")
        # azureOps.blobOps.setContainerClient(os.environ.get("PRODUCTS_BLOB_CONTAINER"))

        # azureOps.blobOps.createOrReplaceBlobFromPyDict("test_product.json", problems_data)

        return {"data":problems_data,"status":200}
    except Exception as e:
        print(e)
        return {"data":[],"status":400}


    # for img_dict in images:
    #     for name, img in img_dict.items():
    #         name = "images/" + name
    #         azureOps.blobOps.createOrUpdateBlob(name, img)


    # print(f"Received file: {file.filename}")

@app.post("/product_image/")
def product_image(request_data: ProductImgDataRequest, authorization: str = Header(...)):
    payload = authorised(authorization)
    azureOps.blobOps.setBlobServiceClient("tralpinestorage1")
    azureOps.blobOps.setContainerClient(os.environ.get("PRODUCTS_BLOB_CONTAINER"))
    img_url = f"images/{request_data.img_url}"
    print("***** ", img_url)
    product_image_bytes = azureOps.blobOps.getBlobData(img_url)
    #print(azureOps.blobOps.createContainerIfNotExists("test"))
    
    base64_str = None
    if product_image_bytes:
        base64_str = base64.b64encode(product_image_bytes).decode("utf-8")
    return {"image_data": base64_str}

