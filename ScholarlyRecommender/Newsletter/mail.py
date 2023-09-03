import smtplib
from email.message import EmailMessage


def send_email(**kwargs):
    EMAIL_ADDRESS = kwargs["email"]

    EMAIL_PASSWORD = kwargs["password"]

    SUBSCRIBERS = kwargs["subscribers"]

    msg = EmailMessage()
    msg["Subject"] = "Your Scholarly Recommender Weekly Newsletter"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = SUBSCRIBERS

    html_string = kwargs["content"]
    msg.set_content(html_string, subtype="html")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
