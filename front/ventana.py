from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QCheckBox, QGroupBox, QScrollArea, QFrame, QApplication,
    QProgressBar, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from front.logica import LogicaPerfiles


class VentanaHermosa(QWidget):

    def __init__(self, datos):
        super().__init__()
        self.datos = datos
        self.activos = {}
        self.logica = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("🚀 Multi-Perfil SeleniumBase Pro")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2c3e50, stop:1 #34495e);
                color: white;
                font-family: 'Segoe UI', Arial;
            }
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 5px;
                margin-top: 1ex;
                background: rgba(52, 73, 94, 0.8);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #ecf0f1;
            }
            QCheckBox {
                font-size: 12px;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                color: white;
                min-width: 150px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
            }
            QPushButton:pressed {
                background: #21618c;
            }
            QPushButton:disabled {
                background: #7f8c8d;
            }
            QLabel {
                font-size: 12px;
            }
            QProgressBar {
                border: 2px solid #3498db;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #27ae60, stop:1 #2ecc71);
            }
            QTextEdit {
                background: rgba(44, 62, 80, 0.9);
                border: 1px solid #3498db;
                border-radius: 5px;
                color: #ecf0f1;
                font-family: 'Consolas', monospace;
            }
        """)

        layout_principal = QVBoxLayout()

        # Header
        header = QLabel("🎯 Sistema Multi-Perfil SeleniumBase")
        header.setFont(QFont("Arial", 18, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #ecf0f1; margin: 20px;")
        layout_principal.addWidget(header)

        # Scroll area for profiles
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        widget_contenido = QWidget()
        layout_contenido = QVBoxLayout()

        self.checkboxes = {}
        for navegador, perfiles in self.datos.items():
            grupo = QGroupBox(f"🌐 {navegador.upper()} ({len(perfiles)} perfiles)")
            layout_grupo = QVBoxLayout()

            self.checkboxes[navegador] = []
            for perfil in perfiles:
                check = QCheckBox(f"📁 {perfil}")
                layout_grupo.addWidget(check)
                self.checkboxes[navegador].append(check)

            grupo.setLayout(layout_grupo)
            layout_contenido.addWidget(grupo)

        widget_contenido.setLayout(layout_contenido)
        scroll.setWidget(widget_contenido)
        layout_principal.addWidget(scroll)

        # Buttons
        layout_botones = QHBoxLayout()

        self.btn_abrir = QPushButton("🚀 Abrir Seleccionados")
        self.btn_abrir.clicked.connect(self.abrir_perfiles)
        layout_botones.addWidget(self.btn_abrir)

        self.btn_seleccionar_todo = QPushButton("✅ Seleccionar Todo")
        self.btn_seleccionar_todo.clicked.connect(self.seleccionar_todo)
        layout_botones.addWidget(self.btn_seleccionar_todo)

        self.btn_deseleccionar = QPushButton("❌ Deseleccionar Todo")
        self.btn_deseleccionar.clicked.connect(self.deseleccionar_todo)
        layout_botones.addWidget(self.btn_deseleccionar)

        layout_principal.addLayout(layout_botones)

        # Progress and status
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout_principal.addWidget(self.progress)

        self.status = QLabel("Estado: Esperando selección...")
        self.status.setStyleSheet("color: #f39c12; font-weight: bold;")
        layout_principal.addWidget(self.status)

        # Log area
        self.log_area = QTextEdit()
        self.log_area.setMaximumHeight(150)
        self.log_area.setPlainText("Log de ejecución:\n")
        layout_principal.addWidget(self.log_area)

        self.setLayout(layout_principal)

    def seleccionar_todo(self):
        for checks in self.checkboxes.values():
            for check in checks:
                check.setChecked(True)

    def deseleccionar_todo(self):
        for checks in self.checkboxes.values():
            for check in checks:
                check.setChecked(False)

    def abrir_perfiles(self):
        self.activos = {}
        for navegador, checks in self.checkboxes.items():
            self.activos[navegador] = [check.text().replace("📁 ", "") for check in checks if check.isChecked()]

        if any(self.activos.values()):
            self.btn_abrir.setEnabled(False)
            self.progress.setVisible(True)
            self.progress.setRange(0, 0)  # Indeterminate

            self.log_area.append("Iniciando apertura de perfiles...")

            self.logica = LogicaPerfiles(self.activos)
            self.logica.progreso_signal.connect(self.actualizar_progreso)
            self.logica.terminado_signal.connect(self.terminado)
            self.logica.start()
        else:
            self.status.setText("❌ Selecciona al menos un perfil")
            self.log_area.append("Error: No se seleccionaron perfiles")

    def actualizar_progreso(self, mensaje):
        self.status.setText(f"🔄 {mensaje}")
        self.log_area.append(mensaje)

    def terminado(self, mensaje):
        self.status.setText(f"✅ {mensaje}")
        self.progress.setVisible(False)
        self.btn_abrir.setEnabled(True)
        self.log_area.append(mensaje)


def seleccionar_perfiles(datos):
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    ventana = VentanaHermosa(datos)
    ventana.show()

    app.exec_()