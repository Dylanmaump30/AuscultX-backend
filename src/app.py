from flask import Flask
from flask_cors import CORS
from src.routes.user import user
from src.routes.audio import audio
app = Flask(__name__)
CORS(app)
app.register_blueprint(user, url_prefix='/users')
app.register_blueprint(audio, url_prefix='/audios')

if __name__ == "__main__":  
    app.run(host="0.0.0.0", port=5000, debug=True)