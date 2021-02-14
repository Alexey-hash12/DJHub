from django.core.mail import send_mail


def send(user_email, author, video):
    send_mail(
        f"A new video has been released on DjHub by {author}",
        f"Author {author} released new video {video}",
        'ryzhakovalexeynicol@gmail.com',
        [user_email],
        fail_silently=False
    )
