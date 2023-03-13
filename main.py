import PySimpleGUI as sg
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from email.message import EmailMessage
import html2text
import email
import imaplib
import chardet
import re
from email.header import decode_header

imap_server = "imap.wp.pl"
email_address = ""
password = ""

SMTP_HOST = 'smtp.wp.pl'
SMTP_USER = ""
SMTP_PASS = ""


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


def read_email(email_address, password):

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

    imap.close()

    return messages


sg.theme('Default 1')
layout = [
    [sg.Text('Email sender and reader', font='Any 15')],
    [sg.Frame(layout=[
        [sg.Text('Email address:'), sg.InputText(key='-EMAIL-')],
        [sg.Text('Password:'), sg.InputText(
            key='-PASSWORD-', password_char='*')],
        [sg.Button('Save')],
    ], title='Account settings')],
    [sg.Frame(layout=[
        [sg.Text('To:'), sg.InputText(key='-TO-')],
        [sg.Text('Subject:'), sg.InputText(key='-SUBJECT-')],
        [sg.Multiline(key='-BODY-', size=(200, 15))],
        [sg.Button('Send')],
    ], title='Send email')],
    [sg.Frame(layout=[
        [sg.Listbox(values=[], key='-LIST-', size=(200, 20))],
        [sg.Button('Refresh')],
    ], title='Emails')]

]

window = sg.Window('Email App', layout, resizable=True, finalize=True)
window.set_min_size((1200, 600))

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == 'Send':
        to = values['-TO-']
        subject = values['-SUBJECT-']
        body = values['-BODY-']
        send_email(to, subject, body, email_address, SMTP_PASS, SMTP_USER)

    if event == 'Refresh':
        messages = read_email(email_address, password)
        window['-LIST-'].update(values=messages)

    if event == 'Save':
        email_address = values['-EMAIL-']
        password = values['-PASSWORD-']
        SMTP_PASS = values['-PASSWORD-']
        SMTP_USER = values['-EMAIL-']

window.close()
