import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

col1, col2 = st.columns(2)

with col1:
    # st.image("images/photo.png")
    st.text("Image not yet imported...")
with col2:
    st.title("Bast'")
    my_desc_1 = "Hey, I am Bastien! A recent Python learner."
    st.markdown(my_desc_1)

    my_desc_2 = """I did several different jobs, all about working with my 
    hands (stoneworker, landscaper, horticulturist...) and I currently run a 
    woodworking business in France: "[L'Art, mais pas trop]( 
    https://lartmaispastrop.fr/)". (Check out my work on [Instagram](
    https://www.instagram.com/lart_maispastrop/)!)"""
    st.markdown(my_desc_2)

    my_desc_3 = """I have not yet worked in programming, or any other IT 
    profession, but I really would like to find my way in this domain, 
    or even better, in video game development! (while keeping my business, 
    of course, I can't quit manual work :blush:)."""
    st.markdown(my_desc_3)

    my_desc_4 = ("I am learning Python as a beginning, and will see what the "
                 "future holds for me!")
    st.markdown(my_desc_4)

st.write("")
st.write("")
content1 = ("Below, you will find some of the apps I have built in Python. "
            "Feel free to contact me!")
st.write(content1)


col3, empty_col, col4 = st.columns([1.5, 0.5, 1.5])

df = pd.read_csv("data.csv")
with col3:
    for index, row in df.iterrows():
        if index % 2 == 0:
            st.header(row["title"])
            st.write(row["description"])
            st.image("images/" + row["image_path"])
            st.link_button("Go to source code", row["source_code_url"])

with col4:
    for index, row in df.iterrows():
        if index % 2 == 1:
            st.header(row["title"])
            st.write(row["description"])
            st.image("images/" + row["image_path"])
            st.link_button("Go to source code", row["source_code_url"])
