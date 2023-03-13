import time

while True:
    # Odczytaj najnowszą wiadomość
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(email_address, passowrd)
    imap.select("Inbox")
    _, msgnums = imap.search(None, "ALL")
    latest_msgnum = msgnums[0].split()[-1]
    _, data = imap.fetch(latest_msgnum, "(RFC822)")
    message = email.message_from_bytes(data[0][1])
    imap.close()

    # Utwórz odpowiedź
    email_message = EmailMessage()
    email_message.add_header('To', message['From'])
    email_message.add_header('From', from_email)
    email_message.add_header('Subject', 'Re: ' + message['Subject'])
    email_message.set_content(
        'Wiadomość dotarła do TBYRWA_ENTERPRISE, niedługo odpowiemy.')

    # Wyślij odpowiedź
    smtp_server = SMTP_SSL(SMTP_HOST, port=SMTP_SSL_PORT)
    smtp_server.login(SMTP_USER, SMTP_PASS)
    smtp_server.send_message(
        email_message, from_addr=from_email, to_addrs=message['From'])
    smtp_server.quit()

    # Odczekaj 5 sekund przed kolejnym sprawdzeniem skrzynki pocztowej
    time.sleep(5)
