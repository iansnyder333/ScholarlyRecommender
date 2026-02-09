"""
Example of how to configure the email server if you have installed ScholarlyRecommender
locally:
Replace the constants with your own email address, password, port number and
subscribers (delivery address).
Note that you need to enable less secure apps in your google account settings,
otherwise this will not work.
Once you have your own constants working, you can delete the input() calls and replace
them with your own constants.
To send an email, simply call send_email(content=html_string) from the Newsletter
module. html_string is the return value from the get_feed() function in feed.py.
"""

import smtplib
from email.message import EmailMessage
import re


def validate_email(email):
    """Validate an email address using regex."""
    regex = r"^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.match(regex, email):
        return True
    return False


def send_email(**kwargs):
    """Send an email using the configured email server."""
    EMAIL_ADDRESS = input("Enter your email address: ")
    EMAIL_PASSWORD = input("Enter your email password: ")
    SUBSCRIBERS = input(
        "Enter your subscribers email addresses (separated by commas): "
    )
    PORT = input("Enter your port number: (465 for gmail)")

    msg = EmailMessage()
    msg["Subject"] = "Your Scholarly Recommender Newsletter"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = SUBSCRIBERS

    html_string = kwargs["content"]

    msg.set_content(html_string, subtype="html")
    with smtplib.SMTP_SSL("smtp.gmail.com", PORT) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
