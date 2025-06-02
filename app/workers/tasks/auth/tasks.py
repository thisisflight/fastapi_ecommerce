import asyncio

from celery import shared_task
from fastapi_mail import FastMail, MessageSchema

from app.backend import mail_conf, settings


@shared_task()
def send_verification_email(email: str, token: str):
    verification_url = f"{settings.DOMAIN}/verify/email?token={token}"

    message = MessageSchema(
        subject="Активация почты",
        recipients=[email],
        body=f"Подтвердите email: {verification_url}",
        subtype="plain",
    )

    async def _send():
        fm = FastMail(mail_conf)
        await fm.send_message(message)

    asyncio.run(_send())
