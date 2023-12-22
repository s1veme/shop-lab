import logging
from dataclasses import asdict

import httpx
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QMessageBox,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
)

from core.settings import BASE_URL, HEIGHT, USER, WIDTH
from models.user import ActiveUser, CreateUser, User
from utils.validatiors import ignore_none_values_and_empty_list

logger = logging.getLogger(__name__)


class LoginWindow(QWidget):
    def __init__(self, stacked_layout: QFormLayout):
        super().__init__()

        self.stacked_layout = stacked_layout
        self.setWindowTitle('Вход')
        self.setGeometry(100, 100, WIDTH, HEIGHT)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        username_edit = QLineEdit(self)
        self.username_input = username_edit
        username_edit.setPlaceholderText('Имя пользователя')
        username_edit.setStyleSheet('color: white; font-size: 18px;')
        username_edit.setMaximumWidth(500)
        form_layout.addRow(username_edit)

        password_edit = QLineEdit(self)
        self.password_input = password_edit
        password_edit.setPlaceholderText('Пароль')
        password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        password_edit.setStyleSheet('color: white; font-size: 18px; margin-top: 10px;')
        password_edit.setMaximumWidth(500)
        form_layout.addRow(password_edit)

        login_button = QPushButton('Войти', self)
        login_button.setMaximumWidth(250)
        login_button.clicked.connect(self.login)
        login_button.setStyleSheet('font-size: 18px; margin-top: 20px;')
        login_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        register_button = QPushButton('Зарегистрироваться', self)
        register_button.setMaximumWidth(250)
        register_button.clicked.connect(self.register)
        register_button.setStyleSheet('font-size: 18px; margin-top: 20px;')
        register_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        button_layout = QHBoxLayout()
        button_layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignBottom)
        button_layout.addWidget(register_button, alignment=Qt.AlignmentFlag.AlignTop)
        form_layout.addRow(button_layout)

        layout.addLayout(form_layout)

        h_box_layout = QHBoxLayout()
        h_box_layout.addStretch()
        h_box_layout.addLayout(layout)
        h_box_layout.addStretch()
        h_box_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.setLayout(h_box_layout)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username:
            QMessageBox.critical(self, 'Ошибка!', 'Пожалуйста, заполните поле "Имя пользователя"')
            return

        if not password:
            QMessageBox.critical(self, 'Ошибка!', 'Пожалуйста, заполните поле "Пароль"')
            return

        response = self.authorize(CreateUser(username=username, password=password))
        if not response:
            QMessageBox.critical(self, 'Ошибка!', 'Кажется, произошла непредвиденная ошибка')
            return

        if 'No active account found with the given credentials' in response.get('detail', []):
            QMessageBox.critical(
                self, 'Неверные данные!', 'Кажется, пользователя с таким именем и паролем не существует'
            )
            return

        ActiveUser(username=username, access_token=response['access'])
        QMessageBox.information(self, 'Вы успешно вошли!', 'Вы успешно вошли в свой аккаунт!')
        self.stacked_layout.setCurrentIndex(1)

    def register(self) -> None:
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username:
            QMessageBox.critical(self, 'Ошибка!', 'Пожалуйста, заполните поле "Имя пользователя"')
            return

        if not password:
            QMessageBox.critical(self, 'Ошибка!', 'Пожалуйста, заполните поле "Пароль"')
            return

        response = self.create_user(CreateUser(username=username, password=password))
        if not response:
            QMessageBox.critical(self, 'Ошибка!', 'Кажется, произошла непредвиденная ошибка')
            return

        if 'Пользователь with this Имя пользователя already exists.' in response.get('username', []):
            QMessageBox.critical(self, 'Ошибка!', 'Данное имя пользователя уже занято!')
            return

        QMessageBox.information(self, 'Вы успешно зарегистрировались!', 'Пожалуйста, теперь войдите в свой аккаунт')

    def create_user(self, user: CreateUser) -> dict | None:
        url = f'{BASE_URL}/api/v1/users/'
        try:
            with httpx.Client(follow_redirects=True) as client:
                response = client.post(url, json=asdict(user, dict_factory=ignore_none_values_and_empty_list))
                return response.json()
        except httpx.RequestError as e:
            logger.error(f'failed to fetch products. Error: {e}')
            return

    def authorize(self, user: CreateUser) -> dict | None:
        url = f'{BASE_URL}/api/common/auth/token'
        try:
            with httpx.Client(follow_redirects=True) as client:
                response = client.post(url, json=asdict(user, dict_factory=ignore_none_values_and_empty_list))
                return response.json()
        except httpx.RequestError as e:
            logger.error(f'failed to fetch products. Error: {e}')
            return
