import smtplib
from email.message import EmailMessage
import re
import os


def validate_email(email):
    regex = r"^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.match(regex, email):
        return True
    return False
