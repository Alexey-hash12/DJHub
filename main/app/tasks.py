# from celery import shared_task
from .models import VideoModels
from main.celery import app
from .service import send

@app.task
def send_message(user_email, author, video):
    send(user_email, author, video)
