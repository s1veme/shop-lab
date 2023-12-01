import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from qt_material import apply_stylesheet

from core.settings import WORK_DIR
from layouts.catalog import ProductCatalogWindow
from layouts.login import LoginWindow
from layouts.product import ProductDetailWindow
from mocks.products import MOCK_PRODUCTS_DATA
from models.product import Product

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(str(WORK_DIR / 'assets/logo.png')))

apply_stylesheet(app, theme='dark_blue.xml')

login_window = LoginWindow()
login_window.show()

catalog_window = ProductCatalogWindow()
catalog_window.show()

product_windows = ProductDetailWindow(Product(**MOCK_PRODUCTS_DATA[0]))
product_windows.show()

sys.exit(app.exec())
