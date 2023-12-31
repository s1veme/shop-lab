import logging
from typing import Callable

import httpx
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QSizePolicy,
    QStackedLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QWidget,
    QScrollArea,
)
from PyQt6.QtGui import QPixmap

from core.settings import BASE_URL, HEIGHT, WIDTH
from layouts.base import BaseWindow
from layouts.order import OrderWindow
from layouts.product import ProductDetailWindow
from models.product import Product


logger = logging.getLogger(__name__)


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
        name_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(name_label)

        description = product.description
        if len(product.description) > 20:
            description = f'{product.description[:20]}...'

        description_label = QLabel(description)
        layout.addWidget(description_label)

        price_label = QLabel(str(product.price) + '₽')
        price_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(price_label)

        image_label = QLabel()
        image = QPixmap()
        image.loadFromData(httpx.get(product.image).content)
        image = image.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        image_label.setPixmap(image)
        image_label.setStyleSheet("border-radius: 10px;")
        layout.addWidget(image_label)

        buy_button = QPushButton('Купить')
        buy_button.clicked.connect(self.create_order)
        layout.addWidget(buy_button)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setMaximumWidth(320)
        self.setStyleSheet("margin: 5px; padding: 10px; background-color: #000; border-radius: 20%;")
        self.setLayout(layout)

    def create_order(self, event):
        order_window = OrderWindow(self.product, self.stacked_layout)
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

        self.addToolBar(self.init_header())

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        search_layout = QHBoxLayout()
        search_layout.addWidget(spacer)

        search_input = QLineEdit()
        self.search_input = search_input
        search_input.setPlaceholderText('Поиск')
        search_layout.addWidget(search_input)

        search_button = QPushButton('Найти')
        search_button.clicked.connect(self.search_products)
        search_layout.addWidget(search_button)

        self.main_layout.addLayout(search_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area_widget = QWidget()
        self.catalog_layout = QGridLayout(self.scroll_area_widget)
        self.catalog_layout.setHorizontalSpacing(10)
        self.catalog_layout.setVerticalSpacing(10)
        self.catalog_layout.setColumnMinimumWidth(0, 200)

        self.populate_catalog(self.fetch_products())

        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.main_layout.addWidget(self.scroll_area)

        self.main_layout.addLayout(self.init_footer())

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def populate_catalog(self, products: list[dict]):
        for i in reversed(range(self.catalog_layout.count())):
            item = self.catalog_layout.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)

        for index, product in enumerate(products):
            card = Product(**product)
            product_card = ProductCard(
                card,
                lambda event: self.on_product_clicked(event, card),
                self.stacked_layout,
            )
            row, col = divmod(index, 4)
            self.catalog_layout.addWidget(product_card, row, col)

    def fetch_products(self, url: str | None = None):
        if not url:
            url = f'{BASE_URL}/api/v1/products'

        try:
            with httpx.Client(follow_redirects=True) as client:
                response = client.get(url)
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            logger.error(f'Failed to fetch products. Error: {e}')
            return []

    def search_products(self):
        search_query = self.search_input.text()
        if search_query:
            search_url = f'{BASE_URL}/api/v1/products/?search={search_query}'
            search_results = self.fetch_products(url=search_url)
            self.populate_catalog(products=search_results)
            return

        self.populate_catalog(products=self.fetch_products())

    def on_product_clicked(self, event, product):
        detail_window = ProductDetailWindow(product, self.stacked_layout)
        self.stacked_layout.addWidget(detail_window)
        self.stacked_layout.setCurrentWidget(detail_window)
