from smtplib import SMTP_SSL, SMTP_SSL_PORT
from email.message import EmailMessage

SMTP_HOST = 'smtp.wp.pl'
SMTP_USER = 'krzysztofisthebest@wp.pl'
# SMTP_PASS = input("Enter your password: ")
SMTP_PASS = 'haslotestowe123'


from_email = SMTP_USER
to_emails = ['krzysztofisthebest@wp.pl']
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
