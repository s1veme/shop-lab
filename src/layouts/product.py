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
from models.product import Product
from layouts.base import BaseWindow


class ProductDetailWindow(QMainWindow, BaseWindow):
    def __init__(self, product: Product, stacked_layout: QStackedLayout):
        super().__init__()

        self.setWindowTitle(product.title)
        self.setGeometry(100, 100, WIDTH, HEIGHT)

        self.stacked_layout = stacked_layout

        self.init_ui(product)

    def init_ui(self, product: Product):
        main_layout = QVBoxLayout()

        main_layout.addLayout(self.init_header(self.return_to_catalog))

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
        details_layout.addWidget(buy_button, 2, 1, Qt.AlignmentFlag.AlignTop)

        description_label = QLabel(product.description)
        details_layout.addWidget(description_label, 2, 0, 1, 1)

        return_to_catalog_action = QAction('Вернуться в каталог', self)
        return_to_catalog_action.triggered.connect(self.return_to_catalog)
        toolbar = self.addToolBar('ReturnToCatalogToolbar')
        toolbar.addAction(return_to_catalog_action)

        main_layout.addLayout(details_layout)

        main_layout.addLayout(self.init_footer())

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def return_to_catalog(self):
        self.stacked_layout.setCurrentIndex(0)
