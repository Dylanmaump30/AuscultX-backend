from dotenv import load_dotenv
import os
import pymongo
load_dotenv()  # Asegúrate de que esté antes de usar las variables

USER = os.getenv("USERDB")
PASSWORD = os.getenv("PASSWORD")
CLUSTER = os.getenv("CLUSTER")
DB = os.getenv("DB")

client = pymongo.MongoClient(f'mongodb+srv://{USER}:{PASSWORD}@{CLUSTER}.k1unb.mongodb.net/?retryWrites=true&w=majority&appName={CLUSTER}')
db = client[DB]


