
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://NetworkSecurity:Sulphur16@cluster0.gutrft7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)


try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)