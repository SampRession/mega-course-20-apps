import requests
from datetime import date, timedelta
from send_email import send_email
from files.config import API_KEY

today = date.today()
format_today = today.strftime("%d %b %Y")
yesterday = today - timedelta(1)

topic = "Python"

url = (f"https://newsapi.org/v2/everything?\
q={topic}&\
from={yesterday}&\
sortBy=popularity&\
language=en&\
pageSize=20&\
apiKey={API_KEY}\
")

request = requests.get(url)
content = request.json()

# Building a string
body = ""
for article in content["articles"]:
    title = article["title"] if article["title"] else "No title"
    desc = article["description"] if article["description"] else \
        "Description is missing"
    link = article["url"]
    body = f"""{body}{title}
Description:
{desc}
{link}


"""

body = body.encode("ascii", 'ignore').decode('ascii')
send_email(body, format_today)
