import logging
from dataclasses import asdict

import httpx
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from email_validator import EmailNotValidError, validate_email

from core.settings import BASE_URL, HEIGHT, WIDTH
from layouts.base import BaseWindow
from models.order import Order
from models.product import Product
from models.user import ActiveUser
from utils.validatiors import ignore_none_values_and_empty_list

logger = logging.getLogger(__name__)


class OrderWindow(QMainWindow, BaseWindow):
    def __init__(self, product: Product, stacked_layout: QVBoxLayout):
        super().__init__()

        self.setWindowTitle('Оформление заказа')
        self.setGeometry(100, 100, WIDTH, HEIGHT)

        self.product = product
        self.stacked_layout = stacked_layout

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.addToolBar(self.init_header())

        form_layout = QFormLayout()

        fio_input = QLineEdit(self)
        fio_input.setPlaceholderText('Введите ФИО')
        fio_input.setStyleSheet('font-size: 18px; margin-top: 10px; color: #fff;')
        fio_input.setMaximumWidth(500)
        self.fio_input = fio_input
        form_layout.addRow(fio_input)

        email_input = QLineEdit(self)
        email_input.setPlaceholderText('Введите почту')
        email_input.setStyleSheet('font-size: 18px; margin-top: 10px; color: #fff;')
        email_input.setMaximumWidth(500)
        self.email_input = email_input
        form_layout.addRow(email_input)

        address_input = QLineEdit(self)
        address_input.setPlaceholderText('Введите адрес доставки')
        address_input.setStyleSheet('font-size: 18px; margin-top: 10px; color: #fff;')
        address_input.setMaximumWidth(500)
        self.address_input = address_input
        form_layout.addRow(address_input)

        order_button = QPushButton('Заказать', self)
        order_button.clicked.connect(self.process_order)
        order_button.setStyleSheet('font-size: 18px; margin-top: 20px;')
        order_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        form_layout.addRow(order_button)

        layout.addLayout(form_layout)

        h_box_layout = QHBoxLayout()
        h_box_layout.addStretch()
        h_box_layout.addLayout(layout)
        h_box_layout.addStretch()
        h_box_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        central_widget.setLayout(h_box_layout)

    def process_order(self):
        fio = self.fio_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.text().strip()

        if not (fio or email or address):
            QMessageBox.critical(self, 'Ошибка', 'Заполните все поля!')
            return

        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError as e:
            QMessageBox.critical(self, 'Ошибка', 'Введите корректный адрес электронной почты!')
            return

        order_info = f'Адрес доставки: {address}'
        self.create_order(
            Order(
                full_name=fio,
                email=email,
                address=address,
                product_id=self.product.id,
            ),
        )
        QMessageBox.information(self, 'Заказ оформлен', order_info)

        self.stacked_layout.setCurrentIndex(1)

    def create_order(self, order: Order) -> dict | None:
        url = f'{BASE_URL}/api/v1/orders/'
        access_token = ActiveUser().access_token
        try:
            with httpx.Client(follow_redirects=True, headers={'Authorization': f'Bearer {access_token}'}) as client:
                response = client.post(url, json=asdict(order, dict_factory=ignore_none_values_and_empty_list))
                return response.json()
        except httpx.RequestError as e:
            logger.error(f'Failed to fetch products. Error: {e}')
            return
