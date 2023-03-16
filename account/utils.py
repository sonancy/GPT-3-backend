import os
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .emailTemplates.verifyEmail import emailVerifyTemplate
from .token import account_activation_token


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['subject'],
                             body=data['body'],
                             from_email=os.environ.get("EMAIL_FROM"),
                             to=[data['to_email']]
                             )
        email.content_subtype = "html"
        email.send()


def sendEmail(user):
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = account_activation_token.make_token(user)

    link = f'http://localhost:3000/auth/verify-email?uid={uid}&token={token}'

    html = emailVerifyTemplate.replace("{link}", link)

    data = {
        'subject': 'Welcome to veWriter',
        'body': html,
        'to_email': user.email
    }

    Util.send_email(data)
