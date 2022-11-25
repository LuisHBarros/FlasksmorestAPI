import uuid
from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from schemas import ItemSchema, ItemUpdateSchema
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from libs.strings import gettext
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import ItemModel

blp = Blueprint("Items", "items", description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    @jwt_required()
    def delete(self, item_id):
        # jwt = get_jwt()
        # if not jwt.get("is_admin"):
        #     abort(401, message="Admin privilege required")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": gettext("item_deleted")}, 200

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)
        try:    
            db.session.add(item)
            db.session.commit()
            return item
        except SQLAlchemyError:
            abort(500, message=gettext("item_error_inserting"))

@blp.route("/item")
class ItemList(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        if ItemSchema.find_by_name(item_data):
            return {"message": gettext("item_name_exists")}, 400
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message=gettext("item_error_inserting"))

        return item