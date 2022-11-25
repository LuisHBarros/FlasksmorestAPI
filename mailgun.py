from flask import request
from requests import post
import os
from dotenv import load_dotenv
from libs.strings import gettext
class MailGunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Mailgun:
    load_dotenv()
    mailgun_domain = os.getenv("MAILGUN_DOMAIN")
    api_key = os.getenv("MAILGUN_API_KEY")
    from_title = "Stores REST API"
    from_email = "postmaster@sandboxfbad23c9836f4217814ef1f4f1758f4f.mailgun.org"

    @classmethod
    def send_email(cls, email, subject, text, html):
        if not cls.api_key:
            raise MailGunException("Failed to load Mailgun API key")
        if not cls.mailgun_domain:
            raise MailGunException("Failed to load Mailgun Domain key")
        response = post(
            f"https://api.mailgun.net/v3/{cls.mailgun_domain}/messages",
            auth=("api", cls.api_key),
            data={"from" : f"{cls.from_title} <{cls.from_email}>",
                "to": email,
                "subject" : subject,
                "text" : text,
                "html" : html
                }) 
        if response.status_code != 200:
            raise MailGunException("Error on sending confirmation email, user registration failed")
        return response