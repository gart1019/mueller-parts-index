import os 
import resend

resend.api_key = os.environ["EMAIL_KEY"]

def sendEmail(to, subject: str):

    params: resend.Emails.SendParams = {
        "from": "Mueller Parts Index - Support <no-reply@support.garrettnorman.us>",
        "to": to,
        "subject": subject,
        "html": "<strong>it works!</strong>",
    }
    
    resend.Emails.send(params=params)