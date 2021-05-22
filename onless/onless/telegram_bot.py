import telegram

BOT_TOKEN = '1546434372:AAEBWg1CQwIJl4-ItzsigwlEor5g4qhDops'   #webdeveloperbot
BOT_URL = 'https://api.telegram.org/bot%s' % BOT_TOKEN
BOT_CHAT_ID = '183551052' #Sirojiddin Yakubov ID

def send_message_to_developer(message):
    """
    only send message to backend developer
    """
    message = 'From Onless: ' + message
    bot = telegram.Bot(token=BOT_TOKEN)
    try:
        bot.sendMessage('183551052', text=message)
    except:
        pass
