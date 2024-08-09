from fastapi import APIRouter, HTTPException, status
from database.models.product import Product
from database.mongo_client import db_client
from database.schemas.product import product_schema, products_schema

router = APIRouter(prefix="/products", tags=["products"], responses={404 : {"message":"No encontrado"}})


@router.get("/", response_model=list[Product])
async def products():
    return products_schema(db_client.products.find())

#POST
@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def user(product: Product):

    #if type(search_user("email", user.email)) == User:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    
    product_dict = dict(product)
    #Eliminamos el id para que MONGO asigne uno por defecto
    del product_dict["id"]

    #Creamos el producto en base de datos y obtenemos el id que acaba de crear MONGO
    id = db_client.products.insert_one(product_dict).inserted_id

    new_product = product_schema(db_client.products.find_one({"_id": id}))

    return Product(**new_product)