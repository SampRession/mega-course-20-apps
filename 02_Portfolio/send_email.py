import smtplib
import ssl
import streamlit as st


def send_email(user_email=None, user_topic=None, user_message=None):
    smtp_server = "smtp.gmail.com"
    port = 465
    username = st.secrets["db_username"]
    password = st.secrets["db_password"]

    receiver_email = st.secrets["db_username"]
    message = f"""\
Subject: {user_topic} // from {user_email}
{user_message}


Sent from {user_email}
"""
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver_email, message)
        server.quit()
