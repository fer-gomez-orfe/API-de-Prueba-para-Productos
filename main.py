from typing import Union
from routers import products, auth_users, users

from fastapi import FastAPI

app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(auth_users.router)
app. include_router(users.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}