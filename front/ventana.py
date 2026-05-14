from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QCheckBox, QGroupBox, QScrollArea, QFrame, QApplication,
    QProgressBar, QTextEdit, QLineEdit, QCalendarWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
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
        self.setWindowTitle("✨ SeleniumBase Dashboard")
        screen = QApplication.primaryScreen()
        if screen:
            available = screen.availableGeometry()
            width = min(1340, max(900, available.width() - 80))
            height = min(860, max(660, available.height() - 80))
            self.resize(width, height)
            self.move(available.left() + 20, available.top() + 20)
        else:
            self.resize(1260, 760)
        self.setMinimumSize(980, 700)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #eef2ff, stop:1 #dbeafe);
                color: #0f172a;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QFrame#panel {
                background: rgba(255, 255, 255, 0.92);
                border: 1px solid rgba(148, 163, 184, 0.18);
                border-radius: 24px;
            }
            QLabel#title {
                color: #0f172a;
                font-size: 28px;
                font-weight: 800;
            }
            QLabel#subtitle {
                color: #475569;
                font-size: 14px;
            }
            QLabel#metricTitle {
                color: #64748b;
                font-size: 12px;
            }
            QLabel#metricValue {
                color: #0f172a;
                font-size: 26px;
                font-weight: 700;
            }
            QGroupBox {
                border: none;
                border-radius: 20px;
                margin-top: 24px;
                padding: 18px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,0.95), stop:1 rgba(226,232,240,0.95));
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 18px;
                padding: 0 6px;
                color: #334155;
                font-size: 14px;
                font-weight: 700;
            }
            QCheckBox {
                font-size: 13px;
                color: #0f172a;
                padding: 6px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #60a5fa;
                border-radius: 5px;
                background: white;
            }
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #60a5fa, stop:1 #38bdf8);
                border: 2px solid #2563eb;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2563eb, stop:1 #38bdf8);
                color: white;
                border: none;
                border-radius: 14px;
                padding: 12px 22px;
                font-size: 13px;
                font-weight: 700;
                min-width: 140px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3b82f6, stop:1 #60a5fa);
            }
            QPushButton:pressed {
                background: #1d4ed8;
            }
            QPushButton:disabled {
                background: #9ca3af;
                color: #e2e8f0;
            }
            QLineEdit {
                background: white;
                border: 1px solid #cbd5e1;
                border-radius: 14px;
                padding: 10px 14px;
                color: #0f172a;
                font-size: 13px;
            }
            QTextEdit {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                color: #0f172a;
                font-family: 'Consolas', monospace;
                font-size: 13px;
            }
            QProgressBar {
                border: 1px solid #cbd5e1;
                border-radius: 10px;
                background: #f8fafc;
                height: 18px;
                text-align: center;
                color: #0f172a;
            }
            QProgressBar::chunk {
                border-radius: 10px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #38bdf8, stop:1 #0284c7);
            }
            QCalendarWidget QWidget {
                alternate-background-color: transparent;
                background: transparent;
            }
            QCalendarWidget QAbstractItemView {
                selection-background-color: #38bdf8;
                selection-color: white;
                color: #0f172a;
                background: white;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        header = QFrame()
        header.setObjectName("panel")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 24, 24, 24)
        header_layout.setSpacing(14)

        title_box = QVBoxLayout()
        title_label = QLabel("SeleniumBase Dashboard")
        title_label.setObjectName("title")
        subtitle_label = QLabel("Interfaz moderna para administrar perfiles y lanzar sesiones de navegador.")
        subtitle_label.setObjectName("subtitle")
        title_box.addWidget(title_label)
        title_box.addWidget(subtitle_label)
        header_layout.addLayout(title_box)
        header_layout.addStretch()

        badge = QLabel("⚡ Control Central")
        badge.setStyleSheet("background: #eff6ff; color: #1e3a8a; border-radius: 14px; padding: 10px 16px;")
        header_layout.addWidget(badge)

        main_layout.addWidget(header)

        body_layout = QHBoxLayout()
        body_layout.setSpacing(16)

        left_panel = QFrame()
        left_panel.setObjectName("panel")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(22, 22, 22, 22)
        left_layout.setSpacing(18)

        left_title = QLabel("Perfiles disponibles")
        left_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #0f172a;")
        left_layout.addWidget(left_title)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar perfil o navegador...")
        self.search_input.textChanged.connect(self.filtrar_perfiles)
        left_layout.addWidget(self.search_input)

        profile_scroll = QScrollArea()
        profile_scroll.setWidgetResizable(True)
        profile_scroll.setStyleSheet("QScrollArea { border: none; }")
        profile_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        scroll_container = QWidget()
        scroll_layout = QVBoxLayout(scroll_container)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(12)

        for navegador, perfiles in self.datos.items():
            group = QGroupBox(f"{navegador.upper()} - {len(perfiles)} perfiles")
            group_layout = QVBoxLayout()
            group_layout.setSpacing(8)

            self.checkboxes[navegador] = []
            for perfil in perfiles:
                check = QCheckBox(perfil)
                group_layout.addWidget(check)
                self.checkboxes[navegador].append(check)

            group.setLayout(group_layout)
            scroll_layout.addWidget(group)

        scroll_layout.addStretch()
        profile_scroll.setWidget(scroll_container)
        left_layout.addWidget(profile_scroll)

        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)

        self.open_button = QPushButton("Abrir Seleccionados")
        self.open_button.clicked.connect(self.abrir_perfiles)
        actions_layout.addWidget(self.open_button)

        self.select_all_button = QPushButton("Seleccionar todo")
        self.select_all_button.clicked.connect(self.seleccionar_todo)
        actions_layout.addWidget(self.select_all_button)

        left_layout.addLayout(actions_layout)

        clear_layout = QHBoxLayout()
        clear_layout.setSpacing(10)
        self.clear_button = QPushButton("Deseleccionar")
        self.clear_button.clicked.connect(self.deseleccionar_todo)
        clear_layout.addWidget(self.clear_button)
        left_layout.addLayout(clear_layout)

        left_panel.setMinimumWidth(380)
        left_panel.setMaximumWidth(450)
        body_layout.addWidget(left_panel)

        right_panel = QVBoxLayout()
        right_panel.setSpacing(16)

        card_row = QFrame()
        card_row.setObjectName("panel")
        card_layout = QHBoxLayout(card_row)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(14)

        card_layout.addWidget(self.crear_tarjeta("Perfiles totales", str(self.contar_perfiles()), "#2563eb"))
        card_layout.addWidget(self.crear_tarjeta("Navegadores", str(len(self.datos)), "#10b981"))
        card_layout.addWidget(self.crear_tarjeta("Estado", "Listo para ejecutar", "#f59e0b"))

        right_panel.addWidget(card_row)

        analytics_card = QGroupBox("Analítica rápida")
        analytics_layout = QHBoxLayout(analytics_card)
        analytics_layout.setSpacing(12)

        stats_panel = QFrame()
        stats_panel.setStyleSheet("background: white; border-radius: 18px;")
        stats_layout = QVBoxLayout(stats_panel)
        stats_layout.setContentsMargins(18, 18, 18, 18)
        stats_layout.setSpacing(14)

        stats_layout.addWidget(self.crear_metric("Usuarios activos", "1.472", "#2563eb"))
        stats_layout.addWidget(self.crear_metric("Alertas totales", "5.472", "#0ea5e9"))
        stats_layout.addWidget(self.crear_metric("Interacción", "+2.6%", "#10b981"))

        analytics_layout.addWidget(stats_panel, 2)

        chart_panel = QFrame()
        chart_panel.setStyleSheet("background: white; border-radius: 18px;")
        chart_layout = QVBoxLayout(chart_panel)
        chart_layout.setContentsMargins(18, 18, 18, 18)
        chart_layout.setSpacing(10)

        chart_title = QLabel("Tendencia de actividad")
        chart_title.setStyleSheet("font-size: 14px; font-weight: 700; color: #0f172a;")
        chart_layout.addWidget(chart_title)
        chart_layout.addWidget(self.crear_chart_placeholder())

        analytics_layout.addWidget(chart_panel, 3)
        right_panel.addWidget(analytics_card)

        detail_row = QHBoxLayout()
        detail_row.setSpacing(16)

        calendar_box = QGroupBox("Calendario")
        calendar_layout = QVBoxLayout(calendar_box)
        calendar_widget = QCalendarWidget()
        calendar_layout.addWidget(calendar_widget)
        detail_row.addWidget(calendar_box, 1)

        status_box = QGroupBox("Estado de ejecución")
        status_layout = QVBoxLayout(status_box)
        status_layout.setSpacing(12)
        status_label = QLabel("Control y registro de los eventos recientes del dashboard.")
        status_label.setWordWrap(True)
        status_layout.addWidget(status_label)
        status_layout.addWidget(self.crear_metric_line("Perfiles seleccionados", "0"))
        status_layout.addWidget(self.crear_metric_line("Última acción", "Esperando"))
        detail_row.addWidget(status_box, 1)

        right_panel.addLayout(detail_row)

        log_card = QGroupBox("Registro de ejecución")
        log_layout = QVBoxLayout(log_card)
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setPlainText("Log de ejecución:\n")
        log_layout.addWidget(self.log_area)

        footer_status = QHBoxLayout()
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setTextVisible(False)
        self.status_label = QLabel("Estado: Esperando selección...")
        self.status_label.setStyleSheet("color: #334155; font-weight: 700;")
        footer_status.addWidget(self.progress, 3)
        footer_status.addWidget(self.status_label, 4)
        log_layout.addLayout(footer_status)

        right_panel.addWidget(log_card, 1)

        body_layout.addLayout(right_panel, 1)
        main_layout.addLayout(body_layout)

    def crear_tarjeta(self, titulo, valor, color):
        tarjeta = QFrame()
        tarjeta.setStyleSheet(
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, "
            f"stop:0 {color}30, stop:1 #ffffff); border-radius: 20px;"
        )
        tarjeta_layout = QVBoxLayout(tarjeta)
        tarjeta_layout.setContentsMargins(18, 18, 18, 18)
        tarjeta_layout.setSpacing(10)

        label_title = QLabel(titulo)
        label_title.setObjectName("metricTitle")
        label_value = QLabel(valor)
        label_value.setObjectName("metricValue")

        tarjeta_layout.addWidget(label_title)
        tarjeta_layout.addWidget(label_value)
        tarjeta_layout.addStretch()
        return tarjeta

    def crear_metric(self, titulo, valor, color):
        metric_frame = QFrame()
        metric_layout = QHBoxLayout(metric_frame)
        metric_layout.setContentsMargins(12, 10, 12, 10)
        metric_layout.setSpacing(12)
        metric_frame.setStyleSheet("background: #f8fafc; border-radius: 16px;")

        label = QLabel(titulo)
        label.setStyleSheet("color: #475569; font-size: 13px;")
        value = QLabel(valor)
        value.setStyleSheet(f"color: {color}; font-size: 18px; font-weight: 700;")
        value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        metric_layout.addWidget(label)
        metric_layout.addWidget(value)
        return metric_frame

    def crear_chart_placeholder(self):
        placeholder = QFrame()
        placeholder.setMinimumHeight(150)
        placeholder.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, "
            "stop:0 #e0f2fe, stop:1 #ffffff); border: 1px solid #cbd5e1; border-radius: 18px;"
        )
        return placeholder

    def crear_metric_line(self, etiqueta, valor):
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)
        frame.setStyleSheet("background: #f8fafc; border-radius: 14px;")

        label = QLabel(etiqueta)
        label.setStyleSheet("color: #475569; font-size: 13px;")
        value = QLabel(valor)
        value.setStyleSheet("color: #0f172a; font-weight: 700; font-size: 13px;")
        value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout.addWidget(label)
        layout.addWidget(value)
        return frame

    def contar_perfiles(self):
        return sum(len(perfiles) for perfiles in self.datos.values())

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
            self.progress.setVisible(True)
            self.progress.setRange(0, 0)
            self.status_label.setText("🔄 Abriendo perfiles seleccionados...")
            self.log_area.append("Iniciando apertura de perfiles...")

            self.logica = LogicaPerfiles(self.activos)
            self.logica.progreso_signal.connect(self.actualizar_progreso)
            self.logica.terminado_signal.connect(self.terminado)
            self.logica.start()
        else:
            self.status_label.setText("❌ Selecciona al menos un perfil")
            self.log_area.append("Error: No se seleccionaron perfiles")

    def actualizar_estadisticas(self):
        seleccionados = sum(check.isChecked() for checks in self.checkboxes.values() for check in checks)
        self.status_label.setText(f"🧭 {seleccionados} perfiles seleccionados")

    def actualizar_progreso(self, mensaje):
        self.status_label.setText(f"🔄 {mensaje}")
        self.log_area.append(mensaje)

    def terminado(self, mensaje):
        self.status_label.setText(f"✅ {mensaje}")
        self.progress.setVisible(False)
        self.open_button.setEnabled(True)
        self.log_area.append(mensaje)


def seleccionar_perfiles(datos):
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    ventana = VentanaHermosa(datos)
    ventana.show()
    app.exec_()
