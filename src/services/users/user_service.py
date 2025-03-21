from flask import jsonify
class UserService:
    def __init__(self, db):
        self.db = db

    def clean_data(self,user_data):
        for field in ['name', 'email', 'username', 'password']:
            if field in user_data and isinstance(user_data[field], str):
                user_data[field] = user_data[field].strip()
        return user_data

    def get_user_by_email(self, email: str):
        return self.db.users.find_one({"email": email})
    
    def existing_user(self, user_data):
        query = {'$or': []}  # Lista de condiciones OR
        if 'username' in user_data and user_data['username']:  
            query['$or'].append({'username': user_data['username']})  
        if 'email' in user_data and user_data['email']:  
            query['$or'].append({'email': user_data['email']})  
        if not query['$or']: 
            return None  
        return self.db.users.find_one(query)  
        
    def create_user(self, user_data):
        result = self.db.users.insert_one(user_data)
        user_id = str(result.inserted_id) if result else None
        response = jsonify({'Create': True, 'user_id': user_id})
        response.status_code = 200
        return response

  
    
    
