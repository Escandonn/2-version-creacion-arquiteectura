# ventana.py

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout
)


class VentanaPrincipal(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema")
        self.setGeometry(100, 100, 1000, 1000)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.tabla)

        self.setLayout(self.layout)