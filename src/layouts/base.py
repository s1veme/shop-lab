from typing import Callable

from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy


class BaseWindow:
    def init_header(self, logout_method: Callable) -> QHBoxLayout:
        header_layout = QHBoxLayout()

        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        header_layout.addItem(spacer)

        logout_button = QPushButton('Выход')
        logout_button.clicked.connect(logout_method)
        logout_button.setMaximumWidth(100)
        header_layout.addWidget(logout_button)

        return header_layout

    def init_footer(self) -> QHBoxLayout:
        footer_layout = QHBoxLayout()

        return footer_layout
