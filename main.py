import PySimpleGUI as sg


username = ''
password = ''
# PROGRESS BAR


def login():
    global username, password
    sg.theme("LightBlue2")
    layout = [[sg.Text("Log In", size=(15, 1), font=40)],
              [sg.Text("Username", size=(15, 1), font=16),
               sg.InputText(key='-usrnm-', font=16)],
              [sg.Text("Password", size=(15, 1), font=16), sg.InputText(
                  key='-pwd-', password_char='*', font=16)],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    window = sg.Window("Log In", layout)

    while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Ok":
                if values['-usrnm-'] == username and values['-pwd-'] == password:
                    sg.popup("Welcome!")
                    break
                elif values['-usrnm-'] != username or values['-pwd-'] != password:
                    sg.popup("Invalid login. Try again")

    window.close()


login()
