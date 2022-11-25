from uuid import uuid4
from db import db
from time import time

confirmation_expiration_delta = 1800

class ConfirmationModel(db.Model):
    __tablename__ = 'confirmations'
    
    id = db.Column(db.String(50), primary_key=True)
    expire_at = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("UserModel")
    
    def __init__(self, user_id: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.id = uuid4().hex
        self.expire_at = int(time()) + confirmation_expiration_delta
        self.confirmed = False
        
    @classmethod
    def find_by_id(cls, _id: str) -> "ConfirmationModel":
        return cls.query.filter_by(id=_id).first()

    def save_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_db(self):
        db.session.delete(self)
        db.session.commit()
    
    @property    
    def expired(self):
        return int(time()) > self.expire_at
    
    
    def force_expire(self):
        if not self.expired:
            self.expire_at = int(time())
            self.save_db()