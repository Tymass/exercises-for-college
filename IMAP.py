import html2text
import email
import imaplib
import chardet
import re
from email.header import decode_header

imap_server = "imap.wp.pl"
email_address = "krzysztofisthebest@wp.pl"
# passowrd = input("Enter your password: ")
passowrd = "haslotestowe123"

imap = imaplib.IMAP4_SSL(imap_server)
imap.login(email_address, passowrd)

imap.select("Inbox")
_, msgnums = imap.search(None, "ALL")  # wazne


for msgnum in msgnums[0].split():
    _, data = imap.fetch(msgnum, "(RFC822)")

    # raw_email_string = data[0][1].decode('utf-8')
    # mail = mailparser.parse_from_string(raw_email_string)

    message = email.message_from_bytes(data[0][1])
    # print(f"Message number: {msgnum}")
    print(f"From: {decode_header(message.get('From'))[0][0]}")
    print(f"To: {decode_header(message.get('To'))[0][0]}")
    # print(f"BCC: {message.get('BCC')}")
    # print(f"Date: {message.get('Date')}")
    # print(f"Subject: {message.get('Subject')}")
    # print(f'Content: \n{mail.text_plain}')

    tresc = ''
    for part in message.walk():
        if part.get_content_maintype() == 'text':
            kodowanie = part.get_content_charset()
            if kodowanie is None:
                # Użyj modułu chardet do wykrycia kodowania
                kodowanie = chardet.detect(part.get_payload())['encoding']
            tekst = part.get_payload(decode=True).decode(kodowanie, 'ignore')
            tekst = re.sub(r'<table.*?>.*?</table>',
                           '', tekst, flags=re.DOTALL)
            tresc = html2text.html2text(tekst)

    print(
        f'CONTENT------------------------------------\n{tresc}')


imap.close()
