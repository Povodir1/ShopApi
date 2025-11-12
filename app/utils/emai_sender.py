import smtplib
from email.mime.text import MIMEText
from pydantic import EmailStr

from app.core.config import settings



def send_email(email:str|EmailStr,message:str,title:str = "Новое сообщение"):
    sender = settings.EMAIL_SENDER
    password = settings.EMAIL_PASSWORD

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()

    msg = MIMEText(message)
    msg["Subject"] = title
    try:
        server.login(sender,password)
        server.sendmail(sender,email,msg.as_string())
    except Exception as e:
        raise e
