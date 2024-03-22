from flask_mail import Message
from extensions import mail


def mail_notify(users, status):
    with mail.connect() as conn:
        for user in users:
            if user.email is None:
                continue
            if status == 1:
                message = 'room activated'
            else:
                message = 'room deactivated'
            subject = "hello, %s" % user.nickname
            msg = Message(recipients=[user.email],
                          body=message,
                          subject=subject,
                          sender=("Admin", "admin@soulfar.com"))

            conn.send(msg)


def mail_morning(users):
    with mail.connect() as conn:
        for user in users:
            if user.email is None:
                continue
            message = '...'
            subject = "hello, %s" % user.nickname
            msg = Message(recipients=[user.email],
                          body=message,
                          subject=subject,
                          sender=("Admin", "admin@soulfar.com"))

            conn.send(msg)


def mail_night(users):
    with mail.connect() as conn:
        for user in users:
            if user.email is None:
                continue
            message = '...'
            subject = "hello, %s" % user.nickname
            msg = Message(recipients=[user.email],
                          body=message,
                          subject=subject,
                          sender=("Admin", "admin@soulfar.com"))

            conn.send(msg)