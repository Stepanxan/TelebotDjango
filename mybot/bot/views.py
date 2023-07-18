import telebot
from django.http import HttpResponse
from telebot import types
from django.views.decorators.csrf import csrf_exempt
from .conf import bot
from .models import Vertical, Gembling, Project, Upplybutton, WrittenOffBalance, Product, Lk, Transaction

@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])
        return HttpResponse('')
    return HttpResponse('Invalid request method')


#Посилання на телеграм канал з закладеною провіркою на те чи підписався мембер на канал
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    first_name = message.chat.first_name
    bot.send_message(chat_id, f"Привіт {first_name} !/n"
                                f"Підпишись на наш телеграм канал", reply_markup=start_markup())
    if start_markup():
        markup = types.ReplyKeyboardMarkup(row_width=1)
        btn_1 = types.KeyboardButton('🔢 Вибір вертикалі')
        btn_2 = types.KeyboardButton('👤 Особистий кабінет')
        markup.row(btn_1, btn_2)
        bot.send_message(chat_id, 'Ви успішно підписалися на канал!', reply_markup=markup)
        bot.register_next_step_handler(message, choose_vertical, choose_main_menu)
    else:
        bot.send_message(chat_id, 'Будь ласка, спочатку підпишіться на канал.')


def start_markup():
    markup = types.InlineKeyboardMarkup(row_width=True)
    link_keyboard = types.InlineKeyboardButton(text="Підпишись на наш телеграм канал", url='https://web.telegram.org/a/#-1946488565')
    check_keyboard = types.InlineKeyboardButton(text="Провірити", callback_data="check")
    markup.add(link_keyboard, check_keyboard)
    return markup


def check(call):
    status = ['creator', 'administrator', 'member']
    if bot.get_chat_member(chat_id='-1001946488565', user_id=call.message.chat.id).status in status:
        bot.send_message(call.message.chat.id, "Дякую за підписку!", reply_markup=start_markup())
    else:
        bot.send_message(call.message.chat.id, "Підпишіться на телеграм канал!", reply_markup=start_markup())



#Кнопка вибору вертикалі
@bot.message_handler(func=lambda message: message.text == '🔢 Вибір вертикалі')
def choose_vertical(message):
    Vertical.choose_vertical(message)


#Кнопка вибору ЛК
@bot.message_handler(func=lambda message: message.text == '👤 Особистий кабінет')
def choose_main_menu(message):
    Lk.choose_main_menu(message)


#Кнопка вибору гемблінга
@bot.message_handler(func=lambda message: message.text == '🎰 гемблінг')
def choose_gembling(message):
    Gembling.choose_gempling(message)



#Кнопка вибору кнопоки прикладу роботи і опису проекту
@bot.message_handler(func=lambda message: message.text in ['🔴 ленд','🟠 преленд','🟢 тг бот', '🔵 кастом'])
def choose_project(message):
    Project.choose_project(message)


#Кнопка вибору кнопоки оплати
@bot.message_handler(func=lambda message: message.text == '💼 Приклад робіт і опис проекту')
def choose_button(message):
    Upplybutton.choose_button(message)

#Кнопка вибору кнопоки списання балансу
@bot.message_handler(func=lambda message: message.text == '💳 кнопка оплати')
def choose_written_off_balance(message):
    WrittenOffBalance.choose_written_off_balance(message)

#Кнопка вибору кнопоки продукт
@bot.message_handler(func=lambda message: message.text == '💸 Списання балансу')
def choose_product(message):
    Product.choose_product(message)



# Обробник натискання кнопки " Історія транзакцій"
@bot.message_handler(func=lambda message: message.text == '🗂 Історія транзакцій')
def handle_transactions_button(message):
    Lk.handle_transactions_history(message)


# Обробка натискання кнопки "🛒 Мої покупки"
@bot.message_handler(func=lambda message: message.text == '🛒 Мої покупки')
def handle_my_purchases(message):
    Lk.handle_my_purchases(message)


# Обробка натискання кнопки "🛒 Мої покупки"
@bot.message_handler(func=lambda message: message.text == '🛒 Мої покупки')
def handle_my_purchases(message):
    chat_id = message.chat.id
    user = UserProfile.objects.get(telegram_id=message.from_user.id)
    purchase_history = get_purchase_history(user)
    if not purchase_history:
        bot.send_message(chat_id, "У вас ще немає покупок.")
    else:
        purchases_info = "🛍️ Ваші покупки:\n"
        for purchase in purchase_history:
            purchases_info += f"{purchase}\n"

        bot.send_message(chat_id, purchases_info)

# Обробка натискання кнопки "Саппорт"
@bot.message_handler(func=lambda message: message.text == '🔨 Саппорт')
def handle_support(message):
    Lk.handle_support_button(message)

# Обробка натискання кнопки "FAQ"
@bot.message_handler(func=lambda message: message.text == '⚙️ FAQ')
def handle_faq_button(message):
    Lk.handle_faq_button(message)


# Обробник натискання кнопок вертикалей
@bot.message_handler(func=lambda message: message.text in ['🎰 гемблінг', '⚽️ бетінг', '🧘 нутра', '🛒 товарка', '💰 крипта', '⬅️ Назад'])
def handle_vertical(message):
    Vertical.handle_vertical(message)


# Обробник натискання кнопоки особистий кабінет
@bot.message_handler(func=lambda message: message.text in ['💰 Баланс','💳 Поповнення','🗂 Історія транзакцій', '🛒 Мої покупки', '⚙️ FAQ', '🔨 Саппорт', '⬅️ Назад'])
def handle_main_menu(message):
    Lk.handle_main_menu(message)


# Обробник натискання кнопок гемблінга
@bot.message_handler(func=lambda message: message.text in ['🔴 ленд','🟠 преленд','🟢 тг бот', '🔵 кастом'])
def handle_gembling(message):
    Gembling.handle_gembling(message)



# Обробник натискання кнопоки прикладу роботи і опису проекту
@bot.message_handler(func=lambda message: message.text in ['💼 приклад роботи і опису проекту'])
def handle_project(message):
    Project.handle_project(message)


#Обробник натискання кнопоки оплати
@bot.message_handler(func=lambda message: message.text in ['💳 кнопка оплати'])
def handle_button(message):
    Upplybutton.handle_button(message)


#Обробник натискання списання балансу
@bot.message_handler(func=lambda message: message.text in ['💸 списання балансу'])
def handle_written_off_balance(message):
    WrittenOffBalance.handle_written_off_balance(message)


#Обробник натискання продукт
@bot.message_handler(func=lambda message: message.text in ['продукт і всі його комплетуючі разом з мануалом'])
def handle_product(message):
    Product.handle_product(message)