import html2text
import email
import imaplib
import chardet
import re
from email.header import decode_header
from SMTP import send_email

imap_server = "imap.wp.pl"


def read_email(email_address, password, SMTP_PASS):

    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(email_address, password)

    imap.select("Inbox")
    _, msgnums = imap.search(None, "ALL")  # wazne

    messages = []
    for msgnum in msgnums[0].split():
        _, data = imap.fetch(msgnum, "(RFC822)")

        message = email.message_from_bytes(data[0][1])
        subject = decode_header(message.get('Subject'))[0][0]
        if isinstance(subject, bytes):
            # if it's a bytes type, decode to str
            subject = subject.decode()
        from_ = decode_header(message.get('From'))[0][0]
        if isinstance(from_, bytes):
            from_ = from_.decode()
        to_ = decode_header(message.get('To'))[0][0]
        if isinstance(to_, bytes):
            to_ = to_.decode()

        content = ''
        for part in message.walk():
            if part.get_content_maintype() == 'text':
                kodowanie = part.get_content_charset()
                if kodowanie is None:
                    # Użyj modułu chardet do wykrycia kodowania
                    kodowanie = chardet.detect(part.get_payload())['encoding']
                tekst = part.get_payload(
                    decode=True).decode(kodowanie, 'ignore')
                tekst = re.sub(r'<table.*?>.*?</table>',
                               '', tekst, flags=re.DOTALL)
                content = html2text.html2text(tekst)

        messages.append({
            'Subject': subject,
            'From': from_,
            'To': to_,
            'Content': content
        })

        flags = imap.fetch(msgnum, '(FLAGS)')[1][0]
        print(flags)
        if b'\\Seen' not in flags:
            auto_response_text = "Thank you for your email. We have received your message and will respond as soon as possible."
            reply_subject = "Odpowiedź na: " + subject
            reply_body = auto_response_text.format(from_=from_)
            send_email(from_, reply_subject, reply_body,
                       email_address, SMTP_PASS, email_address)

    imap.close()

    return messages
