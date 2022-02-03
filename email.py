from fastapi import (
    BackgroudTasks,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException,
    status,
)
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import dotenv_values

config_credentials = dotenv_values(".env")

conf = ConnectionConfig(
    MAIL_USERNAME=config_credentials["MAIL_ADDRESS"],
    MAIL_PASSWORD=config_credentials["MAIL_PASSWORD"],
    MAIL_FROM=config_credentials["MAIL_ADDRESS"],
    MAIL_PORT="587",
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="hi!!!"
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
)
