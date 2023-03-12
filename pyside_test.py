from PySide6.QtWidgets import QApplication, QWidget


app = QApplication([])


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setup()

    def setup(self):
        self.setFixedSize(400, 600)
        self.setWindowTitle("WIDNOW")
        self.show()


login_window = LoginWindow()

app.exec()
