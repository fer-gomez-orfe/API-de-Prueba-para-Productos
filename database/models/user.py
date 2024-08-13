from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[str]= None
    username: str
    full_name: str
    email: str
    disabled: bool
    password: str