from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QCheckBox, QGroupBox, QScrollArea, QApplication, QLineEdit
)
from PyQt5.QtCore import Qt
from front.logica import LogicaPerfiles

class VentanaHermosa(QWidget):
    def __init__(self, datos):
        super().__init__()
        self.datos = datos
        self.activos = {}
        self.logica = None
        self.checkboxes = {}
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Perfiles")
        self.resize(380, 600)
        self.setMinimumSize(320, 450)
        
        # Estilo minimalista tipo Apple (macOS)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f7;
                color: #1d1d1f;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }
            QLabel#title {
                font-size: 26px;
                font-weight: 700;
                color: #1d1d1f;
                padding-bottom: 5px;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #d2d2d7;
                border-radius: 10px;
                padding: 10px 14px;
                font-size: 14px;
                color: #1d1d1f;
            }
            QLineEdit:focus {
                border: 1px solid #007aff;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QGroupBox {
                background-color: #ffffff;
                border: 1px solid #e5e5ea;
                border-radius: 12px;
                margin-top: 24px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                color: #86868b;
                font-size: 12px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            QCheckBox {
                font-size: 14px;
                color: #1d1d1f;
                padding: 8px 0;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1px solid #c7c7cc;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QCheckBox::indicator:checked {
                background-color: #007aff;
                border: 1px solid #007aff;
            }
            QPushButton {
                background-color: #007aff;
                color: #ffffff;
                border: none;
                border-radius: 12px;
                padding: 14px;
                font-size: 15px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #006ae6;
            }
            QPushButton:pressed {
                background-color: #005ecb;
            }
            QPushButton:disabled {
                background-color: #a1a1a6;
                color: #f5f5f7;
            }
            QPushButton#secondary {
                background-color: #e5e5ea;
                color: #007aff;
                padding: 10px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton#secondary:hover {
                background-color: #d1d1d6;
            }
            QLabel#status {
                font-size: 12px;
                color: #86868b;
                padding-top: 8px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 32, 24, 24)
        main_layout.setSpacing(16)

        title = QLabel("Perfiles")
        title.setObjectName("title")
        main_layout.addWidget(title)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar...")
        self.search_input.textChanged.connect(self.filtrar_perfiles)
        main_layout.addWidget(self.search_input)

        profile_scroll = QScrollArea()
        profile_scroll.setWidgetResizable(True)
        
        scroll_container = QWidget()
        scroll_container.setStyleSheet("background-color: transparent;")
        scroll_layout = QVBoxLayout(scroll_container)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(12)

        for navegador, perfiles in self.datos.items():
            if not perfiles:
                continue
            group = QGroupBox(f"{navegador}")
            group_layout = QVBoxLayout()
            group_layout.setContentsMargins(16, 12, 16, 16)
            group_layout.setSpacing(0)

            self.checkboxes[navegador] = []
            for perfil in perfiles:
                check = QCheckBox(perfil)
                group_layout.addWidget(check)
                self.checkboxes[navegador].append(check)

            group.setLayout(group_layout)
            scroll_layout.addWidget(group)

        scroll_layout.addStretch()
        profile_scroll.setWidget(scroll_container)
        main_layout.addWidget(profile_scroll)

        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)
        
        self.select_all_button = QPushButton("Seleccionar todo")
        self.select_all_button.setObjectName("secondary")
        self.select_all_button.clicked.connect(self.seleccionar_todo)
        
        self.clear_button = QPushButton("Limpiar")
        self.clear_button.setObjectName("secondary")
        self.clear_button.clicked.connect(self.deseleccionar_todo)
        
        actions_layout.addWidget(self.select_all_button)
        actions_layout.addWidget(self.clear_button)
        
        main_layout.addLayout(actions_layout)

        self.open_button = QPushButton("Abrir Seleccionados")
        self.open_button.clicked.connect(self.abrir_perfiles)
        main_layout.addWidget(self.open_button)

        self.status_label = QLabel("Listo")
        self.status_label.setObjectName("status")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

    def seleccionar_todo(self):
        for checks in self.checkboxes.values():
            for check in checks:
                check.setChecked(True)
        self.actualizar_estadisticas()

    def deseleccionar_todo(self):
        for checks in self.checkboxes.values():
            for check in checks:
                check.setChecked(False)
        self.actualizar_estadisticas()

    def filtrar_perfiles(self, texto):
        texto = texto.lower()
        for navegador, checks in self.checkboxes.items():
            for check in checks:
                visible = texto in check.text().lower() or texto in navegador.lower()
                check.setVisible(visible)

    def abrir_perfiles(self):
        self.activos = {}
        for navegador, checks in self.checkboxes.items():
            self.activos[navegador] = [check.text() for check in checks if check.isChecked()]

        if any(self.activos.values()):
            self.open_button.setEnabled(False)
            self.status_label.setText("Abriendo perfiles...")

            self.logica = LogicaPerfiles(self.activos)
            self.logica.progreso_signal.connect(self.actualizar_progreso)
            self.logica.terminado_signal.connect(self.terminado)
            self.logica.start()
        else:
            self.status_label.setText("Selecciona al menos un perfil")

    def actualizar_estadisticas(self):
        seleccionados = sum(check.isChecked() for checks in self.checkboxes.values() for check in checks)
        if seleccionados > 0:
            self.status_label.setText(f"{seleccionados} seleccionados")
        else:
            self.status_label.setText("Listo")

    def actualizar_progreso(self, mensaje):
        self.status_label.setText(mensaje)

    def terminado(self, mensaje):
        self.status_label.setText("Completado")
        self.open_button.setEnabled(True)

def seleccionar_perfiles(datos):
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    ventana = VentanaHermosa(datos)
    ventana.show()
    app.exec_()
