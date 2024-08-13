from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from database.mongo_client import db_client
from database.schemas.user import users_schema, user_schema
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "4bd5bac6c336daa16f5581802ddf34bc18a8d82fdce48ef2b3670ff67bdde9fb"

router = APIRouter(prefix="/auth", tags=["authentication"], responses={404 : {"message":"No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl = "login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

users_db= users_schema(db_client.users.find())

def search_user_db(username: str):
    user_db = user_schema(db_client.users.find_one({"username": username}))
    return user_db

def search_user(username: str):
    user = user_schema(db_client.users.find_one({"username": username}))
    return User(**user) 

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                             detail="Credenciales de autenticación invalidas",
                             headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, key= SECRET, algorithms= [ALGORITHM]).get("sub")
        if username is None:
            raise exception      
    except JWTError:
        raise exception 
    return search_user(username)
    

async def current_user(user: User= Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                             detail="Usuario inactivo")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = user_schema(db_client.users.find_one({"username": form.username}))
    if not user_db:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                            detail="El usuario no es correcto")
    user = search_user_db(form.username)
    if not crypt.verify(form.password, user["password"]):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                            detail="La contraseña no es correcta")
    acces_token = {"sub": user["username"],
                   "exp": datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_DURATION)}
    return {"acces_token": jwt.encode(acces_token, SECRET, algorithm= ALGORITHM), "token_type": "bearer"}

@router.get("/me")
async def me(user: User = Depends(current_user)):
    return user
