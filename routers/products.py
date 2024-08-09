from fastapi import APIRouter
from database.models.product import Product
from database.mongo_client import db_client
from database.schemas.product import product_schema, products_schema

router = APIRouter(prefix="/products", tags=["products"], responses={404 : {"message":"No encontrado"}})


@router.get("/", response_model=list[Product])
async def products():
    return products_schema(db_client.products.find())
