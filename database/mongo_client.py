from pymongo import MongoClient

#Conexion a base de datos local
#db_client = MongoClient().local

#Conexion a base de datos remota
uri = "mongodb+srv://test:test2024@cluster0.kya8puk.mongodb.net/"
db_client = MongoClient(uri).test