import boto3 
from dotenv import load_dotenv
import os
import pymongo
load_dotenv()  
ACCESS_KEY_ID =os.getenv('ACCESS_KEY_ID')
ACCESS_SECRET_KEY =os.getenv('ACCESS_SECRET_KEY')
s3 = boto3.client('s3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
)
