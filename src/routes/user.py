from flask import Blueprint, current_app, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from src.services.users.user_service import UserService
from src.database import schemas
from src.database.connection import db
from src.errors import dberrors

user = Blueprint("user", __name__)
user_service = UserService(db)

@user.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        user_schema = schemas.get_user_schema()
        validate(instance=data, schema=user_schema)

        data["password"] = generate_password_hash(data["password"])
        cleaned_data = user_service.clean_data(data)

        if user_service.existing_user(cleaned_data):
            return dberrors.already_exists()

        user_service.create_user(cleaned_data)
        return jsonify({
            "success": True,
            "message": "User registered successfully."
        }), 200

    except ValidationError as e:
        current_app.logger.error(str(e))
        return jsonify({"message": e.schema.get("description", "Validation failed")}), 400

    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return dberrors.data_not_match()


@user.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        
        user = db.users.find_one({"email": email})
        if not user:
            return jsonify({"success": False, "message": "Email or password incorrect."}), 401
        if not check_password_hash(user["password"], password):
            return jsonify({"success": False, "message": "Email or password incorrect."}), 401

        return jsonify({
            "success": True, 
            "_id": str(user["_id"]),
            "name": user["name"],
            "username": user["username"],
            "email": user["email"],

        })
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500
