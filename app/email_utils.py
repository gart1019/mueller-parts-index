import logging
import traceback
from threading import Thread
from flask import render_template
from flask_mail import Message
from itsdangerous import URLSafeSerializer, SignatureExpired, BadSignature
from app import mail, app

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
s = URLSafeSerializer(app.config['SECRET_KEY'])
salt = "confirmation-email-sent"


def generate_token(email):
    return s.dumps(email, salt=salt)

def confirm_token(token, expiration=3600):
    try:
        return s.loads(token, salt=salt, max_age=expiration)
    except SignatureExpired:
        logging.warning("Token expired")
        return False
    except BadSignature:
        logging.warning("Invalid token sig")
        return False

def send_verification_email(to, name, verification_url):
    print("func started")
    try:
        print("try started")
        msg = Message(
            sender="<no-reply@notifications.muellerindex.org>",
            subject="Email Verification Required",
            recipients=[to],
            html=render_template('emails/verification.html', name=name, verify_url=verification_url, email=to)
        )
        print("sending")
        mail.send(msg)
        print("sent")
        logging.info(f"Verification email sent to {to}")
    except Exception as e:
        logging.error(f"Error sending email to {to}: {str(e)}")
        logging.error(traceback.format_exc()) 