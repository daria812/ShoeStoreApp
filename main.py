import sys
from PySide6.QtWidgets import QApplication
from windows.login_window import LoginWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    app.setStyleSheet("""
        QLabel, QPushButton, QLineEdit, QComboBox, QRadioButton {
            color: #000000;
        }
        QMainWindow, QWidget {
            background-color: #FFFFFF;
        }
        QPushButton {
            background-color: #00FA9A;
            border: none;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: #00CC7A;
        }
    """)

    sys.exit(app.exec())