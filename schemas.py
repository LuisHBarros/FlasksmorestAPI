from marshmallow import Schema, fields, pre_dump

from models.user import UserModel

# dump_only = read_only
# load_only = write_only

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    
    
class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    
    
class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    email = fields.Str()


class PlainConfirmationSchema(Schema):
    id = fields.Str(dump_only=True)
    expire_at = fields.Int(required=True, dump_only=True)
    confirmed = fields.Boolean(required=True, dump_only=True)


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)
    
    
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    
    
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)
    
    
class TagSchema(PlainStoreSchema):
    store_id = fields.Int(load_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    
    
class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)
    

class UserSchema(PlainUserSchema):
    confirmation = fields.Nested(PlainConfirmationSchema, dump_only=True)
    
    @pre_dump
    def _pre_dump(self, user:UserModel, **kwargs):
        user.confirmation = [user.most_recent_confirmation]
        return user
    
class ConfirmationSchema(PlainConfirmationSchema):
    user_id = fields.Int(required=True)
    user = fields.Nested(UserSchema, load_only=True)
    
    
