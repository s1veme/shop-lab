from typing import Callable

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton


class BaseWindow:
    def init_header(self, logout_method: Callable) -> QHBoxLayout:
        header_layout = QHBoxLayout()

        logo_label = QLabel()
        logo_label.setPixmap(QPixmap("путь_к_вашему_логотипу.png"))
        header_layout.addWidget(logo_label)

        products_button = QLabel("<a href=\"#\">Все товары</a>")
        products_button.setOpenExternalLinks(True)
        header_layout.addWidget(products_button)

        logout_button = QPushButton("Выход")
        logout_button.clicked.connect(logout_method)
        logout_button.setMaximumWidth(100)
        header_layout.addWidget(logout_button)

        return header_layout

    def init_footer(self) -> QHBoxLayout:
        ...
