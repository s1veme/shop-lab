from typing import Callable

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton


class BaseWindow:
    def init_header(self, logout_method: Callable) -> QHBoxLayout:
        header_layout = QHBoxLayout()

        logout_button = QPushButton('Выход')
        logout_button.clicked.connect(logout_method)
        logout_button.setMaximumWidth(100)
        header_layout.addWidget(logout_button)

        return header_layout

    def init_footer(self) -> QHBoxLayout:
        footer_layout = QHBoxLayout()

        return footer_layout
