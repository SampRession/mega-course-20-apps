from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__)

app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = config.username
app.config["MAIL_PASSWORD"] = config.password

db = SQLAlchemy(app)
mail = Mail(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    start_date = db.Column(db.Date)
    occupation = db.Column(db.String(80))
    

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"].title()
        last_name = request.form["last_name"].title()
        user_email = request.form["email"]
        start_date = request.form["date"]
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        occupation = request.form["occupation"].capitalize()
        
        form = Form(first_name=first_name,
                    last_name=last_name,
                    email=user_email,
                    start_date=start_date_obj,
                    occupation=occupation)
        db.session.add(form)
        db.session.commit()
        
        message_body = f"Thank you for your submission, {first_name}.\n\n" \
                        f"Here are your data:\n" \
                        f"- Name: {first_name} {last_name}\n" \
                        f"- Available start date: {start_date}\n" \
                        f"- Current occupation: {occupation}\n\n" \
                        f"I will contact you later, have a great day!"
                    
        message = Message(subject="New form submission",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[user_email],
                          body=message_body)
        mail.send(message)
        
        flash(f"Hey {first_name.title()}, " 
              "your form was successfully submitted!", 
              "success")
        
        return redirect(url_for("index"))
    
    return render_template("index.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)