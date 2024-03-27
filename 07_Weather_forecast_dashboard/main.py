import streamlit as st
import plotly.express as px
from backend import get_data

# User interface
st.title("Weather Forecast for the Next Days")
place = st.text_input("Place:", placeholder="E.g. Paris, Tirana ...")\
        .capitalize()
days = st.slider("Forecast Days", 1, 5, help="Select number of forecasted days"
                 )
option = st.selectbox("Select data to view", ("Temperature", "Sky"))

try:
    # Get data and time
    data, time = get_data(place, days)

    if place:
        st.header(f"{option} for the next {days} days in {place}")

        # Temperature plot
        if option == "Temperature":
            temperatures = [l_dict["main"]["temp"] for l_dict in data]
            figure = px.line(x=time, y=temperatures,
                             labels={"x": "Time", "y": f"{option} (C°)"})
            st.plotly_chart(figure)

        # Sky visualization
        if option == "Sky":
            sky_conditions = [l_dict["weather"][0]["main"] for l_dict in data]
            img_list = [f"resources/{condition.lower()}.png"
                        for condition in sky_conditions]
            st.image(img_list, width=115, caption=time)

except TypeError:
    st.error("No existing data for this city. Either there is no weather "
             "station here, or there is a typo in the city name.")
