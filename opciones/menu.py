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