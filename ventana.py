# ventana.py

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)

from PyQt5.QtCore import Qt


class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mi Ventana PyQt5")
        self.setGeometry(100, 100, 1000, 1000)

        self.inicializar_ui()

    def inicializar_ui(self):

        layout = QVBoxLayout()

        titulo = QLabel("Ventana 1000 x 1000")
        titulo.setAlignment(Qt.AlignCenter)

        titulo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        layout.addWidget(titulo)

        self.setLayout(layout)