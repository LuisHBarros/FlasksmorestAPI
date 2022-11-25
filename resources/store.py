import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from libs.strings import gettext
from db import db
from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(cls, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    
    def delete(cls, store_id):
        store = StoreModel.query.get_or_404(store_id)
        try:
            db.session.delete(store)
            db.session.commit()
            return {"message" : gettext("store_deleted")}, 200
        except SQLAlchemyError:
            abort(500, message=gettext("store_error_inserting"))


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(cls):
        return StoreModel.query.all()
    
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
            store = StoreModel(**store_data)
            try:
                db.session.add(store)
                db.session.commit()
            except IntegrityError:
                abort(
                    400, message=gettext("store_name_exists")
                )
            except SQLAlchemyError:
                abort(500, message=gettext("store_error_inserting"))
            return store

