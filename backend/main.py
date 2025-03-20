from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
import datetime
import random
from database import SessionLocal, engine, Base, User

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

# Helper function to create a JWT token
def create_access_token(username: str):
    expires_delta = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.datetime.utcnow() + expires_delta
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

@app.get("/protected/")
def protected_route(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return {"message": f"Welcome, {username}!"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
