import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QStackedLayout, QWidget
from qt_material import apply_stylesheet

from core.settings import HEIGHT, WIDTH, WORK_DIR
from layouts.catalog import ProductCatalogWindow

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(str(WORK_DIR / 'assets/logo.png')))

apply_stylesheet(app, theme='dark_blue.xml')

stacked_layout = QStackedLayout()

catalog_window = ProductCatalogWindow(stacked_layout)
stacked_layout.addWidget(catalog_window)

main_widget = QWidget()
main_widget.setGeometry(100, 100, WIDTH, HEIGHT)
main_widget.setLayout(stacked_layout)
main_widget.show()

sys.exit(app.exec())
