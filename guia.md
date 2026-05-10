# ARQUITECTURA MULTI PERFIL SELENIUMBASE + PYQT5

---

# OBJETIVO

IMPORTANTE:

El sistema debe ser:

* asíncrono
* no bloquear la UI
* compatible con múltiples navegadores simultáneos
* estable con PyQt5
* abrir perfiles en paralelo
* evitar congelamiento de interfaz
* evitar cierre completo si un navegador falla
* arquitectura preparada para threads y escalabilidad

La UI nunca debe bloquearse mientras SeleniumBase ejecuta perfiles.

Cada navegador debe ejecutarse en procesos o threads independientes.

---

# ARQUITECTURA ASÍNCRONA

Sistema para:

* Gestionar múltiples perfiles
* Gestionar múltiples navegadores
* Detectar perfiles automáticamente
* Activar uno o varios perfiles
* Abrir perfiles con SeleniumBase
* Usar `user-data-dir`
* Mostrar interfaz visual con PyQt5
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
perfiles_manager.py
   │
   ▼
menu.py
   │
   ▼
seleccionar_perfiles()
   │
   ▼
selenium_manager.py
   │
   ▼
abre navegadores seleccionados
```

---

# DIAGRAMA COMPLETO

```text
╔════════════════════════════════════════════════════════════════════╗
║      ARQUITECTURA MULTI PERFIL SELENIUMBASE + FRONT PYQT5        ║
╚════════════════════════════════════════════════════════════════════╝



                            ┌──────────────┐
                            │    main.py   │
                            └──────┬───────┘
                                   │
                                   │ inicia sistema
                                   ▼


                    ┌──────────────────────────┐
                    │   carpeta_gestor.py      │
                    └──────────┬───────────────┘
                               │
                               │ escanea carpetas
                               ▼

                    ┌──────────────────────────┐
                    │ obtener_navegadores()    │
                    └──────────┬───────────────┘
                               │
                               │ retorna:
                               │ chrome -> 5
                               │ firefox -> 2
                               ▼

                    ┌──────────────────────────┐
                    │   perfiles_manager.py    │
                    └──────────┬───────────────┘
                               │
                               │ crea perfiles
                               │ detecta rutas
                               ▼

          ┌──────────────────────────────────────────┐
          │                                          │
          ▼                                          ▼

┌───────────────────────┐              ┌───────────────────────┐
│ perfiles/chrome/      │              │ perfiles/firefox/     │
└──────────┬────────────┘              └──────────┬────────────┘
           │                                      │
           ▼                                      ▼

┌───────────────────────┐              ┌───────────────────────┐
│ profile_1             │              │ profile_1             │
│ profile_2             │              │ profile_2             │
│ profile_3             │              │ profile_3             │
└───────────────────────┘              └───────────────────────┘



════════════════════════════════════════════════════════════════════
                           FRONTEND PYQT5
════════════════════════════════════════════════════════════════════


                    ┌──────────────────────────┐
                    │      ventana.py          │
                    └──────────┬───────────────┘
                               │
                               │ crea interfaz
                               ▼

                    ┌──────────────────────────┐
                    │        menu.py           │
                    └──────────┬───────────────┘
                               │
                               │ muestra:
                               │
                               │ cantidad perfiles
                               │ perfiles activos
                               │ selección múltiple
                               ▼

                 ┌───────────────────────────────┐
                 │ seleccionar_perfiles()        │
                 └─────────────┬─────────────────┘
                               │
                               │ usuario selecciona:
                               │
                               │ ☑ profile_1
                               │ ☑ profile_3
                               │ ☐ profile_4
                               ▼

════════════════════════════════════════════════════════════════════
                         SELENIUMBASE CORE
════════════════════════════════════════════════════════════════════


                    ┌──────────────────────────┐
                    │   selenium_manager.py    │
                    └──────────┬───────────────┘
                               │
                               │ abre perfiles
                               ▼

         ┌───────────────────────────────────────────┐
         │                                           │
         ▼                                           ▼

┌────────────────────────┐             ┌────────────────────────┐
│ abrir_chrome()         │             │ abrir_firefox()        │
└──────────┬─────────────┘             └──────────┬─────────────┘
           │                                      │
           │ user-data-dir                        │ profile-path
           ▼                                      ▼

┌────────────────────────┐             ┌────────────────────────┐
│ SeleniumBase Chrome    │             │ SeleniumBase Firefox   │
└────────────────────────┘             └────────────────────────┘
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
│   │   ├── profile_1/
│   │   ├── profile_2/
│   │
│   ├── firefox/
│       ├── profile_1/
│       ├── profile_2/
│
├── gestores/
│   ├── carpeta_gestor.py
│   ├── perfiles_manager.py
│   ├── selenium_manager.py
│
├── opciones/
│   ├── menu.py
│
├── front/
│   ├── ventana.py
│   ├── widgets.py
│
└── modelos/
    ├── perfil.py
```

---

# RESPONSABILIDAD DE CADA MÓDULO

## main.py

Control principal del sistema.

Responsabilidades:

* iniciar aplicación
* cargar perfiles
* abrir menú
* iniciar SeleniumBase

---

## carpeta_gestor.py

Gestiona carpetas físicas.

Responsabilidades:

* detectar navegadores
* crear carpetas faltantes
* validar rutas
* contar perfiles

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

Abre navegadores.

Responsabilidades:

* abrir Chrome
* abrir Firefox
* cargar user-data-dir
* ejecutar SeleniumBase

---

## menu.py

Controla opciones.

Responsabilidades:

* mostrar perfiles
* seleccionar perfiles
* activar varios
* activar todos

---

## ventana.py

Interfaz gráfica.

Responsabilidades:

* crear ventana
* crear tabla
* botones
* selección visual

---

## widgets.py

Widgets reutilizables.

Responsabilidades:

* botones
* tablas
* checkbox
* labels

---

# FLUJO DE EJECUCIÓN

## PASO 1

`main.py` inicia sistema.

---

## PASO 2

`carpeta_gestor.py`:

* escanea carpetas
* detecta navegadores
* cuenta perfiles

---

## PASO 3

`obtener_navegadores()` retorna:

```python
{
    "chrome": [
        "profile_1",
        "profile_2"
    ],

    "firefox": [
        "profile_1"
    ]
}
```

---

## PASO 4

`menu.py` muestra:

```text
Chrome -> 2 perfiles
Firefox -> 1 perfil
```

---

## PASO 5

Usuario selecciona:

```text
☑ profile_1
☑ profile_2
```

---

## PASO 6

`selenium_manager.py` abre:

* Chrome
* Firefox
* perfiles activos

---

## PASO 7

SeleniumBase carga:

```python
user_data_dir=ruta
```

---

# FRONTEND PYQT5

## Ventana principal

Contendrá:

```text
┌─────────────────────────────┐
│ Navegadores                 │
├─────────────────────────────┤
│ ☑ Chrome  -> 5 perfiles     │
│ ☑ Firefox -> 2 perfiles     │
├─────────────────────────────┤
│ Profiles                    │
├─────────────────────────────┤
│ ☑ profile_1                 │
│ ☑ profile_2                 │
│ ☐ profile_3                 │
├─────────────────────────────┤
│ [Abrir] [Abrir Todos]       │
└─────────────────────────────┘
```

---

# FUNCIONES PRINCIPALES

## obtener_navegadores()

```python
- escanea navegadores
- cuenta perfiles
- retorna perfiles
```

---

## seleccionar_perfiles()

```python
- activa perfiles
- múltiples perfiles
- activar todos
```

---

## abrir_perfiles()

```python
- abre perfiles seleccionados
- carga user-data-dir
- ejecuta SeleniumBase
```

---

# SISTEMA ASÍNCRONO

## PROBLEMA

Si SeleniumBase abre perfiles directamente desde PyQt5:

```python
abrir_chrome()
```

la interfaz se congela.

---

## SOLUCIÓN

Usar:

* QThread
* threading
* workers
* señales PyQt5

Cada perfil debe abrirse en un thread independiente.

---

# FLUJO ASÍNCRONO

```text
UI PyQt5
   │
   ▼
Thread Manager
   │
   ├── Thread Chrome Profile_1
   ├── Thread Chrome Profile_2
   ├── Thread Firefox Profile_1
   └── Thread Firefox Profile_2
```

---

# THREAD MANAGER

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


    def run(self):

        try:

            if self.navegador == "chrome":
                abrir_chrome(self.perfil)

            elif self.navegador == "firefox":
                abrir_firefox(self.perfil)

        except Exception as e:
            print(e)
```

---

# ABRIR PERFILES SIN BLOQUEAR UI

```python
from gestores.thread_manager import NavegadorThread


threads = []

for navegador, perfiles in activos.items():

    for perfil in perfiles:

        hilo = NavegadorThread(
            navegador,
            perfil
        )

        hilo.start()

        threads.append(hilo)
```

---

# REGLAS IMPORTANTES

## 1

Nunca ejecutar Selenium directamente en UI.

---

## 2

Cada navegador debe ejecutarse separado.

---

## 3

Si un navegador falla:

* la UI sigue funcionando
* los demás perfiles siguen abiertos

---

## 4

No bloquear:

```python
app.exec_()
```

---

## 5

Preparado para:

* 10 perfiles
* 50 perfiles
* 100 perfiles

---

# ARQUITECTURA FINAL ASÍNCRONA

```text
PyQt5 UI
   │
   ▼
Thread Manager
   │
   ▼
SeleniumBase Workers
   │
   ├── Chrome Worker
   ├── Firefox Worker
   ├── Edge Worker
   └── Opera Worker
```

---

# VENTAJAS

* modular
* escalable
* múltiples navegadores
* múltiples perfiles
* compatible SeleniumBase
* compatible PyQt5
* perfiles independientes
* fácil mantenimiento
* preparado para bots simultáneos

---

# PREPARADO PARA FUTURO

Escalable para:

* WhatsApp bots
* Telegram bots
* Instagram bots
* múltiples sesiones
* automatización masiva
* control centralizado
* IA multi perfil

---

# CÓDIGO COMPLETO

---

# main.py

```python
from gestores.carpeta_gestor import obtener_navegadores
from opciones.menu import seleccionar_perfiles
from gestores.selenium_manager import abrir_perfiles


def main():

    datos = obtener_navegadores()

    activos = seleccionar_perfiles(datos)

    abrir_perfiles(activos)


if __name__ == "__main__":
    main()
```

---

# gestores/carpeta_gestor.py

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

# gestores/selenium_manager.py

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

    for navegador, perfiles in activos.items():

        for perfil in perfiles:

            print(f"Abriendo -> {navegador} -> {perfil}")

            if navegador == "chrome":
                abrir_chrome(perfil)

            elif navegador == "firefox":
                abrir_firefox(perfil)
```

---

# opciones/menu.py

```python
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QCheckBox,
    QApplication
)


class MenuPerfiles(QWidget):

    def __init__(self, datos):

        super().__init__()

        self.datos = datos

        self.activos = {}

        self.setWindowTitle("Multi Perfil SeleniumBase")

        self.resize(500, 500)

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

        boton = QPushButton("Abrir Seleccionados")

        boton.clicked.connect(self.obtener_activos)

        self.layout.addWidget(boton)


    def obtener_activos(self):

        for navegador, checks in self.checkboxes.items():

            self.activos[navegador] = []

            for check in checks:

                if check.isChecked():
                    self.activos[navegador].append(
                        check.text()
                    )

        print(self.activos)



def seleccionar_perfiles(datos):

    app = QApplication([])

    ventana = MenuPerfiles(datos)

    ventana.show()

    app.exec_()

    return ventana.activos
```

---

# front/ventana.py

```python
from PyQt5.QtWidgets import QWidget


class Ventana(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Sistema Multi Perfil")

        self.resize(1000, 700)
```

---

# modelos/perfil.py

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

# .gitignore

```gitignore
perfiles/

__pycache__/
*.pyc

venv/
.env

*.log

**/Cache/
**/Code Cache/
**/GPUCache/
```

---

# INSTALAR DEPENDENCIAS

```bash
pip install -U seleniumbase
pip install PyQt5
```

---

# INSTALAR DRIVERS

```bash
seleniumbase install chromedriver
seleniumbase install geckodriver
```

---

# EJECUTAR

```bash
python main.py
```

---

# COMMIT RECOMENDADO

````text
feat: arquitectura multi perfil SeleniumBase + PyQt5

- sistema multi navegador
- gestión automática perfiles
- integración SeleniumBase
- frontend PyQt5
- selección perfiles activos
- arquitectura modular escalable
```text
feat: arquitectura multi perfil SeleniumBase + PyQt5

- sistema multi navegador
- gestión automática perfiles
- integración SeleniumBase
- frontend PyQt5
- selección perfiles activos
- arquitectura modular escalable
````
