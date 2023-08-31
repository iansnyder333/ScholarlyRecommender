import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = None

EMAIL_PASSWORD = None

SUBSCRIBERS = [None]


def send_email(
    path: str = "ScholarlyRecommender/Newsletter/html/ExampleFeed.html",
):
    global EMAIL_ADDRESS, EMAIL_PASSWORD, SUBSCRIBERS

    msg = EmailMessage()
    msg["Subject"] = "Your Scholarly Recommender Weekly Newsletter"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = SUBSCRIBERS

    with open(path, "r") as f:
        html_string = f.read()
    msg.set_content(html_string, subtype="html")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
