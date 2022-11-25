import traceback
from flask import request
from db import db
from mailgun import MailGunException, Mailgun
from models.confirmation import ConfirmationModel
from sqlalchemy.sql import text

class UserModel(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=True, nullable=False)
    email = db.Column(db.String(80))
    confirmation = db.relationship(
        "ConfirmationModel", lazy="dynamic", cascade="all, delete-orphan"
    )
    
    @classmethod
    def most_recent_confirmation(self):
        return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()
    
    
    def send_confirmation_email(self, confirmation_id):
        link = request.url_root[0:-1] + f'/user_confirmation/{confirmation_id}'
        text = f"Please, click the link to confirm your registration: {link}"
        subject = 'Registration confirmation'
        html = f'<html>Please, click the link to confirm your registration: <a href="{link}">{link}</html>'
        return Mailgun.send_email([self.email], subject, text, html)
    
    def save_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_db(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod    
    def find_by_username(self, user_data):
        return self.query.filter(UserModel.username == user_data['username']).first()
    
    
    @classmethod
    def find_by_email(self, user_data):
         return self.query.filter(UserModel.email == user_data['email']).first()
    
    @classmethod    
    def find_by_id(self, user_data):
        return self.query.filter(UserModel.id == user_data['id']).first()
    
    
# user = UserModel.query.filter(
#             UserModel.username == user_data["username"]
#         ).first()