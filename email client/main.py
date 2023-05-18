import PySimpleGUI as sg
from SMTP import send_email
from IMAP import read_email
from sentence_transformers import CrossEncoder
model = CrossEncoder('cross-encoder/stsb-distilroberta-base')


imap_server = "imap.wp.pl"
email_address = ""
password = ""

SMTP_HOST = 'smtp.wp.pl'
SMTP_USER = ""
SMTP_PASS = ""


def check_similarity(messages):
    if len(messages) > 1:
        last_msg = messages[-1]
        prev_msg = messages[-2]
        if isinstance(last_msg, dict) and 'Content' in last_msg and isinstance(prev_msg, dict) and 'Content' in prev_msg:
            similarity = model.predict(
                [last_msg['Content'], prev_msg['Content']])[0]
            if similarity > 0.3:
                print("Last message is similar to previous message")
    else:
        print("Not enough messages to check similarity")


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
        messages = read_email(email_address, password, SMTP_PASS)
        window['-LIST-'].update(values=messages)
        # check_similarity(messages)

    if event == 'Save':
        email_address = values['-EMAIL-']
        password = values['-PASSWORD-']
        SMTP_PASS = values['-PASSWORD-']
        SMTP_USER = values['-EMAIL-']

window.close()
