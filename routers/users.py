from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from database.mongo_client import db_client
from database.schemas.user import users_schema, user_schema
from database.models.user import User

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "4bd5bac6c336daa16f5581802ddf34bc18a8d82fdce48ef2b3670ff67bdde9fb"

router = APIRouter(prefix="/users", tags=["users"], responses={404 : {"message":"No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl = "login")

crypt = CryptContext(schemes=["bcrypt"])

def get_password_hash(password):
    return crypt.hash(password)


#Creación de nuevo usuario
@router.post("/new_user")
async def new_user(user: User):
    
    #if type(search_user("email", user.email)) == User:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")

    if (db_client.users.find_one({"email":user.email})):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    
    user_dict = dict(user)
    del user_dict["id"]

    hashed_pass = get_password_hash(user_dict["password"])
    user_dict["password"]= hashed_pass
    
    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)
    
        
            
	
    	