class WhatsappSelectors:
    # ==========================================
    # NAVEGACIÓN Y FILTROS
    # ==========================================
    GRUPOS_BUTTON = '//span[text()="Grupos"]'
    
    # ==========================================
    # LISTA DE CHATS
    # ==========================================
    # Selector genérico que captura los spans que contienen los títulos de los grupos
    TITULOS_GRUPOS = '//span[@dir="auto" and @title and contains(@class, "x1iyjqo2")]'
    
    # Selecciona el contenedor de la fila (row) del grupo, buscando por su título o parte de él
    GRUPO_ESPECIFICO = '//div[@role="row" and .//span[@dir="auto" and contains(@title, "{}") and contains(@class, "x1iyjqo2")]]'
    
    # ==========================================
    # VENTANA DE CHAT (MENSAJES)
    # ==========================================
    # Selector genérico para la barra donde se escribe el mensaje
    CHAT_INPUT = '//div[@data-testid="conversation-compose-box-input" and @contenteditable="true"]'
    
    # Selector específico para la barra de mensajes en grupos (usar .format(nombre_grupo))
    CHAT_INPUT_GRUPO = '//div[@aria-label="Escribir un mensaje para el grupo {}"]'
    
    # Selectores para el botón de enviar mensaje
    SEND_BUTTON = '//button[@aria-label="Enviar"]'
    SEND_BUTTON_ICON = '//span[@data-icon="wds-ic-send-filled"]'
