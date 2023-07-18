from time import sleep

import telebot
from django.conf import settings

TOKEN = '6322977859:AAHuQBiddHs0KUOgffgGSuHGTnLrxyAabfI'

# Ініціалізуємо телеграм-бота
bot = telebot.TeleBot(TOKEN)


# Встановлюємо вебхук
bot.remove_webhook()
sleep(1)
bot.set_webhook(url=settings.WEBHOOK_URL)