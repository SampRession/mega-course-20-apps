import smtplib
import ssl
import imghdr
from email.message import EmailMessage
from files import config


def send_email(image, date):
    smtp_server = "smtp.gmail.com"
    port = 465
    username = config.username
    password = config.password
    receiver_email = config.username

    email_message = EmailMessage()
    email_message["Subject"] = f"Movement has been detected! // {date}"
    email_message.set_content(
        "Hey, something has moved in front of the camera!\n")

    with open(image, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image",
                                 subtype=imghdr.what(image))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver_email, email_message.as_string())
        server.quit()
