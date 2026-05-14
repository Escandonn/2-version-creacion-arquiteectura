# Arquitectura del Bot de WhatsApp

Este proyecto está diseñado para automatizar interacciones en WhatsApp Web utilizando SeleniumBase. La arquitectura se basa en el principio de separación de responsabilidades (Separation of Concerns), lo que asegura que el código sea mantenible, escalable y fácil de leer.

## Estructura de Archivos

```
/
├── main.py
├── bot_sb.py
├── ui_selectors.py
├── perfil/
│   └── profile 1/      (Carpeta autogenerada por Chrome/SeleniumBase con la sesión)
```

### 1. `main.py`
Es el punto de entrada principal (Entrypoint). Su única responsabilidad es inicializar la configuración (como definir la ruta del perfil de usuario) y arrancar la clase del bot. Mantener este archivo simple permite que otros desarrolladores entiendan rápidamente dónde y cómo inicia la aplicación.

### 2. `ui_selectors.py`
Contiene la clase `WhatsappSelectors`. Aquí se centralizan todas las rutas XPath utilizadas para identificar elementos en el DOM (la interfaz de WhatsApp).
- **Ventaja**: Si WhatsApp actualiza el diseño de su página y los elementos cambian, no necesitas buscar en toda la lógica del bot. Solo debes actualizar el XPath correspondiente en este archivo.

### 3. `bot_sb.py`
Contiene la clase principal `WhatsappBot` que implementa la lógica orientada a objetos.
- Controla el navegador utilizando `SeleniumBase`.
- Ejecuta los pasos lógicos del negocio a través de métodos modulares (`entrar_a_grupos`, `obtener_titulos_grupos`, `entrar_a_chat`, `escribir_y_enviar_mensaje`).
- Implementa un menú interactivo en consola para permitir pruebas parciales del sistema, sin requerir una recarga del navegador por cada acción, agilizando el flujo de trabajo de desarrollo.

## Ejecución
Para iniciar el proyecto basta con ejecutar:
```bash
python main.py
```
