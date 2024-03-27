import smtplib
import ssl
from files import config


def send_email(msg_body, date):
    smtp_server = "smtp.gmail.com"
    port = 465
    username = config.username
    password = config.password

    receiver_email = config.username
    message = f"""\
Subject: Daily digest // {date}
Here are the yesterday news mentioning "Python":

{msg_body}


Requested from NewsAPI.org
"""
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver_email, message)
        server.quit()
