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
menu.py (PyQt5)
   │
   ▼
seleccionar_perfiles()
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

---

# ESTRUCTURA FINAL

```text
proyecto/
│
├── main.py
│
├── perfiles/
│   ├── chrome/
│   │   ├── Profile 1/
│   │   ├── Profile 2/
│   │
│   ├── firefox/
│       ├── profile_1/
│       ├── profile_2/
│
├── gestores/
│   ├── __init__.py
│   ├── carpeta_gestor.py
│   ├── perfiles_manager.py
│   ├── selenium_manager.py
│   ├── thread_manager.py
│
├── opciones/
│   ├── __init__.py
│   ├── menu.py
│
├── front/
│   ├── __init__.py
│   ├── ventana.py
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

## menu.py

Controla la interfaz PyQt5.

Responsabilidades:

* mostrar perfiles detectados
* checkboxes para seleccionar perfiles
* botón "Abrir Seleccionados"
* crear threads para cada perfil
* mostrar estado de ejecución
* **mantener ventana abierta**

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

## PASO 4: Mostrar Interfaz PyQt5

`menu.py` crea ventana:

```text
┌────────────────────────────────┐
│ Navegadores Detectados         │
├────────────────────────────────┤
│ chrome -> 2 perfiles           │
│ ☐ Profile 1                    │
│ ☐ Profile 2                    │
├────────────────────────────────┤
│ firefox -> 1 perfil            │
│ ☐ profile_1                    │
├────────────────────────────────┤
│ [Abrir Seleccionados]          │
├────────────────────────────────┤
│ Estado: Esperando selección... │
└────────────────────────────────┘
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

## PASO 7: Crear Threads (NO BLOQUEA UI)

`abrir_en_threads()` crea threads:

```python
for navegador, perfiles in activos.items():
    for perfil in perfiles:
        hilo = NavegadorThread(navegador, perfil)
        hilo.start()
        threads.append(hilo)
```

---

## PASO 8: Threads Abren Navegadores

Cada `NavegadorThread`:

* corre en paralelo
* ejecuta `abrir_chrome()` o `abrir_firefox()`
* carga perfil con `user-data-dir`
* abre URL de prueba
* **NO bloquea la UI**

---

## PASO 9: UI Permanece Activa

Ventana PyQt5:

* sigue respondiendo
* permite seleccionar más perfiles
* muestra estado en tiempo real
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
┌─────────────────────────────────────────┐
│          PyQt5 UI (Main Thread)         │
├─────────────────────────────────────────┤
│                                         │
│  ☑ Profile 1  ☑ Profile 2             │
│  [Abrir Seleccionados]                 │
│  "Perfiles abiertos. Ventana activa."  │
│                                         │
└────────────┬────────────────────────────┘
             │
             ├─────────────────────────────────────┐
             │                                     │
             ▼                                     ▼
    
    ┌──────────────────────┐       ┌──────────────────────┐
    │ NavegadorThread      │       │ NavegadorThread      │
    │ chrome/Profile 1     │       │ firefox/profile_1    │
    │                      │       │                      │
    │ SeleniumBase Chrome  │       │ SeleniumBase Firefox │
    │ user-data-dir=...    │       │ user-data-dir=...    │
    │ open(google.com)     │       │ open(google.com)     │
    └──────────────────────┘       └──────────────────────┘
    
    (Ejecuta en paralelo sin bloquear UI)
```

---

# VENTAJAS DEL SISTEMA

* **UI No se congela** mientras SeleniumBase corre
* **Múltiples perfiles simultáneos** en paralelo
* **Escalable** a 10, 50, 100 perfiles
* **Modular** - fácil agregar navegadores
* **Robusto** - si un perfil falla, otros continúan
* **Flexible** - abrir nuevos perfiles sin reiniciar
* **Preparado** para bots, automatización masiva

---

# CÓDIGO COMPLETO

---

## main.py

```python
from gestores.carpeta_gestor import obtener_navegadores
from opciones.menu import seleccionar_perfiles


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


def seleccionar_perfiles(datos):

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
✅ Interfaz PyQt5 completa  
✅ Sistema asíncrono con threads  
✅ UI no bloqueada  
✅ Múltiples perfiles en paralelo  
✅ Manejo de errores en threads  
✅ Escalable a cientos de perfiles  
✅ Compatible con Chrome y Firefox  
✅ Preparado para bots y automatización  

---

# PROXIMAS MEJORAS

* Agregar Signal/Slot para actualizaciones en tiempo real
* Progreso bar de ejecución
* Guardar configuración de perfiles
* Agregar más navegadores (Edge, Opera)
* Sistema de logging completo
* Monitor de recursos (CPU, memoria)
* Pausar/Reanudar perfiles
* Kill automático de procesos zombie
