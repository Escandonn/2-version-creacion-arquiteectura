from PyQt5.QtCore import QThread, pyqtSignal
from gestores.thread_manager import NavegadorThread
from gestores.sesiones_manager import SesionesManager
from whatsapp.acciones import entrar_a_chat, escribir_y_enviar_mensaje


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

class LogicaEnvioMensajes(QThread):
    progreso_signal = pyqtSignal(str)
    terminado_signal = pyqtSignal(str)

    def __init__(self, ids_sesiones, nombre_grupo, mensaje):
        super().__init__()
        self.ids_sesiones = ids_sesiones
        self.nombre_grupo = nombre_grupo
        self.mensaje = mensaje

    def run(self):
        self.progreso_signal.emit(f"Iniciando envío a grupo '{self.nombre_grupo}'...")
        
        for id_sesion in self.ids_sesiones:
            sb = SesionesManager.obtener_sesion(id_sesion)
            if not sb:
                self.progreso_signal.emit(f"[{id_sesion}] Sesión no encontrada.")
                continue
                
            self.progreso_signal.emit(f"[{id_sesion}] Entrando al chat...")
            exito_chat, msg_chat = entrar_a_chat(sb, self.nombre_grupo)
            
            if exito_chat:
                self.progreso_signal.emit(f"[{id_sesion}] Enviando mensaje...")
                exito_msg, msg_envio = escribir_y_enviar_mensaje(sb, self.mensaje, self.nombre_grupo)
                self.progreso_signal.emit(f"[{id_sesion}] Resultado: {msg_envio}")
            else:
                self.progreso_signal.emit(f"[{id_sesion}] Falló entrada a chat: {msg_chat}")

        self.terminado_signal.emit("Proceso de envío completado.")