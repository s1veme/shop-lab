from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
)


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Вход")
        self.setGeometry(100, 100, 1366, 768)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        # Поле ввода для почты
        email_edit = QLineEdit(self)
        email_edit.setPlaceholderText("Почта")
        email_edit.setStyleSheet("color: white; font-size: 18px;")
        email_edit.setMaximumWidth(500)
        form_layout.addRow(email_edit)

        # Поле ввода для пароля
        password_edit = QLineEdit(self)
        password_edit.setPlaceholderText("Пароль")
        password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        password_edit.setStyleSheet("color: white; font-size: 18px; margin-top: 10px;")
        password_edit.setMaximumWidth(500)
        form_layout.addRow(password_edit)

        # Кнопка "Войти"
        login_button = QPushButton("Войти", self)
        login_button.clicked.connect(self.login)
        login_button.setStyleSheet("font-size: 18px; margin-top: 20px;")
        login_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        button_layout = QHBoxLayout()
        button_layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        form_layout.addRow(button_layout)

        layout.addLayout(form_layout)

        # Выравниваем по вертикали
        h_box_layout = QHBoxLayout()
        h_box_layout.addStretch()
        h_box_layout.addLayout(layout)
        h_box_layout.addStretch()
        h_box_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.setLayout(h_box_layout)

    def login(self):
        # TODO: Добавить логику авторизации.
        print("Вход выполнен")
