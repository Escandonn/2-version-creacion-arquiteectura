# Arquitectura del Bot de WhatsApp (Versión Consola / Sin UI)

Esta es la versión del bot controlada enteramente por consola. Ha sido actualizada para implementar una **lógica multi-perfil sincronizada y asíncrona**, permitiendo ejecutar múltiples perfiles de diferentes navegadores en paralelo, manteniendo sus flujos y posibles errores totalmente independientes.

## Estructura de Archivos

```
/sin-ui
├── main.py              (Punto de entrada, Menú Maestro y orquestador de Hilos)
├── bot_sb.py            (Lógica de SeleniumBase y manipulación de WhatsApp)
├── ui_selectors.py      (Centralización de XPaths de la interfaz)
├── carpeta_gestor.py    (Escaneo y listado automático de perfiles)
├── perfiles/            (Directorio raíz de perfiles)
│   ├── chrome/
│   └── firefox/
└── arquitectura.md      (Explicación detallada de la lógica de hilos)
```

### Novedades del Sistema

- **Selección Dinámica:** Al arrancar el script, te mostrará una lista de todos los perfiles detectados en la carpeta `perfiles/` y te dejará elegir cuáles abrir.
- **Hilos Paralelos:** Los navegadores se abren de forma simultánea (paralela) usando `threading`.
- **Menú Maestro Centralizado:** Para evitar que la consola colapse con múltiples perfiles pidiendo `input()`, el menú está en `main.py`. Este menú captura tus directrices (ej: qué mensaje enviar) y luego manda la orden a los bots en paralelo.
- **Aislamiento de Errores:** Si el perfil 1 falla buscando un grupo, el perfil 2 y 3 continuarán sin inmutarse ni retrasarse.
- **Mensajes Independientes:** El menú maestro te permite asignar un grupo y un mensaje distinto para cada perfil activo, o asignar el mismo para todos.

## Ejecución
Para iniciar el proyecto basta con asegurarte de tener perfiles creados en la carpeta `perfiles` y ejecutar:
```bash
python main.py
```
