def get_user_schema():
    return {
        "bsonType": "object",
        "required": ["name", "username", "email", "password"],
        "properties": {
            "name": {
                "bsonType": "string",
                "pattern": "^[A-Za-zÁÉÍÓÚáéíóúÑñ\\s]+$",
                "description": "The name can only contain letters and spaces"
            },
            "username": {
                "bsonType": "string",
                "minLength": 3,
                "pattern": "^[a-zA-Z0-9_]+$",
                "description": "The username can only contain letters, numbers, and underscores"
            },
            "email": {
                "bsonType": "string",
                "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                "description": "Must be a valid email address"
            },
            "password": {
                "bsonType": "string",
                "minLength": 6,
                "description": "The password must be at least 6 characters long"
            }
        }
    }
def get_audios_schema():
    return {
        "type": "object",  
        "required": ["userID", "audio_filename", "s3_key"],  
        "properties": {
            "s3_key": {"type": "string"},  
            "audio_filename": {"type": "string"},
            "userID": {"type": "string"}
        }
    }

