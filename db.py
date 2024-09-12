from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import g

db = None
uri = 'mongodb+srv://crescenzogarofalo:Qwertyui123!"£@cluster0.wumd0.mongodb.net/?retryWrites=true&w=majority&appName=cluster0'
def get_db():
    if 'db' not in g:
        #client = MongoClient('mongodb://localhost:27017/')
        client = MongoClient(uri, server_api=ServerApi('1'))
        g.db = client['blog']
    return g.db

