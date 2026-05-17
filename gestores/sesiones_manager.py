# Gestor de Sesiones Activas
# Mantiene las instancias de SeleniumBase para que la UI pueda interactuar con ellas

class SesionesManager:
    _sesiones = {}

    @classmethod
    def registrar_sesion(cls, id_sesion, sb):
        """Registra una sesión activa de SeleniumBase"""
        cls._sesiones[id_sesion] = sb
        print(f"[SesionesManager] Registrada sesión: {id_sesion}")

    @classmethod
    def obtener_sesion(cls, id_sesion):
        """Devuelve la instancia sb de una sesión, o None si no existe"""
        return cls._sesiones.get(id_sesion)

    @classmethod
    def eliminar_sesion(cls, id_sesion):
        """Elimina una sesión del registro"""
        if id_sesion in cls._sesiones:
            del cls._sesiones[id_sesion]
            print(f"[SesionesManager] Eliminada sesión: {id_sesion}")

    @classmethod
    def obtener_todas(cls):
        """Devuelve un diccionario con todas las sesiones activas"""
        return cls._sesiones

    @classmethod
    def obtener_ids(cls):
        """Devuelve una lista con los IDs de las sesiones activas"""
        return list(cls._sesiones.keys())
