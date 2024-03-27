import time
import requests
import selectorlib
import smtplib
import ssl
import sqlite3
from files import config

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}


class Event:
    def scrape(self, url):
        """Scrape the page source from the URL and return it as string,
        formatted in HTML"""
        response = requests.get(url, headers=HEADERS)
        source = response.text
        return source

    def extract(self, source):
        """Extract the target (in yaml) value and return it as a string"""
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class Email:
    def send(self, msg_body):
        """"Send an email containing the formatted content of the database"""
        smtp_server = "smtp.gmail.com"
        port = 465
        username = config.username
        password = config.password

        receiver_email = config.username
        message = f"""\
Subject: Upcoming tours

Here are the upcoming tours listed by PythonAnywhere:

{msg_body}



Scraped from https://programmer100.pythonanywhere.com/tours/
"""
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, receiver_email, message)
            print("Email was sent!")
            server.quit()


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("database/data.db")

    def read(self):
        """Read all the content of the table 'events' in database and return
        it"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events")
        rows = cursor.fetchall()
        return rows

    def format_db(self):
        """Format the content of the database to natural language and write it
        in a .txt file. Then, return the content of this .txt file as a string.
        """
        rows = self.read()
        with open("database/formatted_data.txt", "a") as file:
            for row in rows:
                text = f"{row[0]}, {row[1]}, {row[2]}\n"
                file.write(text)
            file.close()
        with open("database/formatted_data.txt", "r") as file:
            content = file.read()
            file.close()
            return content

    def compare(self, extracted):
        """Check if the extracted content already exists in database, return
        True or False"""
        row = extracted.split(",")
        row = [item.strip() for item in row]
        band, city, date = row
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM events WHERE band=? AND city=? AND date=?",
            (band, city, date))
        rows = cursor.fetchall()
        return rows

    def store(self, extracted):
        """Store the extracted content in a new row in the database"""
        row = extracted.split(",")
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES (?,?,?)", row)
        self.connection.commit()


def main():
    while True:
        event = Event()
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)
        if extracted != "No upcoming tours":
            database = Database()
            row = database.compare(extracted)
            if not row:
                database.store(extracted)
                print(extracted)
                email = Email()
                email.send(database.format_db())
        time.sleep(2)


if __name__ == "__main__":
    main()
