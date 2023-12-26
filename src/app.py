import http
import logging
import sys

import httpx
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QStackedLayout, QWidget
from qt_material import apply_stylesheet

from core.settings import BASE_URL, HEIGHT, WIDTH, WORK_DIR
from layouts.catalog import ProductCatalogWindow
from layouts.login import LoginWindow
from services.api import APIService

logger = logging.getLogger(__name__)


def main():
    APIService(BASE_URL)

    with httpx.Client(follow_redirects=True) as client:
        response = client.get(f'{BASE_URL}/api/common/health')
        if response.status_code != http.HTTPStatus.OK:
            logger.error('the backend is not available')
            return

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(WORK_DIR / 'assets/logo.png')))

    apply_stylesheet(app, theme='dark_amber.xml')

    stacked_layout = QStackedLayout()

    catalog_window = ProductCatalogWindow(stacked_layout)
    login_window = LoginWindow(stacked_layout)

    stacked_layout.addWidget(login_window)
    stacked_layout.addWidget(catalog_window)

    main_widget = QWidget()
    main_widget.setGeometry(100, 100, WIDTH, HEIGHT)
    main_widget.setLayout(stacked_layout)
    main_widget.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
