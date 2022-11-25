from datetime import timedelta
import secrets
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
from db import db
from flask_migrate import Migrate
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from resources.confirmation import blp as ConfirmationBlueprint
import os
from dotenv import load_dotenv


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    
    app.config["JWT_SECRET_KEY"] = os.getenv('APP_SECRET_KEY')
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
    jwt = JWTManager(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    '''
        Error handling than not more useful
    '''
    
    # @jwt.additional_claims_loader
    # def add_claims_to_jwt(identity):
    #     if identity == 1:
    #         return {"is_admin": True}
    #     return {"is_admin": False}
    
    # @jwt.expired_token_loader
    # def expired_token_callback(jwt_header, jwt_payload):
    #     return jsonify({"message": "The token has expired.",
    #                     "error" : "token expired"}), 401

    # @jwt.invalid_token_loader
    # def invalid_token_callback(error):
    #     return jsonify({"message": "Signature verification failed.",
    #                     "error" : "Invalid token" }), 401

    # @jwt.unauthorized_loader
    # def missing_token_callback(error):
    #     return jsonify({"message": "Request does not contain an access token.",
    #                     "error" : "authorization required"}), 401

    # @jwt.needs_fresh_token_loader
    # def token_not_fresh_callback(jwt_header, jwt_payload):
    #     return jsonify({"message": "The token is not fresh", 
    #                     "error":"fresh_token_required"}), 401



    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ConfirmationBlueprint)

    return app