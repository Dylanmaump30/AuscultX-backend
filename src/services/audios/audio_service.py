import boto3
from dotenv import load_dotenv
import os
from src.services.audios.S3Connect import s3
from src.audioprocess.Audioutils import create_directory
load_dotenv()  
BUCKET_NAME = os.getenv('S3_NAME')
SRC_FOLDER = os.path.abspath('src/files/audios')

def uploadFile(filename):
    with open(filename, "rb") as f:
        s3.upload_fileobj(f, BUCKET_NAME, filename)

def downloadFile(filename, user_id):
    try:
        s3_key = f'public/{user_id}/{filename}'
        local_dir = f'C:/Proyectos/LungTrack/Server/backend/src/files/audios/{user_id}'
        local_path = os.path.join(local_dir, filename)
        create_directory(local_dir)
        s3_client = boto3.client('s3')
        s3_object = s3_client.head_object(Bucket=BUCKET_NAME, Key=s3_key)
        s3_file_size = s3_object['ContentLength']
        with open(local_path, 'wb') as f:
            s3.download_fileobj(BUCKET_NAME, s3_key, f)

        if os.path.exists(local_path):
            local_file_size = os.path.getsize(local_path)
            if local_file_size == s3_file_size:
                print(f"✅ Archivo descargado correctamente: {local_path}")
            else:
                print(f"⚠️ Advertencia: Tamaño incorrecto. S3: {s3_file_size} bytes, Local: {local_file_size} bytes")
        else:
            print(f"❌ Error: El archivo no se guardó en {local_path}")

    except Exception as e:
        print(f"❌ Error en la descarga: {e}")
        raise e