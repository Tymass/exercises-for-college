import PySimpleGUI as sg
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from email.message import EmailMessage
from SMTP import send_email

SMTP_HOST = 'smtp.wp.pl'
SMTP_USER = 'krzysztofisthebest@wp.pl'
# SMTP_PASS = input("Enter your password: ")
SMTP_PASS = 'haslotestowe123'


sg.theme('Default 1')
layout = [
    [sg.Text('Email sender and reader', font='Any 15')],
    [sg.Frame(layout=[
        [sg.Text('To:'), sg.InputText(key='-TO-')],
        [sg.Text('Subject:'), sg.InputText(key='-SUBJECT-')],
        [sg.Multiline(key='-BODY-', size=(60, 20))],
        [sg.Button('Send')],
    ], title='Send email')],
    [sg.Frame(layout=[
        [sg.Listbox(values=[], key='-LIST-', size=(60, 20))],
        [sg.Button('Refresh')],
    ], title='Emails')]
]

window = sg.Window('Email App', layout, resizable=True)
window.close()
