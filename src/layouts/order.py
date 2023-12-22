from PyQt6.QtWidgets import QGridLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget

from core.settings import HEIGHT, WIDTH
from models.product import Product


class OrderWindow(QMainWindow):
    def __init__(self, product: Product):
        super().__init__()

        self.setWindowTitle('Оформление заказа')
        self.setGeometry(100, 100, WIDTH, HEIGHT)

        self.product = product

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        grid_layout = QGridLayout()

        fio_label = QLabel('Введите ФИО:')
        self.fio_input = QLineEdit(self)
        grid_layout.addWidget(fio_label, 0, 0)
        grid_layout.addWidget(self.fio_input, 0, 1)

        email_label = QLabel('Введите почту:')
        self.email_input = QLineEdit(self)
        grid_layout.addWidget(email_label, 1, 0)
        grid_layout.addWidget(self.email_input, 1, 1)

        address_label = QLabel('Введите адрес доставки:')
        self.address_input = QLineEdit(self)
        grid_layout.addWidget(address_label, 2, 0)
        grid_layout.addWidget(self.address_input, 2, 1)

        main_layout.addLayout(grid_layout)

        order_button = QPushButton('Заказать', self)
        order_button.clicked.connect(self.place_order)
        main_layout.addWidget(order_button)

        central_widget.setLayout(main_layout)

    def place_order(self):
        fio = self.fio_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.text().strip()

        if not (fio or email or address):
            QMessageBox.critical(self, 'Ошибка', 'Заполните все поля!')
            return

        if '@' not in email or '.' not in email:
            QMessageBox.critical(self, 'Ошибка', 'Введите корректный адрес электронной почты!')
            return

        order_info = f'Адрес доставки: {address}\nНомер заказа: {self.product.id}'
        QMessageBox.information(self, 'Заказ оформлен', order_info)

        self.close()
