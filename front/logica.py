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