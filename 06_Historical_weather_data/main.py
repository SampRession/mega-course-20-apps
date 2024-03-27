import numpy as np
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

stations = pd.read_csv("data/sources.txt", skiprows=23)
html_stations = stations.to_html(columns=[" SOUID", "SOUNAME                 "
                                                    "                "])


@app.route("/")
def home():
    return render_template("home.html", data=html_stations)


@app.route("/api/v1/<station>")
def get_station_hist(station):
    try:
        filename = f"data/TG_SOUID{str(station).zfill(6)}.txt"
        df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
        df["CELSIUS"] = df["   TG"] / 10
        # En html (essai avant solution)
        # html_df = df.to_html(columns=["    DATE", "CELSIUS"])
        # return render_template("query.html", data=html_df)
        #
        # En dictionnaire
        dict_result = df.to_dict(orient="records")
        return dict_result
    except FileNotFoundError:
        return "Error: No existing data for this station"


@app.route("/api/v1/<station>/<date>")
def get_temp(station, date):
    try:
        filename = f"data/TG_SOUID{str(station).zfill(6)}.txt"
        df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
        df["CELSIUS"] = df["   TG"].mask(df[" Q_TG"] != 0, np.nan) / 10
        temperature = df.loc[df["    DATE"] == date]["CELSIUS"].squeeze()
        return {"station"    : station,
                "date"       : date,
                "temperature": temperature}
    except FileNotFoundError:
        return "Error: No existing data for this station"


@app.route("/api/v1/<station>/yearly/<year>")
def get_year_hist(station, year):
    try:
        filename = f"data/TG_SOUID{str(station).zfill(6)}.txt"
        df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
        df["CELSIUS"] = df["   TG"] / 10
        df["    DATE"] = df["    DATE"].astype(str)
        result = df[df["    DATE"].str.startswith(str(year))]
        dict_result = result.to_dict(orient="records")
        return dict_result
    except FileNotFoundError:
        return "Error: No existing data for this station"


if __name__ == "__main__":
    app.run(debug=True)
