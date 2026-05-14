from bot_sb import WhatsappBot

def main():
    USER_DATA_DIR = r"perfil/profile 1"
    
    print("INICIANDO BOT DE WHATSAPP...")
    bot = WhatsappBot(user_data_dir=USER_DATA_DIR)
    bot.run()

if __name__ == "__main__":
    main()