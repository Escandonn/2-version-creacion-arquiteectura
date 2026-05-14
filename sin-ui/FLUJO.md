# Flujo Paso a Paso de la Automatización

Este documento describe la secuencia técnica que sigue el bot para automatizar WhatsApp Web.

## 1. Inicialización y Autenticación
1. Se levanta la instancia de `SeleniumBase` (SB) utilizando el parámetro `user_data_dir=perfil/profile 1`.
2. Al apuntar a esta carpeta, el bot recupera la sesión almacenada. Si es la primera vez, el usuario deberá escanear el código QR. Si ya ha sido escaneado, pasará directamente a los chats.
3. El bot carga `https://web.whatsapp.com/` y hace un `time.sleep` inicial de 15 segundos (o más, dependiendo de la conexión) para asegurar que el DOM de WhatsApp termine de renderizarse por completo.

## 2. Menú Interactivo de Pruebas
Una vez cargada la interfaz principal de WhatsApp, se libera la consola al usuario mostrando un menú interactivo. El navegador queda "esperando" las instrucciones por consola.

## 3. Acciones Disponibles

### Acción: Entrar a la pestaña Grupos
1. El bot busca el botón de filtros "Grupos" usando su XPath específico.
2. Si encuentra el elemento, usa inyección de JavaScript para hacer *Scroll* hasta el botón (`scrollIntoView`) y hace *Click* directamente mediante JS (`arguments[0].click()`), lo cual es menos susceptible a fallos visuales que un click normal.

### Acción: Imprimir títulos de los grupos
1. Se asume que el usuario ya se encuentra en la vista filtrada por grupos.
2. Se espera unos segundos para que se renderice la lista de chats.
3. Mediante una consulta XPath que busca `span` genéricos de títulos (`@dir="auto" and @title`), se recuperan todos los elementos visualizados.
4. Se itera la lista extrayendo el atributo `title` de cada elemento y se imprimen en consola.

### Acción: Entrar a un chat de grupo
1. Se le pide al usuario que digite el título del grupo (o una parte de él).
2. Se formatea el string XPath para buscar el `span` que coincida total o parcialmente con el texto usando `contains(@title, "{nombre_ingresado}")`.
3. El bot buscará el elemento. Si no lo encuentra, hará *Scroll* hacia abajo en el panel lateral hasta dar con él o llegar al final de la lista. Una vez encontrado, se hace *Click* (vía JS) en dicho elemento, abriendo el chat del lado derecho de la pantalla.

### Acción: Enviar mensaje a un chat abierto
1. Se requiere que exista un chat seleccionado (activo) en la pantalla.
2. Se localiza la caja de texto (chat input) buscando un div con atributo `contenteditable="true"` y el `data-testid` correspondiente a la barra de composición de mensaje.
3. Se hace *Click* ordinario sobre la caja de texto para darle el foco (Focus).
4. Se utiliza `send_keys(texto)` de Selenium para tipear el mensaje caracter por caracter, simulando que es un humano.
5. Inmediatamente, se localiza el botón con el icono de enviar (ícono de avioncito de papel, `aria-label="Enviar"`).
6. Se presiona el botón, concretando el envío en WhatsApp.
