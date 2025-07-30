import smtplib
from email.mime.text import MIMEText
import random
import string
from core.config import settings
from fastapi import HTTPException
import logging
from jinja2 import Environment, FileSystemLoader


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

env = Environment(loader=FileSystemLoader('templates'))

async def generate_verification_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

async def send_verification_email(email: str, code: str):
    logger.info(f"Sending email from {settings.MAIL_USERNAME} via {settings.MAIL_SERVER}:{settings.MAIL_PORT}")
    
    template = env.get_template('send_email.html')
    
    html_content = template.render(
        verification_code=code,
        email=email
    )
    
    msg = MIMEText(html_content, 'html')
    msg['Subject'] = 'Подтверждение email'
    msg['From'] = settings.MAIL_USERNAME
    msg['To'] = email

    try:
        with smtplib.SMTP_SSL(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
            server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
            server.send_message(msg)
        logger.info(f"Email sent successfully to {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")