import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .config import (
    EMAIL_HOST,
    EMAIL_PORT,
    EMAIL_ADDRESS,
    EMAIL_PASSWORD
)

def send_email(to_email: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
