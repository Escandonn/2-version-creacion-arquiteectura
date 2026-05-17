# ARQUITECTURA MULTI PERFIL SELENIUMBASE + PYQT5 (ASÍNCRONA)

---

# OBJETIVO

Sistema asíncrono para:

* Gestionar múltiples perfiles
* Gestionar múltiples navegadores
* Detectar perfiles automáticamente
* Activar uno o varios perfiles
* Abrir perfiles con SeleniumBase
* Usar `user-data-dir`
* Mostrar interfaz visual con PyQt5
* **Ejecutar perfiles en threads independientes**
* **No bloquear la UI**
* Escalable a cientos de perfiles

---

# FLUJO GENERAL

```text
main.py
   │
   ▼
carpeta_gestor.py
   │
   ▼
obtener_navegadores()
   │
   ▼
front/ventana.py (UI Hermosa)
   │
   ▼
front/logica.py (QThread)
   │
   ▼
thread_manager.py
   │
   ├── NavegadorThread (Chrome Profile_1)
   ├── NavegadorThread (Chrome Profile_2)
   ├── NavegadorThread (Firefox Profile_1)
   └── NavegadorThread (Firefox Profile_2)
   │
   ▼
selenium_manager.py
   │
   ▼
SeleniumBase (Paralelo)
```
SeleniumBase (Paralelo)
```

---

# ESTRUCTURA FINAL

```text
proyecto/
│
├── main.py
│
├── perfiles/
│   ├── chrome/
│   ├── firefox/
│
├── gestores/
│   ├── __init__.py
│   ├── carpeta_gestor.py
│   ├── perfiles_manager.py
│   ├── selenium_manager.py
│   ├── thread_manager.py
│   └── sesiones_manager.py (NUEVO: Gestiona sesiones vivas)
│
├── selectores/
│   ├── __init__.py
│   └── ui_selectors.py (NUEVO: Selectores XPath/CSS aislados)
│
├── whatsapp/
│   ├── __init__.py
│   └── acciones.py (NUEVO: Lógica de interacción con WhatsApp)
│
├── opciones/
│   ├── __init__.py
│   ├── menu.py (legacy)
│
├── front/
│   ├── __init__.py
│   ├── ventana.py (UI Hermosa + Panel WhatsApp)
│   ├── logica.py (QThread Perfiles + QThread Mensajes)
│
├── modelos/
│   ├── __init__.py
│   ├── perfil.py
│
├── .gitignore
├── guia.md
├── arquitectura.md
└── README.md
```

---

# RESPONSABILIDAD DE CADA MÓDULO

## main.py

Control principal del sistema.

Responsabilidades:

* iniciar aplicación
* cargar perfiles desde carpeta_gestor
* abrir menú PyQt5
* no bloquear con SeleniumBase

---

## carpeta_gestor.py

Gestiona carpetas físicas.

Responsabilidades:

* crear estructura `perfiles/chrome` y `perfiles/firefox`
* detectar navegadores
* contar perfiles
* retornar diccionario de navegadores y perfiles

---

## perfiles_manager.py

Gestiona perfiles.

Responsabilidades:

* cargar perfiles
* detectar perfiles activos
* retornar información
* organizar perfiles

---

## selenium_manager.py

Abre navegadores (ahora asíncrono).

Responsabilidades:

* función `abrir_chrome(perfil)`
* función `abrir_firefox(perfil)`
* cargar `user-data-dir`
* ejecutar SeleniumBase

---

## thread_manager.py (NUEVO)

Gestiona threads de navegadores.

Responsabilidades:

* clase `NavegadorThread` hereda de `Thread`
* recibe navegador y perfil
* ejecuta navegador en thread independiente
* manejo de errores sin bloquear UI

---

## menu.py (LEGACY)

Versión anterior de la UI.

Responsabilidades:

* mantenido por compatibilidad
* interfaz básica con PyQt5
* sin QThread (bloquea UI)

---

## front/ventana.py (UI HERMOSA)

Interfaz gráfica hermosa.

Responsabilidades:

* diseño moderno con gradientes y colores
* QGroupBox para navegadores
* QCheckBox con íconos para perfiles
* QScrollArea para muchos perfiles
* QProgressBar indeterminada
* QTextEdit para logs en tiempo real
* botones: Abrir, Seleccionar Todo, Deseleccionar Todo
* señales PyQt5 para comunicación asíncrona
* **mantener ventana abierta y responsiva**

---

## front/logica.py (QTHREAD)

Lógica asíncrona con QThread.

Responsabilidades:

* heredar de QThread
* emitir señales `progreso_signal` y `terminado_signal`
* crear NavegadorThread para cada perfil
* manejar progreso sin bloquear UI
* comunicación thread-safe con UI

---

## ventana.py

Interfaz gráfica base.

Responsabilidades:

* crear ventana principal
* definir tamaño y título
* estructura base para extensiones

---

## perfil.py

Modelo de perfil.

Responsabilidades:

* almacenar datos del perfil
* nombre, navegador, ruta
* estado activo/inactivo
* métodos activar/desactivar

---

# FLUJO DE EJECUCIÓN

## PASO 1: Inicializar Sistema

`main.py` inicia.

```python
python main.py
```

---

## PASO 2: Detectar Perfiles

`carpeta_gestor.py` escanea carpetas:

* crea estructura si no existe
* detecta navegadores
* lista perfiles

---

## PASO 3: Obtener Navegadores

`obtener_navegadores()` retorna:

```python
{
    "chrome": [
        "Profile 1",
        "Profile 2"
    ],
    "firefox": [
        "profile_1"
    ]
}
```

---

## PASO 4: Mostrar UI Hermosa

`front/ventana.py` crea ventana hermosa:

```text
┌─────────────────────────────────────────────────┐
│ 🎯 Sistema Multi-Perfil SeleniumBase          │
├─────────────────────────────────────────────────┤
│ 🌐 CHROME (2 perfiles)                         │
│ ☐ 📁 Profile 1                                │
│ ☐ 📁 Profile 2                                │
├─────────────────────────────────────────────────┤
│ 🌐 FIREFOX (1 perfil)                          │
│ ☐ 📁 profile_1                                │
├─────────────────────────────────────────────────┤
│ [🚀 Abrir Seleccionados] [✅ Seleccionar Todo] │
│ [❌ Deseleccionar Todo]                        │
├─────────────────────────────────────────────────┤
│ 🔄 Estado: Esperando selección...             │
├─────────────────────────────────────────────────┤
│ Log de ejecución:                              │
│ Iniciando apertura de perfiles...              │
└─────────────────────────────────────────────────┘
```

---

## PASO 5: Usuario Selecciona Perfiles

Usuario marca checkboxes:

```text
☑ Profile 1
☐ Profile 2
☑ profile_1
```

---

## PASO 6: Presiona "Abrir Seleccionados"

Se ejecuta `obtener_activos()`:

```python
{
    "chrome": ["Profile 1"],
    "firefox": ["profile_1"]
}
```

---

## PASO 7: Crear QThread (NO BLOQUEA UI)

`LogicaPerfiles` (QThread) inicia:

```python
self.logica = LogicaPerfiles(self.activos)
self.logica.progreso_signal.connect(self.actualizar_progreso)
self.logica.terminado_signal.connect(self.terminado)
self.logica.start()
```

---

## PASO 8: QThread Crea NavegadorThreads

Dentro de `LogicaPerfiles.run()`:

```python
for navegador, perfiles in self.activos.items():
    for perfil in perfiles:
        self.progreso_signal.emit(f"Abriendo {navegador} -> {perfil}")

        hilo = NavegadorThread(navegador, perfil)
        hilo.start()
        self.threads.append(hilo)
```

---

## PASO 9: Señales Actualizan UI

Señales PyQt5 actualizan la UI en tiempo real:

```python
def actualizar_progreso(self, mensaje):
    self.status.setText(f"🔄 {mensaje}")
    self.log_area.append(mensaje)
```

---

## PASO 10: UI Permanece Activa

Ventana hermosa:

* sigue respondiendo
* permite seleccionar más perfiles
* muestra progreso en tiempo real
* no se congela

---

# SISTEMA ASÍNCRONO

## Problema Resuelto

Antes: SeleniumBase bloqueaba la UI

```python
abrir_chrome("Profile 1")  # Bloquea
abrir_chrome("Profile 2")  # Espera
```

Resultado: Interfaz congelada.

---

## Solución Implementada

Usar `threading.Thread` con `NavegadorThread`:

```python
hilo1 = NavegadorThread("chrome", "Profile 1")
hilo2 = NavegadorThread("chrome", "Profile 2")
hilo1.start()  # Paralelo
hilo2.start()  # Paralelo
```

Resultado: UI responsiva.

---

# ARQUITECTURA ASÍNCRONA

```text
┌─────────────────────────────────────────────────┐
│              PyQt5 UI Hermosa                   │
│  (Main Thread - Responsive)                     │
├─────────────────────────────────────────────────┤
│                                                 │
│  ☑ Profile 1  ☑ Profile 2                     │
│  [🚀 Abrir] [✅ Todo] [❌ Nada]                │
│  🔄 Abriendo chrome -> Profile 1              │
│  Log: Iniciando... Abriendo... Terminado.     │
│                                                 │
└────────────┬────────────────────────────────────┘
             │
             ├─────────────────────────────────────┐
             │                                     │
             ▼                                     ▼
    
    ┌──────────────────────┐       ┌──────────────────────┐
    │ LogicaPerfiles       │       │ NavegadorThread      │
    │ (QThread)            │       │ (Thread)             │
    │ progreso_signal.emit │       │ SeleniumBase Chrome  │
    │ terminado_signal.emit│       │ user-data-dir=...    │
    │                      │       │ open(google.com)     │
    │                      │       │                      │
    └──────────────────────┘       └──────────────────────┘
    
    (Ejecuta en paralelo sin bloquear UI hermosa)
```

---

# VENTAJAS DEL SISTEMA

* **UI Hermosa y Responsive** - gradientes, íconos, scroll
* **No se congela** mientras SeleniumBase corre
* **Múltiples perfiles simultáneos** en paralelo
* **Escalable** a 10, 50, 100 perfiles
* **Modular** - fácil agregar navegadores
* **Robusto** - si un perfil falla, otros continúan
* **Flexible** - abrir nuevos perfiles sin reiniciar
* **QThread + Signals** - comunicación thread-safe
* **Log en tiempo real**
* **Botones adicionales** (Seleccionar Todo, Deseleccionar)
* **Preparado** para bots, automatización masiva
* **QThread + Señales PyQt5** - comunicación thread-safe

---

# CÓDIGO COMPLETO

---

## main.py

```python
from gestores.carpeta_gestor import obtener_navegadores
from front.ventana import seleccionar_perfiles


def main():

    datos = obtener_navegadores()

    seleccionar_perfiles(datos)


if __name__ == "__main__":
    main()
```

---

## gestores/carpeta_gestor.py

```python
import os

RUTA_PERFILES = "perfiles"


NAVS = [
    "chrome",
    "firefox"
]



def crear_estructura():

    if not os.path.exists(RUTA_PERFILES):
        os.makedirs(RUTA_PERFILES)

    for nav in NAVS:

        ruta = os.path.join(
            RUTA_PERFILES,
            nav
        )

        if not os.path.exists(ruta):
            os.makedirs(ruta)



def obtener_navegadores():

    crear_estructura()

    navegadores = {}

    for navegador in os.listdir(RUTA_PERFILES):

        ruta_navegador = os.path.join(
            RUTA_PERFILES,
            navegador
        )

        if os.path.isdir(ruta_navegador):

            perfiles = []

            for perfil in os.listdir(ruta_navegador):

                ruta_perfil = os.path.join(
                    ruta_navegador,
                    perfil
                )

                if os.path.isdir(ruta_perfil):
                    perfiles.append(perfil)

            navegadores[navegador] = perfiles

    return navegadores
```

---

## gestores/thread_manager.py

```python
from threading import Thread
from gestores.selenium_manager import (
    abrir_chrome,
    abrir_firefox
)


class NavegadorThread(Thread):

    def __init__(
        self,
        navegador,
        perfil
    ):

        super().__init__()

        self.navegador = navegador
        self.perfil = perfil
        self.daemon = True


    def run(self):

        try:

            if self.navegador == "chrome":
                abrir_chrome(self.perfil)

            elif self.navegador == "firefox":
                abrir_firefox(self.perfil)

        except Exception as e:
            print(f"Error al abrir {self.navegador} {self.perfil}: {e}")
```

---

## gestores/selenium_manager.py

```python
import os
from seleniumbase import SB



def abrir_chrome(perfil):

    ruta = os.path.join(
        "perfiles",
        "chrome",
        perfil
    )

    with SB(
        browser="chrome",
        uc=True,
        user_data_dir=ruta
    ) as sb:

        sb.open("https://google.com")

        sb.sleep(999)



def abrir_firefox(perfil):

    ruta = os.path.join(
        "perfiles",
        "firefox",
        perfil
    )

    with SB(
        browser="firefox",
        user_data_dir=ruta
    ) as sb:

        sb.open("https://google.com")

        sb.sleep(999)



def abrir_perfiles(activos):

    from gestores.thread_manager import NavegadorThread

    threads = []

    for navegador, perfiles in activos.items():

        for perfil in perfiles:

            print(f"Abriendo en thread -> {navegador} -> {perfil}")

            hilo = NavegadorThread(
                navegador,
                perfil
            )

            hilo.start()

            threads.append(hilo)
```

---

## opciones/menu.py

```python
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QCheckBox,
    QApplication
)

from gestores.thread_manager import NavegadorThread


class MenuPerfiles(QWidget):

    def __init__(self, datos):

        super().__init__()

        self.datos = datos

        self.activos = {}

        self.threads = []

        self.setWindowTitle("Multi Perfil SeleniumBase")

        self.resize(500, 600)

        self.layout = QVBoxLayout()

        self.checkboxes = {}

        self.crear_ui()

        self.setLayout(self.layout)


    def crear_ui(self):

        titulo = QLabel("Navegadores Detectados")

        self.layout.addWidget(titulo)

        for navegador, perfiles in self.datos.items():

            texto = QLabel(
                f"{navegador} -> {len(perfiles)} perfiles"
            )

            self.layout.addWidget(texto)

            self.checkboxes[navegador] = []

            for perfil in perfiles:

                check = QCheckBox(perfil)

                self.layout.addWidget(check)

                self.checkboxes[navegador].append(check)

        self.boton = QPushButton("Abrir Seleccionados")

        self.boton.clicked.connect(self.obtener_activos)

        self.layout.addWidget(self.boton)

        self.status = QLabel("")
        self.layout.addWidget(self.status)


    def obtener_activos(self):

        for navegador, checks in self.checkboxes.items():

            self.activos[navegador] = []

            for check in checks:

                if check.isChecked():
                    self.activos[navegador].append(
                        check.text()
                    )

        if any(self.activos.values()):
            self.status.setText("Abriendo perfiles en threads...")
            self.boton.setEnabled(False)
            self.abrir_en_threads()
            self.status.setText("Perfiles abiertos. Ventana activa.")
        else:
            self.status.setText("Selecciona al menos un perfil antes de abrir.")


    def abrir_en_threads(self):

        for navegador, perfiles in self.activos.items():

            for perfil in perfiles:

                print(f"Abriendo en thread -> {navegador} -> {perfil}")

                hilo = NavegadorThread(
                    navegador,
                    perfil
                )

                hilo.start()

                self.threads.append(hilo)


def sel eccionar_perfiles(datos):

    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    ventana = MenuPerfiles(datos)

    ventana.show()

    app.exec_()
```

---

## front/ventana.py

```python
from PyQt5.QtWidgets import QWidget


class Ventana(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Sistema Multi Perfil")

        self.resize(1000, 700)
```

---

## front/logica.py

```python
from PyQt5.QtCore import QThread, pyqtSignal
from gestores.thread_manager import NavegadorThread


class LogicaPerfiles(QThread):

    progreso_signal = pyqtSignal(str)
    terminado_signal = pyqtSignal(str)

    def __init__(self, activos):
        super().__init__()
        self.activos = activos
        self.threads = []

    def run(self):
        self.progreso_signal.emit("Iniciando apertura de perfiles...")

        for navegador, perfiles in self.activos.items():
            for perfil in perfiles:
                self.progreso_signal.emit(f"Abriendo {navegador} -> {perfil}")

                hilo = NavegadorThread(navegador, perfil)
                hilo.start()
                self.threads.append(hilo)

        self.progreso_signal.emit("Todos los perfiles iniciados en threads")
        self.terminado_signal.emit("Perfiles abiertos exitosamente. UI activa.")
```

---

## front/ventana.py

```python
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
```

---

## modelos/perfil.py

```python
class Perfil:

    def __init__(
        self,
        nombre,
        navegador,
        ruta
    ):

        self.nombre = nombre

        self.navegador = navegador

        self.ruta = ruta

        self.activo = False


    def activar(self):
        self.activo = True


    def desactivar(self):
        self.activo = False
```

---

# INSTALACIÓN

## Dependencias

```bash
pip install -U seleniumbase
pip install PyQt5
```

---

## Drivers

```bash
python -m seleniumbase install chromedriver
python -m seleniumbase install geckodriver
```

---

# EJECUCIÓN

```bash
python main.py
```

---

# CARACTERÍSTICAS IMPLEMENTADAS

✅ Arquitectura modular  
✅ Detección automática de perfiles  
✅ **UI Hermosa y Responsive** (gradientes, íconos, scroll)  
✅ Sistema asíncrono con QThread + Thread  
✅ UI no bloqueada  
✅ Múltiples perfiles en paralelo  
✅ Manejo de errores en threads  
✅ Escalable a cientos de perfiles  
✅ Compatible con Chrome y Firefox  
✅ **Señales PyQt5 para comunicación thread-safe**  
✅ **Log en tiempo real**  
✅ **Botones adicionales** (Seleccionar Todo, Deseleccionar)  
✅ Preparado para bots y automatización  

---

# PROXIMAS MEJORAS

* Agregar Signal/Slot para actualizaciones en tiempo real
* Progreso bar con porcentaje real
* Guardar configuración de perfiles
* Agregar más navegadores (Edge, Opera)
* Sistema de logging completo a archivo
* Monitor de recursos (CPU, memoria)
* Pausar/Reanudar perfiles
* Kill automático de procesos zombie
* Tema oscuro/claro
* Animaciones de carga
* Notificaciones del sistema
* Exportar logs
* Configuración avanzada
* Sistema de logging completo
* Monitor de recursos (CPU, memoria)
* Pausar/Reanudar perfiles
* Kill automático de procesos zombie
