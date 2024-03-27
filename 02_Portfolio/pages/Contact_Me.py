import streamlit as st
import pandas as pd
from email_validator import validate_email, EmailNotValidError
from send_email import send_email


st.set_page_config(layout="wide", page_title="Contact Me")

st.header("Contact Me")

df = pd.read_csv("topics.csv")
with st.form(key="contact_form"):
    user_email = st.text_input("Your email address", placeholder="johnsmith@gmail.com")
    user_topic = st.selectbox("Why would you like to contact me?", df, index=None)
    user_message = st.text_area("Your message", max_chars=2048, help="You can write in english, or in french!")
    button = st.form_submit_button("Send")
    if button:
        try:
            validate_email(user_email)
            send_email(user_email, user_topic, user_message)
            st.info("Your email was sent successfully!")
        except EmailNotValidError:
            st.error("Your email address is not valid.")
