import time
from SMTP import send_email


def autoresponder(to, from_, subject, content, SMTP_PASS, SMTP_USER):
    body = f"Thank you for your email. We have received your message and will respond as soon as possible.\n\nOriginal message:\nFrom: {from_}\nSubject: {subject}\n\n{content}"
    send_email(to, "Autoresponse", body, from_, SMTP_PASS, SMTP_USER)
