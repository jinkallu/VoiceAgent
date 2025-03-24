from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
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
class ProductRequest(BaseModel):
    rg_name: str  # Expected data key (resource group name)

class ProductDataRequest(BaseModel):
    product_name: str  # Expected data key (resource group name)

# Helper function to create a JWT token
def create_access_token(username: str):
    expires_delta = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/register/")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # Log the received data
    print(f"Received user data: {user_data}")

    # Check if the username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password
    hashed_password = pwd_context.hash(user_data.password)
    user = User(username=user_data.username, hashed_password=hashed_password)
    db.add(user)
    db.commit()

    return {"message": "User registered successfully"}


@app.post("/login/")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not pwd_context.verify(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user_data.username)
    return {"access_token": access_token}

def authorised(authorization):
    try:
        # Expecting header: "Bearer <token>"
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        print(e)
        if 'exp' in str(e):
            raise HTTPException(status_code=401, detail="Token expired")
        else:
            raise HTTPException(status_code=401, detail="Invalid token")
    


@app.get("/protected/")
def protected_route(authorization: str = Header(...)):
    payload = authorised(authorization)
    username = payload.get("sub")
    resource_groups  = [azureOps.resourceManagement.list_resource_groups()[1]] # TODO: proper one
    return {"message": f"Welcome, {username}!", "resource_groups": resource_groups}

@app.post("/products/")
def products(request_data: ProductRequest, authorization: str = Header(...)):
    payload = authorised(authorization)
    blob_storage = azureOps.resourceManagement.get_blobstorage_from_resource_group(request_data.rg_name)
    if len(blob_storage) == 0:
        return
    
    azureOps.blobOps.setBlobServiceClient(storage_name=blob_storage[0]["name"])
    azureOps.blobOps.setContainerClient(os.environ.get("PRODUCTS_BLOB_CONTAINER"))
    products = azureOps.blobOps.getStorageMappingAsJson(os.environ.get("MAPPING_BLOB"))

    product_list = []

    for product in products:
        for key, value in product.items():
            product_list.append({"name": key, "json": value})


    return {"products": product_list}

@app.post("/product_data/")
def product_data(request_data: ProductDataRequest, authorization: str = Header(...)):
    payload = authorised(authorization)
    product_data = azureOps.blobOps.getProductAsJson(request_data.product_name)
    #print(azureOps.blobOps.createContainerIfNotExists("test"))
    

    return {"product_data": product_data}

@app.post("/upload/")
async def upload(file: UploadFile = File(...), authorization: str = Header(...)):
    payload = authorised(authorization)
    # Check if it's a PDF
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are accepted."
        )

    pdf_bytes = await file.read()
    problems_steps, images = processPDF.process(file_data = pdf_bytes)
    azureOps.blobOps.setBlobServiceClient("tralpinestorage1")
    azureOps.blobOps.setContainerClient(os.environ.get("PRODUCTS_BLOB_CONTAINER"))

    azureOps.blobOps.createOrReplaceBlobFromPyDict("test_product.json", problems_steps)

    print(f"Received file: {file.filename}")

