import bcrypt
import jwt
from datetime import datetime, timedelta
import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.config import get_db
from database.models import User
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_jwt_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

class UserCreate(BaseModel):
    nrp: str
    nama_lengkap: str
    password: str
    pangkat_satker: str
    role: str = "anggota"

class UserLogin(BaseModel):
    nrp: str
    password: str

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.nrp == user.nrp).first()
    if db_user:
        raise HTTPException(status_code=400, detail="NRP already registered")
    
    password_bytes = user.password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    new_user = User(
        nrp=user.nrp,
        nama_lengkap=user.nama_lengkap,
        password_hash=hashed_password,
        pangkat_satker=user.pangkat_satker,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    return {"message": "User successfully registered"}

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.nrp == user.nrp).first()
    
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    password_bytes = user.password.encode('utf-8')
    hash_bytes = db_user.password_hash.encode('utf-8')
    
    if not bcrypt.checkpw(password_bytes, hash_bytes):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token_expire = datetime.utcnow() + timedelta(minutes=120)
    to_encode = {"sub": db_user.nrp, "role": db_user.role, "exp": token_expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": encoded_jwt, "token_type": "bearer", "role": db_user.role, "nrp": db_user.nrp}
