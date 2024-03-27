from streamlit import secrets
import requests

API_KEY = secrets["API_KEY"]


def get_data(place, forecast_days):
    url = (f"https://api.openweathermap.org/data/2.5/forecast?"
           f"q={place.capitalize()}"
           f"&cnt={forecast_days * 8}"
           "&units=metric"
           f"&APPID={API_KEY}")
    response = requests.get(url)
    data = response.json()
    if data["cod"] == "200":
        filtered_data = data["list"]
        filtered_time = [l_dict["dt_txt"] for l_dict in filtered_data]
        return filtered_data, filtered_time


if __name__ == "__main__":
    get_data("Carpentras", 3)
