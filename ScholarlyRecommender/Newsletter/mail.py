import smtplib
from email.message import EmailMessage


def send_email(
    path: str = "ScholarlyRecommender/Newsletter/html/NewTestFeed.html",
):
    EMAIL_ADDRESS = "scholarlyrecommender@gmail.com"

    EMAIL_PASSWORD = input("*")

    SUBSCRIBERS = [
        "scholarlyrecommender@gmail.com",
    ]

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


# send_email(path="ScholarlyRecommender/Newsletter/html/NewTestFeed.html")