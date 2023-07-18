import telebot

# Ваш токен Telegram-бота
TOKEN = '6322977859:AAHuQBiddHs0KUOgffgGSuHGTnLrxyAabfI'

# Ініціалізуємо телеграм-бота
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Бот підключений та працює.')


if __name__ == '__main__':
    bot.polling()