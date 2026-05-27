from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from database.db import Database
from windows.main_window import MainWindow
import os
from PySide6.QtGui import QIcon

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database.instance()
        self.setWindowTitle("Вход")
        self.resize(300, 200)

        icon_path = os.path.join(os.path.dirname(__file__), "..", "images", "Icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            # Если нет .ico, можно взять .png
            icon_path = os.path.join(os.path.dirname(__file__), "..", "images", "Icon.png")
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Логин:"))
        self.login_edit = QLineEdit()
        layout.addWidget(self.login_edit)

        layout.addWidget(QLabel("Пароль:"))
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_edit)

        btn_login = QPushButton("Войти")
        btn_login.clicked.connect(self.login)
        layout.addWidget(btn_login)

        btn_guest = QPushButton("Войти как гость")
        btn_guest.clicked.connect(self.guest_login)
        layout.addWidget(btn_guest)

        self.setLayout(layout)

    def login(self):
        login = self.login_edit.text()
        password = self.password_edit.text()
        query = "SELECT role, full_name FROM users WHERE login=%s AND password_hash=%s"
        rows = self.db.execute_query(query, (login, password))
        if rows:
            role = rows[0]['role']
            full_name = rows[0]['full_name']
            self.main_window = MainWindow(role, full_name)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def guest_login(self):
        self.main_window = MainWindow("guest", "Гость")
        self.main_window.show()
        self.close()