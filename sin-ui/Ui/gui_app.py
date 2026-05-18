import os
import sys
import time
import threading
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QTextEdit,
    QComboBox, QDialog, QFormLayout, QMessageBox, QHeaderView, QGroupBox,
    QAbstractItemView, QCheckBox, QHBoxLayout
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot

# Importar capa de base de datos y utilidades existentes
from base_de_datos import db_manager
from carpeta_gestor import obtener_navegadores
from bot_sb import WhatsappBot

# ==============================================================================
# HILO DE CONTROL DE BOT (QTHREAD WORKER)
# ==============================================================================

class BotWorker(QThread):
    status_changed = pyqtSignal(str, str)  # id_sesion, nuevo_estado
    log_received = pyqtSignal(str, str)    # id_sesion, mensaje_log
    stats_updated = pyqtSignal()           # Señal para actualizar la tabla de estadísticas

    def __init__(self, navegador, perfil, user_data_dir):
        super().__init__()
        self.navegador = navegador
        self.perfil = perfil
        self.user_data_dir = user_data_dir
        self.id_sesion = f"{navegador}_{perfil}"
        self.bot = None

    def run(self):
        self.status_changed.emit(self.id_sesion, "CONECTANDO...")
        self.log_received.emit(self.id_sesion, "Iniciando WebDriver con uc=False...")
        
        # Instanciamos el bot de SeleniumBase
        self.bot = WhatsappBot(navegador=self.navegador, user_data_dir=self.user_data_dir)
        
        # Redirigimos el log del bot hacia la señal de PyQt5 mediante inyección de callback
        def gui_log_callback(msg):
            self.log_received.emit(self.id_sesion, msg)
            # Si el mensaje indica envío exitoso, emitimos señal para refrescar estadísticas en vivo
            if "enviado exitosamente" in msg or "Estadistica de mensaje" in msg:
                self.stats_updated.emit()

        self.bot.log_callback = gui_log_callback
        
        # Hilo de monitoreo para cambiar el estado visual de "CONECTANDO..." a "LISTO" cuando bot.ready sea True
        def monitorear_estado_ready():
            while self.bot and self.bot.is_running:
                if self.bot.ready:
                    self.status_changed.emit(self.id_sesion, "LISTO")
                    break
                time.sleep(0.5)

        threading.Thread(target=monitorear_estado_ready, daemon=True).start()

        try:
            self.bot.run()
        except Exception as e:
            self.log_received.emit(self.id_sesion, f"ERROR CRITICO: {e}")
            self.status_changed.emit(self.id_sesion, "ERROR")
        finally:
            self.status_changed.emit(self.id_sesion, "APAGADO")
            self.log_received.emit(self.id_sesion, "Navegador cerrado.")


# ==============================================================================
# DIÁLOGOS MODALES (CRUD FORMULARIES)
# ==============================================================================

class PerfilDialog(QDialog):
    def __init__(self, parent=None, perfil_datos=None):
        super().__init__(parent)
        self.perfil_datos = perfil_datos
        self.setWindowTitle("Registrar Perfil" if not perfil_datos else "Editar Perfil")
        self.resize(450, 300)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)
        layout.setSpacing(10)

        self.input_ruta = QLineEdit(self)
        self.input_ruta.setPlaceholderText("ej: perfiles/chrome/Profile 3")
        self.input_real = QLineEdit(self)
        self.input_real.setPlaceholderText("ej: Bot de Ventas")
        self.input_correo = QLineEdit(self)
        self.input_contrasena = QLineEdit(self)
        self.input_contrasena.setEchoMode(QLineEdit.Password)
        self.input_personalidad = QLineEdit(self)
        self.input_personalidad.setPlaceholderText("ej: Gracioso, Profesional")
        self.input_ia = QLineEdit(self)
        self.input_ia.setPlaceholderText("ej: GPT-4o, Claude-3.5")

        if self.perfil_datos:
            # Rellenar datos para edición
            self.input_ruta.setText(self.perfil_datos["nombre_profile"])
            self.input_ruta.setEnabled(False) # No permitir cambiar la ruta física directamente
            self.input_real.setText(self.perfil_datos["nombre_real_whatsapp"] or "")
            self.input_correo.setText(self.perfil_datos["correo"] or "")
            self.input_contrasena.setText(self.perfil_datos["contrasena"] or "")
            self.input_personalidad.setText(self.perfil_datos["personalidad"] or "")
            self.input_ia.setText(self.perfil_datos["ia"] or "")

        layout.addRow("Ruta de Perfil (Fisica):", self.input_ruta)
        layout.addRow("Nombre Real WhatsApp:", self.input_real)
        layout.addRow("Correo Electronico:", self.input_correo)
        layout.addRow("Contrasena:", self.input_contrasena)
        layout.addRow("Personalidad de IA:", self.input_personalidad)
        layout.addRow("Modelo de IA Flag:", self.input_ia)

        btn_box = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar", self)
        self.btn_guardar.clicked.connect(self.accept)
        self.btn_cancelar = QPushButton("Cancelar", self)
        self.btn_cancelar.clicked.connect(self.reject)
        
        btn_box.addWidget(self.btn_cancelar)
        btn_box.addWidget(self.btn_guardar)
        layout.addRow(btn_box)

    def obtener_valores(self):
        return {
            "nombre_profile": self.input_ruta.text().strip(),
            "nombre_real": self.input_real.text().strip() or None,
            "correo": self.input_correo.text().strip() or None,
            "contrasena": self.input_contrasena.text().strip() or None,
            "personalidad": self.input_personalidad.text().strip() or None,
            "ia": self.input_ia.text().strip() or None
        }


class GrupoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Grupo de WhatsApp")
        self.resize(350, 150)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)
        layout.setSpacing(10)

        self.input_nombre = QLineEdit(self)
        self.input_nombre.setPlaceholderText("Nombre exacto del grupo en WhatsApp Web")
        layout.addRow("Nombre de Grupo:", self.input_nombre)

        btn_box = QHBoxLayout()
        self.btn_guardar = QPushButton("Registrar", self)
        self.btn_guardar.clicked.connect(self.accept)
        self.btn_cancelar = QPushButton("Cancelar", self)
        self.btn_cancelar.clicked.connect(self.reject)
        
        btn_box.addWidget(self.btn_cancelar)
        btn_box.addWidget(self.btn_guardar)
        layout.addRow(btn_box)

    def obtener_nombre(self):
        return self.input_nombre.text().strip()


# ==============================================================================
# VENTANA PRINCIPAL (MAIN DASHBOARD WINDOW)
# ==============================================================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WhatsApp Multi-Perfil - Panel de Control & Estadisticas")
        self.resize(1100, 750)
        
        # Inicializar estructuras de control
        self.workers_activos = {}
        
        # Inicializar DB SQLite y sincronizar perfiles fisicos
        db_manager.inicializar_base_de_datos()
        perfiles_disco = obtener_navegadores()
        db_manager.sincronizar_perfiles_desde_disco(perfiles_disco)

        self.init_ui()
        self.aplicar_estilos_premium()

    def init_ui(self):
        # Widget Central y Tab Principal
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Título superior de alta gama
        self.lbl_titulo = QLabel("🤖 WHATSAPP AUTOMATION DASHBOARD", self)
        self.lbl_titulo.setObjectName("lbl_titulo")
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.lbl_titulo)

        self.tabs = QTabWidget(self)
        self.main_layout.addWidget(self.tabs)

        # Inicialización de las 4 pestañas interactivas
        self.init_tab_control()
        self.init_tab_perfiles()
        self.init_tab_grupos()
        self.init_tab_estadisticas()

        # Cargar datos iniciales en las tablas
        self.cargar_datos_control()
        self.cargar_datos_perfiles()
        self.cargar_datos_grupos()
        self.cargar_datos_estadisticas()

    # ==========================================================================
    # PESTAÑA 1: CONTROL Y EJECUCIÓN DE BOTS
    # ==========================================================================
    def init_tab_control(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Explicación
        lbl_info = QLabel("Selecciona los perfiles que deseas iniciar en paralelo. Una vez conectados (estado LISTO), podras enviarles comandos masivos.", self)
        layout.addWidget(lbl_info)

        # Tabla de Bots
        self.tabla_bots = QTableWidget(self)
        self.tabla_bots.setColumnCount(6)
        self.tabla_bots.setHorizontalHeaderLabels([
            "Seleccion", "ID", "Ruta de Perfil", "Nombre Visual", "IA", "Estado"
        ])
        self.tabla_bots.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_bots.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_bots.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.tabla_bots)

        # Fila de Botones de Lanzamiento
        btn_layout = QHBoxLayout()
        self.btn_lanzar = QPushButton("🚀 Lanzar Seleccionados en Paralelo", self)
        self.btn_lanzar.clicked.connect(self.lanzar_bots_seleccionados)
        self.btn_detener = QPushButton("🛑 Detener Todos los Bots Activos", self)
        self.btn_detener.clicked.connect(self.detener_todos_los_bots)
        
        btn_layout.addWidget(self.btn_lanzar)
        btn_layout.addWidget(self.btn_detener)
        layout.addLayout(btn_layout)

        # Caja de Menú Maestro (Comandos en Caliente)
        self.box_maestro = QGroupBox("Menú Maestro de Comandos (Global)", self)
        box_layout = QHBoxLayout(self.box_maestro)

        self.btn_entrar_grupos = QPushButton("1. Entrar a pestaña Grupos", self)
        self.btn_entrar_grupos.clicked.connect(self.cmd_entrar_grupos)
        self.btn_imprimir_titulos = QPushButton("2. Imprimir titulos de grupos", self)
        self.btn_imprimir_titulos.clicked.connect(self.cmd_imprimir_titulos)
        self.btn_envio_personalizado = QPushButton("3. Enviar Mensaje Dirigido (DB)", self)
        self.btn_envio_personalizado.clicked.connect(self.cmd_enviar_personalizado)
        self.btn_envio_masivo = QPushButton("4. Enviar Mensaje Comun Masivo", self)
        self.btn_envio_masivo.clicked.connect(self.cmd_enviar_masivo)

        box_layout.addWidget(self.btn_entrar_grupos)
        box_layout.addWidget(self.btn_imprimir_titulos)
        box_layout.addWidget(self.btn_envio_personalizado)
        box_layout.addWidget(self.btn_envio_masivo)
        layout.addWidget(self.box_maestro)

        # Terminal de Logs
        lbl_console = QLabel("Consola de Logs en Tiempo Real:", self)
        layout.addWidget(lbl_console)
        self.log_console = QTextEdit(self)
        self.log_console.setReadOnly(True)
        self.log_console.setObjectName("log_console")
        layout.addWidget(self.log_console)

        self.tabs.addTab(widget, "Control de Bots")

    # ==========================================================================
    # PESTAÑA 2: GESTIÓN DE PERFILES (CRUD)
    # ==========================================================================
    def init_tab_perfiles(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.tabla_perfiles = QTableWidget(self)
        self.tabla_perfiles.setColumnCount(6)
        self.tabla_perfiles.setHorizontalHeaderLabels([
            "ID", "Ruta de Perfil", "Nombre Visual", "Correo", "Personalidad IA", "Motor IA"
        ])
        self.tabla_perfiles.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_perfiles.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_perfiles.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.tabla_perfiles)

        btn_layout = QHBoxLayout()
        self.btn_add_perfil = QPushButton("[+] Agregar Perfil", self)
        self.btn_add_perfil.clicked.connect(self.agregar_perfil)
        self.btn_edit_perfil = QPushButton("[*] Editar Perfil Seleccionado", self)
        self.btn_edit_perfil.clicked.connect(self.editar_perfil)
        self.btn_del_perfil = QPushButton("[-] Eliminar Perfil Seleccionado", self)
        self.btn_del_perfil.clicked.connect(self.eliminar_perfil)

        btn_layout.addWidget(self.btn_add_perfil)
        btn_layout.addWidget(self.btn_edit_perfil)
        btn_layout.addWidget(self.btn_del_perfil)
        layout.addLayout(btn_layout)

        self.tabs.addTab(widget, "Administrar Perfiles")

    # ==========================================================================
    # PESTAÑA 3: GESTIÓN DE GRUPOS (CRUD)
    # ==========================================================================
    def init_tab_grupos(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.tabla_grupos = QTableWidget(self)
        self.tabla_grupos.setColumnCount(4)
        self.tabla_grupos.setHorizontalHeaderLabels([
            "ID", "Nombre de Grupo Oficial", "Ultimo Mensaje Enviado", "Fecha y Hora Envio"
        ])
        self.tabla_grupos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_grupos.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_grupos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.tabla_grupos)

        btn_layout = QHBoxLayout()
        self.btn_add_grupo = QPushButton("[+] Registrar Nuevo Grupo", self)
        self.btn_add_grupo.clicked.connect(self.agregar_grupo)
        self.btn_del_grupo = QPushButton("[-] Eliminar Grupo Seleccionado", self)
        self.btn_del_grupo.clicked.connect(self.eliminar_grupo)

        btn_layout.addWidget(self.btn_add_grupo)
        btn_layout.addWidget(self.btn_del_grupo)
        layout.addLayout(btn_layout)

        self.tabs.addTab(widget, "Administrar Grupos")

    # ==========================================================================
    # PESTAÑA 4: ASOCIACIONES Y ESTADÍSTICAS
    # ==========================================================================
    def init_tab_estadisticas(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # Panel Izquierdo: Formulario de Asociación
        self.box_asociar = QGroupBox("Vincular Perfil con Grupo (Many-to-Many)", self)
        box_layout = QFormLayout(self.box_asociar)
        box_layout.setSpacing(12)

        self.combo_perfiles = QComboBox(self)
        self.combo_grupos = QComboBox(self)
        self.btn_asociar = QPushButton("🔗 Crear Asociación", self)
        self.btn_asociar.clicked.connect(self.asociar_perfil_con_grupo)

        box_layout.addRow("Seleccionar Perfil:", self.combo_perfiles)
        box_layout.addRow("Seleccionar Grupo:", self.combo_grupos)
        box_layout.addRow("", self.btn_asociar)
        
        layout.addWidget(self.box_asociar, stretch=1)

        # Panel Derecho: Reporte Global de Estadísticas
        stats_box = QGroupBox("Estadisticas y Mensajes Enviados por Perfil", self)
        stats_layout = QVBoxLayout(stats_box)

        self.tabla_stats = QTableWidget(self)
        self.tabla_stats.setColumnCount(5)
        self.tabla_stats.setHorizontalHeaderLabels([
            "Perfil WhatsApp", "Grupo de Destino", "Mensajes", "Ultimo Mensaje", "Fecha de Actividad"
        ])
        self.tabla_stats.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_stats.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_stats.setEditTriggers(QAbstractItemView.NoEditTriggers)
        stats_layout.addWidget(self.tabla_stats)

        self.btn_refresh_stats = QPushButton("🔄 Actualizar Estadisticas", self)
        self.btn_refresh_stats.clicked.connect(self.cargar_datos_estadisticas)
        stats_layout.addWidget(self.btn_refresh_stats)

        layout.addWidget(stats_box, stretch=2)

        self.tabs.addTab(widget, "Asociaciones & Estadisticas")

    # ==========================================================================
    # CARGAR DATOS DESDE SQLITE HASTA LOS COMPONENTES
    # ==========================================================================
    def cargar_datos_control(self):
        perfiles = db_manager.obtener_perfiles()
        self.tabla_bots.setRowCount(len(perfiles))
        
        for row_idx, p in enumerate(perfiles):
            # Checkbox para seleccionar perfiles
            chk_box = QCheckBox(self)
            chk_box.setChecked(False)
            chk_widget = QWidget()
            chk_layout = QHBoxLayout(chk_widget)
            chk_layout.addWidget(chk_box)
            chk_layout.setAlignment(Qt.AlignCenter)
            chk_layout.setContentsMargins(0, 0, 0, 0)
            self.tabla_bots.setCellWidget(row_idx, 0, chk_widget)

            self.tabla_bots.setItem(row_idx, 1, QTableWidgetItem(str(p["id"])))
            self.tabla_bots.setItem(row_idx, 2, QTableWidgetItem(p["nombre_profile"]))
            self.tabla_bots.setItem(row_idx, 3, QTableWidgetItem(p["nombre_real_whatsapp"] or "N/A"))
            self.tabla_bots.setItem(row_idx, 4, QTableWidgetItem(p["ia"] or "Desactivada"))
            
            # Estado inicial
            ruta_perfil = p["nombre_profile"]
            partes = ruta_perfil.replace("\\", "/").split("/")
            navegador = partes[1] if len(partes) >= 3 else "chrome"
            perfil_nombre = partes[2] if len(partes) >= 3 else "Profile 1"
            id_sesion = f"{navegador}_{perfil_nombre}"
            
            estado = "APAGADO"
            if id_sesion in self.workers_activos:
                if self.workers_activos[id_sesion].isRunning():
                    estado = "LISTO" if getattr(self.workers_activos[id_sesion], "bot", None) and self.workers_activos[id_sesion].bot.ready else "CONECTANDO..."
            
            item_estado = QTableWidgetItem(estado)
            if estado == "LISTO":
                item_estado.setForeground(Qt.green)
            elif estado == "CONECTANDO...":
                item_estado.setForeground(Qt.yellow)
            else:
                item_estado.setForeground(Qt.gray)

            self.tabla_bots.setItem(row_idx, 5, item_estado)

    def cargar_datos_perfiles(self):
        perfiles = db_manager.obtener_perfiles()
        self.tabla_perfiles.setRowCount(len(perfiles))
        
        # Actualizar QComboBox del Tab 4
        self.combo_perfiles.clear()
        
        for row_idx, p in enumerate(perfiles):
            self.tabla_perfiles.setItem(row_idx, 0, QTableWidgetItem(str(p["id"])))
            self.tabla_perfiles.setItem(row_idx, 1, QTableWidgetItem(p["nombre_profile"]))
            self.tabla_perfiles.setItem(row_idx, 2, QTableWidgetItem(p["nombre_real_whatsapp"] or "N/A"))
            self.tabla_perfiles.setItem(row_idx, 3, QTableWidgetItem(p["correo"] or "N/A"))
            self.tabla_perfiles.setItem(row_idx, 4, QTableWidgetItem(p["personalidad"] or "Asistente"))
            self.tabla_perfiles.setItem(row_idx, 5, QTableWidgetItem(p["ia"] or "Desactivada"))

            # Añadir al combo de asociaciones
            self.combo_perfiles.addItem(f"{p['nombre_real_whatsapp']} ({p['nombre_profile']})", p["id"])

    def cargar_datos_grupos(self):
        grupos = db_manager.obtener_grupos()
        self.tabla_grupos.setRowCount(len(grupos))
        
        # Actualizar QComboBox del Tab 4
        self.combo_grupos.clear()

        for row_idx, g in enumerate(grupos):
            self.tabla_grupos.setItem(row_idx, 0, QTableWidgetItem(str(g["id"])))
            self.tabla_grupos.setItem(row_idx, 1, QTableWidgetItem(g["nombre"]))
            self.tabla_grupos.setItem(row_idx, 2, QTableWidgetItem(g["ultimo_mensaje"] or "Ninguno"))
            self.tabla_grupos.setItem(row_idx, 3, QTableWidgetItem(g["ultimo_mensaje_fecha"] or "Nunca"))

            # Añadir al combo de asociaciones
            self.combo_grupos.addItem(g["nombre"], g["id"])

    def cargar_datos_estadisticas(self):
        stats = db_manager.obtener_estadisticas_globales()
        self.tabla_stats.setRowCount(len(stats))
        
        for row_idx, s in enumerate(stats):
            self.tabla_stats.setItem(row_idx, 0, QTableWidgetItem(s["nombre_real_whatsapp"]))
            self.tabla_stats.setItem(row_idx, 1, QTableWidgetItem(s["nombre_grupo"]))
            self.tabla_stats.setItem(row_idx, 2, QTableWidgetItem(str(s["mensajes_enviados"])))
            self.tabla_stats.setItem(row_idx, 3, QTableWidgetItem(s["ultimo_mensaje_enviado"] or "N/A"))
            self.tabla_stats.setItem(row_idx, 4, QTableWidgetItem(s["ultimo_envio_fecha"] or "N/A"))

    # ==========================================================================
    # CONTROL DE BOTS Y HILOS (THREAD-SAFE AUTOMATION GATEWAY)
    # ==========================================================================
    def lanzar_bots_seleccionados(self):
        perfiles = db_manager.obtener_perfiles()
        lanzados = 0
        
        for idx in range(self.tabla_bots.rowCount()):
            # Obtener el CheckBox de la celda
            chk_widget = self.tabla_bots.cellWidget(idx, 0)
            if not chk_widget:
                continue
            chk_box = chk_widget.findChild(QCheckBox)
            if not chk_box or not chk_box.isChecked():
                continue

            perfil_sel = perfiles[idx]
            ruta = perfil_sel["nombre_profile"]
            
            partes = ruta.replace("\\", "/").split("/")
            navegador = partes[1] if len(partes) >= 3 else "chrome"
            perfil_nombre = partes[2] if len(partes) >= 3 else "Profile 1"
            id_sesion = f"{navegador}_{perfil_nombre}"

            if id_sesion in self.workers_activos and self.workers_activos[id_sesion].isRunning():
                self.escribir_log("SISTEMA", f"El bot '{id_sesion}' ya esta en ejecucion en segundo plano.")
                continue

            # Crear y lanzar Worker en QThread
            worker = BotWorker(navegador=navegador, perfil=perfil_nombre, user_data_dir=ruta)
            
            # Conectar señales
            worker.status_changed.connect(self.actualizar_estado_visual)
            worker.log_received.connect(self.escribir_log)
            worker.stats_updated.connect(self.cargar_datos_estadisticas) # Recargar stats al enviar mensajes
            
            self.workers_activos[id_sesion] = worker
            worker.start()
            lanzados += 1

        if lanzados == 0:
            QMessageBox.warning(self, "Advertencia", "Por favor selecciona al menos un perfil de la tabla marcando su casilla.")

    def detener_todos_los_bots(self):
        if not self.workers_activos:
            self.escribir_log("SISTEMA", "No hay ningun bot activo en ejecucion.")
            return

        self.escribir_log("SISTEMA", "Enviando comando de apagado a todos los bots activos...")
        for id_s, worker in list(self.workers_activos.items()):
            if worker.bot:
                worker.bot.is_running = False
        
        time.sleep(1)
        self.cargar_datos_control()

    @pyqtSlot(str, str)
    def actualizar_estado_visual(self, id_sesion, nuevo_estado):
        # Buscar en la tabla el perfil correspondiente
        for idx in range(self.tabla_bots.rowCount()):
            ruta = self.tabla_bots.item(idx, 2).text()
            partes = ruta.replace("\\", "/").split("/")
            naveg = partes[1] if len(partes) >= 3 else "chrome"
            perf = partes[2] if len(partes) >= 3 else "Profile 1"
            id_s = f"{naveg}_{perf}"

            if id_s == id_sesion:
                item_estado = QTableWidgetItem(nuevo_estado)
                if nuevo_estado == "LISTO":
                    item_estado.setForeground(Qt.green)
                elif nuevo_estado == "CONECTANDO...":
                    item_estado.setForeground(Qt.yellow)
                else:
                    item_estado.setForeground(Qt.gray)
                self.tabla_bots.setItem(idx, 5, item_estado)
                break

    @pyqtSlot(str, str)
    def escribir_log(self, id_sesion, mensaje):
        fecha = datetime.now().strftime("%H:%M:%S")
        log_str = f"[{fecha}] [{id_sesion}] {mensaje}"
        self.log_console.append(log_str)

    # ==========================================================================
    # MAESTRO DE COMANDOS - MÉTODOS DE ACCIÓN GRÁFICOS
    # ==============================================================================
    def obtener_bots_listos(self):
        ready_workers = []
        for id_s, worker in self.workers_activos.items():
            if worker.isRunning() and worker.bot and worker.bot.ready:
                ready_workers.append(worker.bot)
        return ready_workers

    def cmd_entrar_grupos(self):
        bots = self.obtener_bots_listos()
        if not bots:
            QMessageBox.information(self, "Aviso", "No hay ningun perfil de WhatsApp listo todavía (conecta perfiles y espera a que muestren el estado 'LISTO').")
            return

        self.escribir_log("COMANDO MAESTRO", "Ordenando a todos los bots entrar a la pestaña 'Grupos'...")
        for bot in bots:
            t = threading.Thread(target=bot.entrar_a_grupos, daemon=True)
            t.start()

    def cmd_imprimir_titulos(self):
        bots = self.obtener_bots_listos()
        if not bots:
            QMessageBox.information(self, "Aviso", "No hay ningun perfil de WhatsApp listo.")
            return

        self.escribir_log("COMANDO MAESTRO", "Ordenando a todos los bots imprimir los títulos de los grupos...")
        for bot in bots:
            t = threading.Thread(target=bot.obtener_titulos_grupos, daemon=True)
            t.start()

    def cmd_enviar_personalizado(self):
        bots = self.obtener_bots_listos()
        if not bots:
            QMessageBox.information(self, "Aviso", "No hay bots listos para ejecutar comandos.")
            return

        # Consultar asociaciones en la DB
        relaciones = db_manager.obtener_perfil_con_grupos()
        perfiles_db = db_manager.obtener_perfiles()
        
        self.escribir_log("COMANDO MAESTRO", "Enviando mensajes personalizados según asociaciones de la Base de Datos...")
        enviados = 0

        for bot in bots:
            # Buscar asociación para el perfil
            rel = next((r for r in relaciones if r["nombre_profile"] == bot.user_data_dir), None)
            if not rel or not rel["grupos_asociados"]:
                self.escribir_log(bot.user_data_dir, "ERROR: No tiene ningún grupo asociado en la base de datos.")
                continue

            # Tomar el primer grupo asociado
            grupos = [g.strip() for g in rel["grupos_asociados"].split(",")]
            grupo_destino = grupos[0]

            # Personalidad del bot
            personalidad = "Asistente"
            p_db = next((p for p in perfiles_db if p["nombre_profile"] == bot.user_data_dir), None)
            if p_db and p_db["personalidad"]:
                personalidad = p_db["personalidad"]

            mensaje = f"Hola, este es un mensaje automático de control. Personalidad: {personalidad}."

            # Ejecutar en hilo paralelo
            def job_personalizado(b=bot, g=grupo_destino, msg=mensaje):
                b.entrar_a_chat(g)
                time.sleep(2)
                b.escribir_y_enviar_mensaje(msg)

            threading.Thread(target=job_personalizado, daemon=True).start()
            enviados += 1

        if enviados == 0:
            QMessageBox.warning(self, "Error", "Ninguno de los perfiles listos tiene grupos asociados en la base de datos. Ve a la pestaña 'Asociaciones' y vinculalos primero.")

    def cmd_enviar_masivo(self):
        bots = self.obtener_bots_listos()
        if not bots:
            QMessageBox.information(self, "Aviso", "No hay bots listos para mensajería.")
            return

        # Pedir grupo y mensaje de manera gráfica
        dialog = QDialog(self)
        dialog.setWindowTitle("Enviar Mensaje Masivo Común")
        dialog.resize(400, 200)
        layout = QFormLayout(dialog)
        
        input_grupo = QLineEdit(dialog)
        input_grupo.setPlaceholderText("Nombre exacto del grupo")
        input_msg = QTextEdit(dialog)
        input_msg.setPlaceholderText("Mensaje común a enviar...")

        layout.addRow("Nombre de Grupo:", input_grupo)
        layout.addRow("Mensaje:", input_msg)

        btn_box = QHBoxLayout()
        btn_send = QPushButton("Enviar Masivo", dialog)
        btn_send.clicked.connect(dialog.accept)
        btn_cancel = QPushButton("Cancelar", dialog)
        btn_cancel.clicked.connect(dialog.reject)
        btn_box.addWidget(btn_cancel)
        btn_box.addWidget(btn_send)
        layout.addRow(btn_box)

        if dialog.exec() == QDialog.Accepted:
            grupo = input_grupo.text().strip()
            mensaje = input_msg.toPlainText().strip()

            if not grupo or not mensaje:
                QMessageBox.critical(self, "Error", "El grupo y el mensaje no pueden estar vacios.")
                return

            self.escribir_log("COMANDO MAESTRO", f"Iniciando envío masivo paralelo al grupo '{grupo}'...")
            for bot in bots:
                def job_masivo(b=bot, g=grupo, msg=mensaje):
                    b.entrar_a_chat(g)
                    time.sleep(2)
                    b.escribir_y_enviar_mensaje(msg)

                threading.Thread(target=job_masivo, daemon=True).start()

    # ==========================================================================
    # GESTION CRUD - METODOS OPERATIVOS
    # ==========================================================================
    def agregar_perfil(self):
        dialog = PerfilDialog(self)
        if dialog.exec() == QDialog.Accepted:
            datos = dialog.obtener_valores()
            if not datos["nombre_profile"]:
                return
            exito = db_manager.agregar_perfil(
                nombre_profile=datos["nombre_profile"],
                nombre_real=datos["nombre_real"],
                correo=datos["correo"],
                contrasena=datos["contrasena"],
                personalidad=datos["personalidad"],
                ia=datos["ia"]
            )
            if exito:
                QMessageBox.information(self, "Exito", "Perfil registrado correctamente.")
                self.cargar_datos_perfiles()
                self.cargar_datos_control()
            else:
                QMessageBox.critical(self, "Error", "El perfil ya existe o la ruta es invalida.")

    def editar_perfil(self):
        selected_row = self.tabla_perfiles.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Advertencia", "Por favor selecciona un perfil de la tabla para editar.")
            return

        perfil_id = int(self.tabla_perfiles.item(selected_row, 0).text())
        perfiles = db_manager.obtener_perfiles()
        perfil_datos = next((p for p in perfiles if p["id"] == perfil_id), None)

        if not perfil_datos:
            return

        dialog = PerfilDialog(self, perfil_datos)
        if dialog.exec() == QDialog.Accepted:
            datos = dialog.obtener_valores()
            exito = db_manager.actualizar_perfil(
                perfil_id=perfil_id,
                nombre_real=datos["nombre_real"],
                correo=datos["correo"],
                contrasena=datos["contrasena"],
                personalidad=datos["personalidad"],
                ia=datos["ia"]
            )
            if exito:
                QMessageBox.information(self, "Exito", "Perfil actualizado correctamente.")
                self.cargar_datos_perfiles()
                self.cargar_datos_control()
            else:
                QMessageBox.critical(self, "Error", "No se pudo actualizar el perfil.")

    def eliminar_perfil(self):
        selected_row = self.tabla_perfiles.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Advertencia", "Selecciona el perfil que deseas eliminar.")
            return

        perfil_id = int(self.tabla_perfiles.item(selected_row, 0).text())
        nombre_prof = self.tabla_perfiles.item(selected_row, 1).text()
        
        btn_resp = QMessageBox.question(
            self, "Confirmar eliminacion", 
            f"¿Estas seguro de que deseas eliminar permanentemente el perfil '{nombre_prof}' de la Base de Datos?",
            QMessageBox.Yes | QMessageBox.No
        )

        if btn_resp == QMessageBox.Yes:
            conn = db_manager.obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM perfiles WHERE id = ?", (perfil_id,))
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Exito", "Perfil eliminado correctamente.")
            self.cargar_datos_perfiles()
            self.cargar_datos_control()

    def agregar_grupo(self):
        dialog = GrupoDialog(self)
        if dialog.exec() == QDialog.Accepted:
            nombre = dialog.obtener_nombre()
            if not nombre:
                return
            exito = db_manager.agregar_grupo(nombre)
            if exito:
                QMessageBox.information(self, "Exito", f"Grupo '{nombre}' registrado correctamente.")
                self.cargar_datos_grupos()
            else:
                QMessageBox.critical(self, "Error", "El grupo ya esta registrado.")

    def eliminar_grupo(self):
        selected_row = self.tabla_grupos.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Advertencia", "Selecciona el grupo que deseas eliminar.")
            return

        grupo_id = int(self.tabla_grupos.item(selected_row, 0).text())
        nombre = self.tabla_grupos.item(selected_row, 1).text()

        btn_resp = QMessageBox.question(
            self, "Confirmar eliminacion", 
            f"¿Estas seguro de que deseas eliminar el grupo '{nombre}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if btn_resp == QMessageBox.Yes:
            conn = db_manager.obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM grupos WHERE id = ?", (grupo_id,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Exito", "Grupo eliminado de la base de datos.")
            self.cargar_datos_grupos()
            self.cargar_datos_estadisticas()

    def asociar_perfil_con_grupo(self):
        perfil_idx = self.combo_perfiles.currentIndex()
        grupo_idx = self.combo_grupos.currentIndex()

        if perfil_idx < 0 or grupo_idx < 0:
            QMessageBox.warning(self, "Advertencia", "Asegúrate de que haya perfiles y grupos registrados para poder asociarlos.")
            return

        perfil_id = self.combo_perfiles.currentData()
        grupo_id = self.combo_grupos.currentData()

        exito = db_manager.asociar_perfil_con_grupo(perfil_id, grupo_id)
        if exito:
            QMessageBox.information(self, "Exito", "Asociación Muchos a Muchos registrada correctamente.")
            self.cargar_datos_estadisticas()
            self.cargar_datos_perfiles() # Para actualizar la vista de grupos asociados
        else:
            QMessageBox.critical(self, "Error", "No se pudo crear la asociación.")

    # ==========================================================================
    # APARIENCIA Y HOJA DE ESTILOS PREMIUM (QSS STYLESHEET)
    # ==========================================================================
    def aplicar_estilos_premium(self):
        qss = """
        QMainWindow {
            background-color: #121212;
        }
        QWidget {
            color: #e0e0e0;
            font-family: "Segoe UI", Arial, sans-serif;
            font-size: 13px;
        }
        QLabel {
            font-weight: 500;
        }
        QLabel#lbl_titulo {
            font-size: 22px;
            font-weight: bold;
            color: #25D366;
            margin: 15px 0 10px 0;
            letter-spacing: 1px;
        }
        QTabWidget::pane {
            border: 1px solid #2d2d2d;
            background-color: #1a1a1a;
            border-radius: 8px;
        }
        QTabBar::tab {
            background-color: #222222;
            color: #888888;
            padding: 10px 20px;
            margin-right: 4px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            font-weight: 500;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: #1a1a1a;
            color: #25D366;
            font-weight: bold;
        }
        QPushButton {
            background-color: #2a2a2a;
            border: 1px solid #3a3a3a;
            color: #e0e0e0;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #25D366;
            color: #121212;
            border: 1px solid #25D366;
        }
        QPushButton:pressed {
            background-color: #1ebd56;
        }
        QTableWidget {
            background-color: #1c1c1c;
            alternate-background-color: #242424;
            gridline-color: #2d2d2d;
            border: 1px solid #2d2d2d;
            border-radius: 6px;
        }
        QTableWidget::item {
            padding: 6px;
        }
        QHeaderView::section {
            background-color: #2a2a2a;
            color: #00ADB5;
            padding: 8px;
            border: 1px solid #1e1e1e;
            font-weight: bold;
        }
        QLineEdit, QTextEdit, QComboBox {
            background-color: #2a2a2a;
            border: 1px solid #3a3a3a;
            border-radius: 6px;
            padding: 6px;
            color: #ffffff;
        }
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
            border: 1px solid #25D366;
        }
        QTextEdit#log_console {
            background-color: #0d0e11;
            border: 1px solid #20242c;
            border-radius: 6px;
            font-family: "Consolas", "Courier New", monospace;
            font-size: 12px;
            color: #00FF66;
            padding: 8px;
        }
        QGroupBox {
            border: 1px solid #2d2d2d;
            border-radius: 6px;
            margin-top: 15px;
            font-weight: bold;
            color: #00ADB5;
            padding: 15px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 15px;
            border-left-width: 1px;
            border-left-color: #3a3a3a;
            border-left-style: solid;
        }
        """
        self.setStyleSheet(qss)


# ==============================================================================
# PROCEDIMIENTO DE INICIO (BOOT GATEWAY)
# ==============================================================================

def lanzar_gui():
    app = QApplication(sys.argv)
    
    # Resolver problema de escala en monitores de alta resolución (HiDPI)
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    lanzar_gui()
