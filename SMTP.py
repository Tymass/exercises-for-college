from smtplib import SMTP_SSL, SMTP_SSL_PORT
from email.message import EmailMessage

SMTP_HOST = 'mail.example.com'
SMTP_USER = 'someone@example.com'
SMTP_PASS = 'Secret!'


from_email = 'My name <someone@examples.com>'
to_emails = ['nanodano@devdungeon.com', 'admin@devdungeon.com']
email_message = EmailMessage()
email_message.add_header('To', ', '.join(to_emails))
email_message.add_header('From', from_email)
email_message.add_header('Subject', 'Hello!')
email_message.add_header('X-Priority', '1')
email_message.set_content('Hello, world!')


smtp_server = SMTP_SSL(SMTP_HOST, port=SMTP_SSL_PORT)
smtp_server.set_debuglevel(1)
smtp_server.login(SMTP_USER, SMTP_PASS)
smtp_server.sendmail(from_email, to_emails, email_message)

smtp_server.quit()
