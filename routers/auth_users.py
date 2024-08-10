from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext


ALGORITH = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "4bd5bac6c336daa16f5581802ddf34bc18a8d82fdce48ef2b3670ff67bdde9fb"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl = "login")

crypt = CryptContext(schemes=["bcrypt"])

