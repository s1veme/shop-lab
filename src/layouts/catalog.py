from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QStackedLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QWidget,
    QScrollArea,
)
from PyQt6.QtGui import QPixmap

from core.settings import HEIGHT, WIDTH
from layouts.base import BaseWindow
from layouts.order import OrderWindow
from layouts.product import ProductDetailWindow
from mocks.products import MOCK_PRODUCTS_DATA
from models.product import Product


class ProductCard(QWidget):
    product: Product

    def __init__(
        self,
        product: Product,
        on_clicked: Callable,
        stacked_layout: QStackedLayout,
    ):
        super().__init__()
        self.product = product
        self.stacked_layout = stacked_layout

        layout = QVBoxLayout()

        name_label = QLabel(product.title)
        name_label.setCursor(Qt.CursorShape.PointingHandCursor)
        name_label.mousePressEvent = on_clicked
        layout.addWidget(name_label)

        description_label = QLabel(product.description)
        layout.addWidget(description_label)

        price_label = QLabel(str(product.price))
        layout.addWidget(price_label)

        image_label = QLabel()
        image_label.setPixmap(QPixmap(product.image))
        layout.addWidget(image_label)

        buy_button = QPushButton('Купить')
        buy_button.clicked.connect(self.create_order)
        layout.addWidget(buy_button)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setMaximumWidth(200)
        self.setStyleSheet("margin: 5px; padding: 10px; background-color: #000; border-radius: 20%;")
        self.setLayout(layout)

    def create_order(self, event):
        print(type(event))
        order_window = OrderWindow(self.product)
        self.stacked_layout.addWidget(order_window)
        self.stacked_layout.setCurrentWidget(order_window)


class ProductCatalogWindow(QMainWindow, BaseWindow):
    def __init__(self, stacked_layout: QStackedLayout):
        super().__init__()

        self.setWindowTitle('Каталог товаров')
        self.setGeometry(100, 100, WIDTH, HEIGHT)

        self.stacked_layout = stacked_layout

        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()

        self.main_layout.addLayout(self.init_header(self.logout))

        self.scroll_area = QScrollArea()
        self.scroll_area_widget = QWidget()
        self.catalog_layout = QGridLayout(self.scroll_area_widget)
        self.catalog_layout.setHorizontalSpacing(10)
        self.catalog_layout.setVerticalSpacing(10)
        self.catalog_layout.setColumnMinimumWidth(0, 200)

        self.populate_catalog()

        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.main_layout.addWidget(self.scroll_area)

        self.main_layout.addLayout(self.init_footer())

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def populate_catalog(self):
        for i, product in enumerate(MOCK_PRODUCTS_DATA):
            card = Product(**product)
            product_card = ProductCard(
                card,
                lambda event: self.on_product_clicked(event, card),
                self.stacked_layout,
            )
            row, col = divmod(i, 4)
            self.catalog_layout.addWidget(product_card, row, col)

    def on_product_clicked(self, event, product):
        detail_window = ProductDetailWindow(product, self.stacked_layout)
        self.stacked_layout.addWidget(detail_window)
        self.stacked_layout.setCurrentWidget(detail_window)

    def logout(self):
        # TODO: Добавить логику выхода из профиля.
        pass