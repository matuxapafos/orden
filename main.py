from flask import Flask
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from routes import views_bp, api_bp
from database import db


load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
DEBUG = os.getenv("DEBUG")
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")


app = Flask(__name__)

app.register_blueprint(views_bp)
app.register_blueprint(api_bp, url_prefix="/api")

app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
jwt = JWTManager(app)

app.config["SQLALCHEMY_DATABASE_URI"] = DB_CONNECTION_STRING
db.init_app(app)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)
