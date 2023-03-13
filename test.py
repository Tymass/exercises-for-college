def send_email(to, subject, content):
    from_email = SMTP_USER
    to_emails = [to]
    email_message = EmailMessage()
    email_message.add_header('To', ', '.join(to_emails))
    email_message.add_header('From', from_email)
    email_message.add_header('Subject', subject)
    email_message.add_header('X-Priority', '1')
    email_message.set_content(content)

    smtp_server = SMTP_SSL(SMTP_HOST, port=SMTP_SSL_PORT)
    smtp_server.set_debuglevel(1)
    smtp_server.login(SMTP_USER, SMTP_PASS)
    smtp_server.sendmail(from_email, to_emails, email_message.as_bytes())
    smtp_server.quit()
