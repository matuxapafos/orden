from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from models import Base
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from routes import views_bp, api_bp

load_dotenv()


DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
DEBUG = os.getenv("DEBUG")

app = Flask(__name__)

app.register_blueprint(views_bp)
app.register_blueprint(api_bp, url_prefix="/api")

app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
jwt = JWTManager(app)


engine = create_engine(DB_CONNECTION_STRING, echo=True)

Session = sessionmaker(engine)


def create_db_and_tables() -> None:
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)
