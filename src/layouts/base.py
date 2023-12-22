from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QStackedLayout,
    QToolBar,
    QWidget,
)

from models.user import ActiveUser


class BaseWindow:
    stacked_layout: QStackedLayout

    def init_header(self):
        toolbar = QToolBar('Main Toolbar')

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        toolbar.addWidget(spacer)

        logout_action = toolbar.addAction('Выход')
        logout_action.triggered.connect(self.logout)

        return_to_catalog_action = toolbar.addAction('Вернуться в каталог')
        return_to_catalog_action.triggered.connect(self.return_to_catalog)

        return toolbar

    def init_footer(self) -> QHBoxLayout:
        footer_layout = QHBoxLayout()

        return footer_layout

    def logout(self):
        user = ActiveUser()
        del user
        self.stacked_layout.setCurrentIndex(0)
        QMessageBox.information(self, 'Успешно!', 'Вы успешно вышли из аккаунта!')

    def return_to_catalog(self):
        self.stacked_layout.setCurrentIndex(1)
