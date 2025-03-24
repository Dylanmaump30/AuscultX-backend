from datetime import date
from bson import ObjectId
from flask import Blueprint, Response, request
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from src.services.users.user_service import UserService
from src.database import schemas
from src.database.connection import db
from src.errors import dberrors
from bson import json_util 
import json
import os
import gzip
from src.services.audios.audio_service import downloadFile
from src.audioprocess.Mainprocess import process_audio

audio = Blueprint("audio", __name__)

SRC_FOLDER = os.path.abspath('src/files/audios')



@audio.route('/upload', methods=['POST'])
def upload_file():
    data = request.get_json()
    if not data:
        return Response(json.dumps({"error": "No JSON received"}), status=400, mimetype="application/json")
    user_id = data.get("userID")
    if not user_id:
        return Response(json.dumps({"error": "userID is missing"}), status=400, mimetype="application/json")

    if not db.users.find_one({'_id': ObjectId(user_id)}):
        return dberrors.not_found()
    audio_schema = schemas.get_audios_schema()
    try:
        validate(instance=data, schema=audio_schema)  
    except ValidationError as e:
        return Response(json.dumps({"error": f"Validation error: {e.message}"}), status=400, mimetype="application/json")
    result = db.audios.insert_one(data)
    response = json.dumps({'_id': str(result.inserted_id), 'status': 200})
    return Response(response, mimetype="application/json")

def compress_json(data):
    json_str = json.dumps(data)  
    compressed_data = gzip.compress(json_str.encode('utf-8'))  
    return compressed_data


@audio.route('/results/<audio_id>', methods=['GET'])
def get_results(audio_id):
    try:
        data = db.audios.find_one({'_id': ObjectId(audio_id)})
        if not data:
            return Response(json_util.dumps({"error": "Audio no encontrado"}), status=404, mimetype="application/json")
        
        audio_filename = data.get('audio_filename')
        user_ID = data.get('userID')

        if not audio_filename:
            return Response(json_util.dumps({"error": "Archivo de audio no encontrado"}), status=404, mimetype="application/json")

        downloadFile(audio_filename, user_ID)  
        audio_path = os.path.join(SRC_FOLDER, user_ID, audio_filename)

        results = process_audio(audio_path)
        if results is None:
            return Response(json_util.dumps({"error": "No se pudo procesar el audio"}), mimetype="application/json")

        compressed_results = compress_json(results)

        response = Response(compressed_results, mimetype="application/gzip")
        response.headers["Content-Encoding"] = "gzip"
        response.headers["Content-Disposition"] = f"attachment; filename=results_{audio_id}.json.gz"
        
        return response

    except Exception as e:
        return Response(json_util.dumps({"error": f"Error interno: {str(e)}"}), status=500, mimetype="application/json")


@audio.route('/<user_id>', methods=['GET'])
def get_user_audios(user_id):
    data = db.audios.find({'userID': user_id})
    audios = []
    
    for audio in data:
        audio['_id'] = str(audio['_id'])  
        audios.append(audio)

    if audios:
        return Response(json_util.dumps(audios), mimetype="application/json")
    return dberrors.not_found()
        