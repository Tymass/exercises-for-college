from smtplib import SMTP_SSL, SMTP_SSL_PORT
from email.message import EmailMessage

SMTP_HOST = 'smtp.wp.pl'


def send_email(to, subject, body, email_address, SMTP_PASS, SMTP_USER):
    email_message = EmailMessage()
    email_message.add_header('To', to)
    email_message.add_header('From', SMTP_USER)
    email_message.add_header('Subject', subject)
    email_message.set_content(body)

    smtp_server = SMTP_SSL(SMTP_HOST, port=SMTP_SSL_PORT)
    smtp_server.set_debuglevel(1)
    smtp_server.login(SMTP_USER, SMTP_PASS)
    smtp_server.sendmail(email_address, to, email_message.as_bytes())
    smtp_server.quit()
