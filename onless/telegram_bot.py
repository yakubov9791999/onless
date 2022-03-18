import os

import telegram

BOT_TOKEN = os.getenv('BOT_TOKEN')   #webdeveloperbot
BOT_URL = 'https://api.telegram.org/bot%s' % BOT_TOKEN
BOT_CHAT_ID = os.getenv('BOT_CHAT_ID') #Sirojiddin Yakubov ID

def send_message_to_developer(message):
    """
    only send message to backend developer
    """
    message = 'From Onless: ' + message
    bot = telegram.Bot(token=BOT_TOKEN)
    try:
        bot.sendMessage(BOT_CHAT_ID, text=message)
    except:
        pass
