import traceback
from db import db
from time import time
from flask import make_response, render_template
from flask_smorest import Blueprint
from mailgun import MailGunException, Mailgun
from models import ConfirmationModel, UserModel
from flask.views import MethodView
from schemas import ConfirmationSchema
from libs.strings import gettext

blp = Blueprint("Confirmations", "confirmations", description="Operations on confirmation process")

confirmation_schema = ConfirmationSchema()

@blp.route("/user_confirmation/<string:confirmation_id>")
class Confirmation(MethodView):
    def get(self, confirmation_id):
        """Return confirmation HTML page"""
        confirmation = ConfirmationModel.query.get_or_404(confirmation_id)
        
        if time() > confirmation.expire_at: #Confirmation is expired
            return {"message" : gettext("confirmation_link_expired")}, 400
        
        if confirmation.confirmed: #User already confirmed
            return {"message" : gettext("confirmation_already_confirmed")}, 400
            
        confirmation.confirmed = True
        confirmation.save_db()
        
        headers = {"Content-Type": "text/html"}
        return make_response(
            render_template("confirmation_page.html", email=confirmation.user.email),
            200,
            headers
        )
        
        
@blp.route("/confirmation/user/<int:user_id>")
class ConfirmationByUser(MethodView):
    def get(self, user_id):
        '''return confirmations for a giver user. ONLY FOR TESTING'''
        user = UserModel.query.get_or_404(user_id)
        return(
            {
                "current_time": int(time()),
                "confirmation": [
                    confirmation_schema().dump(each)
                    for each in user.confirmation.order_by(ConfirmationModel.expire_at)
                ],
            },
            200,
        )
    
    
    def post(self, user_id):
        '''Resend a confirmation email to a giver user'''
        user = UserModel.query.get_or_404(user_id)
        
        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                if confirmation.confirmed:
                    return {"message": gettext("confirmation_already_confirmed")}, 400
                confirmation.force_expire()
            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.save_db()
            user.save_db()
            user.send_confirmation_email()  # re-send the confirmation email
            return ({"message": gettext("confirmation_resend_successful")
                     }, 201)
        except MailGunException as e:
            return {"message": str(e)}, 500
        except:
            traceback.print_exc()
            return {"message": gettext("confirmation_resend_fail")}, 500
