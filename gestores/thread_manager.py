from threading import Thread
from gestores.selenium_manager import (
    abrir_chrome,
    abrir_firefox,
    abrir_edge
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

            elif self.navegador == "edge":
                abrir_edge(self.perfil)

        except Exception as e:
            print(f"Error al abrir {self.navegador} {self.perfil}: {e}")