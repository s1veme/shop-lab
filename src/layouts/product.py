import requests
from PyQt6.QtWidgets import (
    QMainWindow,
    QStackedLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QWidget,
)
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtCore import Qt

from core.settings import HEIGHT, WIDTH
from layouts.order import OrderWindow
from models.product import Product
from layouts.base import BaseWindow


class ProductDetailWindow(QMainWindow, BaseWindow):
    def __init__(self, product: Product, stacked_layout: QStackedLayout):
        super().__init__()

        self.setWindowTitle(product.title)
        self.setGeometry(100, 100, WIDTH, HEIGHT)

        self.stacked_layout = stacked_layout
        self.product = product

        self.init_ui(product)

    def init_ui(self, product: Product):
        main_layout = QVBoxLayout()

        self.addToolBar(self.init_header())

        details_layout = QGridLayout()

        image_label = QLabel()
        image = QPixmap()
        image.loadFromData(requests.get(product.image).content)
        image = image.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        image_label.setPixmap(image)
        details_layout.addWidget(image_label, 0, 0, 2, 1)

        name_label = QLabel(product.title)
        name_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        details_layout.addWidget(name_label, 0, 1, Qt.AlignmentFlag.AlignTop)

        price_label = QLabel(f'Цена: {product.price}')
        price_label.setStyleSheet('font-size: 16px;')
        details_layout.addWidget(price_label, 1, 1, Qt.AlignmentFlag.AlignBottom)

        buy_button = QPushButton('Купить')
        buy_button.setStyleSheet('font-size: 14px;')
        buy_button.clicked.connect(self.create_order)
        buy_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        details_layout.addWidget(buy_button, 2, 1, Qt.AlignmentFlag.AlignTop)

        description_label = QLabel(product.description)
        description_label.setWordWrap(True)
        details_layout.addWidget(description_label, 2, 0, 1, 1)

        main_layout.addLayout(details_layout)

        main_layout.addLayout(self.init_footer())

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_order(self, event):
        order_window = OrderWindow(self.product, self.stacked_layout)
        self.stacked_layout.addWidget(order_window)
        self.stacked_layout.setCurrentWidget(order_window)
