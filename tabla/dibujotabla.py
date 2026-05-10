# tabla/dibujotabla.py

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)


class DibujoTabla(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.crear_tabla()

        self.setLayout(self.layout)

    def crear_tabla(self):

        self.tabla = QTableWidget()

        # columnas
        columnas = [
            "id",
            "nombre",
            "navegador",
            "texto",
            "personalidad",
            "historia",
            "chat",
            "activo"
        ]

        self.tabla.setColumnCount(len(columnas))
        self.tabla.setHorizontalHeaderLabels(columnas)

        # ejemplo filas
        self.tabla.setRowCount(3)

        datos = [
            ["1", "Carlos", "Chrome", "Hola", "Serio", "Historia 1", "Chat 1", "True"],
            ["2", "Ana", "Firefox", "Mensaje", "Alegre", "Historia 2", "Chat 2", "False"],
            ["3", "Luis", "Edge", "Texto", "Neutral", "Historia 3", "Chat 3", "True"]
        ]

        for fila, contenido in enumerate(datos):

            for columna, valor in enumerate(contenido):

                item = QTableWidgetItem(valor)

                self.tabla.setItem(fila, columna, item)

        # diseño tabla
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.tabla.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                color: white;
                gridline-color: #444;
                font-size: 14px;
            }

            QHeaderView::section {
                background-color: #333;
                color: white;
                padding: 8px;
                border: 1px solid #444;
                font-weight: bold;
            }
        """)

        self.layout.addWidget(self.tabla)