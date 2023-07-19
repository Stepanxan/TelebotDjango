from .conf import bot
from telebot import types
from django.db import models


#База даних, таблиця реєстрації юзера
class UserProfile(models.Model):
    telegram_id = models.PositiveIntegerField(unique=True)
    username = models.CharField(max_length=256)
    balance_uah = models.DecimalField(max_digits=10, decimal_places=2)
    balance_usd = models.DecimalField(max_digits=10, decimal_places=2)
    balance_rub = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"User: {self.username}, ID: {self.telegram_id}"

    class Meta:
        db_table = "userprofile"

#База даних для історії транзакцій
class Transaction(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Transaction {self.id} for User: {self.user.username}, Amount: {self.amount}, Type: {self.transaction_type}"


#База даних історії покупок
class Purchase(models.Model):
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='purchases')
    seller = models.CharField(max_length=256)
    content = models.CharField(max_length=256)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer.username} купив(ла) від {self.seller}: {self.content} ({self.purchase_date})"

    class Meta:
        db_table = "purchase"

class Vertical():

    @staticmethod
    def choose_vertical(message):
        chat_id = message.chat.id

        # Створення клавіатури з кнопками вертикалей
        markup = types.ReplyKeyboardMarkup(row_width=1)
        btn_1 = types.KeyboardButton('🎰 гемблінг')
        btn_2 = types.KeyboardButton('⚽️ бетінг')
        btn_3 = types.KeyboardButton('🧘 нутра')
        btn_4 = types.KeyboardButton('🛒 товарка')
        btn_5 = types.KeyboardButton('💰 крипта')
        back = types.KeyboardButton('⬅️ Назад')
        markup.row(btn_1, btn_2, btn_3, btn_4, btn_5, back)
        bot.send_message(chat_id, 'Оберіть вертикаль:', reply_markup=markup)

    @staticmethod
    def handle_vertical(message):
        chat_id = message.chat.id
        vertical = message.text
        if message.text == '⬅️ Назад':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            btn_1 = types.KeyboardButton('🔢 Вибір вертикалі')
            btn_2 = types.KeyboardButton('👤 Особистий кабінет')
            markup.row(btn_1, btn_2)
            bot.send_message(message.chat.id, 'повернувся до вибору вертикалі', reply_markup=markup)
        else:
            bot.send_message(chat_id, f'Ви обрали вертикаль: {vertical}')


# Особистий кабінет
class Lk ():
    @staticmethod
    def choose_main_menu(message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(row_width=1)
        btn_1 = types.KeyboardButton('💰 Баланс')
        btn_2 = types.KeyboardButton('💳 Поповнення')
        btn_3 = types.KeyboardButton('🗂 Історія транзакцій')
        btn_4 = types.KeyboardButton('🛒 Мої покупки')
        btn_5 = types.KeyboardButton('⚙️ FAQ')
        btn_6 = types.KeyboardButton('🔨 Саппорт')
        back = types.KeyboardButton('⬅️ Назад')
        markup.row(btn_1, btn_2, btn_3, btn_4, btn_5, btn_6, back)
        bot.send_message(chat_id, '👤 Особистий кабінет', reply_markup=markup)


# Обробник натискання кнопок особистого кабінету
    @staticmethod
    def handle_main_menu(message):
        chat_id = message.chat.id
        vertical = message.text
        if message.text == '⬅️ Назад':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            btn_1 = types.KeyboardButton('🔢 Вибір вертикалі')
            btn_2 = types.KeyboardButton('👤 Особистий кабінет')
            markup.row(btn_1, btn_2)
            bot.send_message(message.chat.id, 'повернувся до головного меню', reply_markup=markup)
        elif message.text == '💰 Баланс':
            user = UserProfile.objects.get(telegram_id=message.from_user.id)
            balance_text = f"💰 Баланс:\n"
            balance_text += f"💴 Гривні (UAH): {user.balance_uah}\n"
            balance_text += f"💵 Долари (USD): {user.balance_usd}\n"
            balance_text += f"₽ Рублі (RUB): {user.balance_rub}\n"
            bot.send_message(chat_id, balance_text)
        else:
            bot.send_message(chat_id, f'Ви обрали: {vertical}')


#Обробка натискання кнопки "Поповнення"
    @staticmethod
    def payment_markup(message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(row_width=1)
        btn_1 = types.KeyboardButton('QIWI')
        btn_2 = types.KeyboardButton('Bitcoin')
        btn_3 = types.KeyboardButton('Перевід на картку')
        back = types.KeyboardButton('⬅️ Назад')
        markup.row(btn_1, btn_2, btn_3, back)
        bot.send_message(chat_id, 'Ви обрали спосіб оплати', reply_markup=markup)

    # Обробка типу оплати
    @staticmethod
    def handle_payment(message):
        chat_id = message.chat.id
        payment_method = message.text
        if payment_method in ['QIWI', 'Bitcoin', 'Перевід на картку']:
            bot.send_message(chat_id, f'Ви обрали спосіб оплати: {payment_method}')
            confirm_markup = types.ReplyKeyboardMarkup(row_width=1)
            btn_1 = types.KeyboardButton('✅ Підтвердити')
            back = types.KeyboardButton('⬅️ Назад')
            confirm_markup.row(btn_1, back)
            bot.send_message(chat_id, 'Натисніть кнопку Підтвердити для продовження', reply_markup=confirm_markup)
        elif message.text == '⬅️ Назад':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            btn_1 = types.KeyboardButton('🔢 Вибір вертикалі')
            btn_2 = types.KeyboardButton('👤 Особистий кабінет')
            markup.row(btn_1, btn_2)
            bot.send_message(message.chat.id, 'повернувся до головного меню', reply_markup=markup)
        else:
            bot.send_message(chat_id, 'Невірний вибір способу оплати.')

    # Обробка натискання кнопки " Історія транзакцій"
    @staticmethod
    def handle_transactions_history(message):
        chat_id = message.chat.id
        user = UserProfile.objects.get(telegram_id=message.from_user.id)
        transactions = Transaction.objects.filter(user=user).order_by('-timestamp')
        if transactions:
            transactions_text = "Історія транзакцій:\n"
            for transaction in transactions:
                transactions_text += f"\n 📋 Тип: {transaction.transaction_type}\n 💰 Сума: {transaction.amount}\n ⏱ Час: {transaction.timestamp}\n"
            bot.send_message(chat_id, transactions_text)
        else:
            bot.send_message(chat_id, "Історія транзакцій порожня.")


    @staticmethod
    # Обробка натискання кнопки "🛒 Мої покупки"
    def handle_my_purchases(message):
        chat_id = message.chat.id
        user = UserProfile.objects.get(telegram_id=message.from_user.id)
        purchases = Purchase.objects.filter(buyer=user).order_by('-purchase_date')
        if purchases:
            purchases_info = "🛒 Ваші покупки:\n"
            for purchase in purchases:
                seller_nickname = purchase.seller
                content = purchase.content
                purchase_date = purchase.purchase_date.strftime("%Y-%m-%d %H:%M:%S")
                purchases_info += f"\n 👤 Продавець: {seller_nickname}\n📦 Контент: {content}\n🕰 Дата покупки: {purchase_date}\n"
            bot.send_message(chat_id, purchases_info)
        else:
            bot.send_message(chat_id, "У вас ще немає покупок.")

    # Обробка натискання кнопки "FAQ"
    @staticmethod
    def handle_faq_button(message):
        chat_id = message.chat.id
        faq_message = "Відповіді на всі найчастіше задані повідомлення: "
        bot.send_message(chat_id, faq_message)


# Обробка натискання кнопки " Саппорт"
    @staticmethod
    def handle_support_button(message):
        chat_id = message.chat.id
        support_channel_id = "6170783158"
        support_link = f"https://t.me/c/{support_channel_id[4:]}"  # Посилання на канал саппорту
        bot.send_message(chat_id, f"Якщо у вас виникли питання або потрібна допомога, приєднуйтесь до нашого каналу саппорту VNV Solutions Bot: {support_link}")



class Gembling():

#Кнопка вибору гембінга
    @staticmethod
    def choose_gempling(message):
        chat_id = message.chat.id

        # Створення клавіатури з кнопками гембінга
        markup = types.ReplyKeyboardMarkup(row_width=1)
        btn_1 = types.KeyboardButton('🔴 ленд')
        btn_2 = types.KeyboardButton('🟠 преленд')
        btn_3 = types.KeyboardButton('🟢 тг бот')
        btn_4 = types.KeyboardButton('🔵 кастом')
        back = types.KeyboardButton('⬅️ Назад')
        markup.row(btn_1, btn_2, btn_3, btn_4, back)
        bot.send_message(chat_id, 'Оберіть тип гемблінга', reply_markup=markup)


# Обробник натискання кнопок гемблінга
    @staticmethod
    def handle_gembling(message):
        chat_id = message.chat.id
        vertical = message.text
        if message.text == '⬅️ Назад':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            btn_1 = types.KeyboardButton('🔢 Вибір вертикалі')
            btn_2 = types.KeyboardButton('👤 Особистий кабінет')
            markup.row(btn_1, btn_2)
            bot.send_message(message.chat.id, 'повернувся до головного меню', reply_markup=markup)
        else:
            bot.send_message(chat_id, f'Ви обрали гемблінг: {vertical}')


class Project():
    # Кнопка вибору кнопоки прикладу роботи і опису проекту
    @staticmethod
    def choose_project(message):
        chat_id = message.chat.id


        markup = types.ReplyKeyboardMarkup(row_width=1)
        btn_1 = types.KeyboardButton('💼 Приклад робіт і опис проекту')
        back = types.KeyboardButton('⬅️ Назад')
        markup.row(btn_1, back)
        bot.send_message(chat_id, f'Ви обрали: {message.text}', reply_markup=markup)

    # Обробник натискання кнопоки прикладу роботи і опису проекту
    @staticmethod
    def handle_project(message):
        chat_id = message.chat.id
        vertical = message.text
        if message.text == '⬅️ Назад':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            btn_1 = types.KeyboardButton('🔢 Вибір вертикалі')
            btn_2 = types.KeyboardButton('👤 Особистий кабінет')
            markup.row(btn_1, btn_2)
            bot.send_message(message.chat.id, 'повернувся до вибору вертикалі', reply_markup=markup)
        else:
            bot.send_message(chat_id, f'Ви обрали приклад роботи і опису проекту: {vertical}')


class Upplybutton():

    # Кнопка вибору кнопоки кнопка оплати
    @staticmethod
    def choose_button(message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(row_width=1)
        btn_1 = types.KeyboardButton('💳 кнопка оплати')
        back = types.KeyboardButton('⬅️ Назад')
        markup.row(btn_1,back)
        bot.send_message(chat_id, 'Виберіть кнопку оплати', reply_markup=markup)

    # Обробник натискання кнопоки кнопка оплати
    @staticmethod
    def handle_button(message):
        chat_id = message.chat.id
        vertical = message.text
        if message.text == '⬅️ Назад':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            btn_1 = types.KeyboardButton('🔢 Вибір вертикалі')
            btn_2 = types.KeyboardButton('👤 Особистий кабінет')
            markup.row(btn_1, btn_2)
            bot.send_message(message.chat.id, 'повернувся до вибору вертикалі', reply_markup=markup)
        else:
            bot.send_message(chat_id, f'Ви обрали: {vertical}')


class WrittenOffBalance():

    # Кнопка вибору кнопоки списання балансу
    @staticmethod
    def choose_written_off_balance(message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(row_width=1)
        btn_1 = types.KeyboardButton('💸 Списання балансу')
        back = types.KeyboardButton('⬅️ Назад')
        markup.row(btn_1, back)
        bot.send_message(chat_id, 'Підтвердіть списання балансу', reply_markup=markup)

    # Обробник натискання кнопоки списання балансу
    @staticmethod
    def handle_written_off_balance(message):
        chat_id = message.chat.id
        vertical = message.text
        if message.text == '⬅️ Назад':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            btn_1 = types.KeyboardButton('🔢 Вибір вертикалі')
            btn_2 = types.KeyboardButton('👤 Особистий кабінет')
            markup.row(btn_1, btn_2)
            bot.send_message(message.chat.id, 'повернувся до вибору вертикалі', reply_markup=markup)
        else:
            bot.send_message(chat_id, f'Ви обрали: {vertical}')


class Product():

    # Кнопка вибору кнопоки продукт і всі його комплетуючі разом з мануалом
    @staticmethod
    def choose_product(message):
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(row_width=1)
        btn_1 = types.KeyboardButton('продукт і всі його комплетуючі разом з мануалом')
        back = types.KeyboardButton('⬅️ Назад')
        markup.row(btn_1, back)
        bot.send_message(chat_id, 'продукт і всі його комплетуючі разом з мануалом', reply_markup=markup)

    # Обробник натискання продукт і всі його комплетуючі разом з мануалом
    @staticmethod
    def handle_product(message):
        chat_id = message.chat.id
        vertical = message.text
        if message.text == '⬅️ Назад':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            btn_1 = types.KeyboardButton('🔢 Вибір вертикалі')
            btn_2 = types.KeyboardButton('👤 Особистий кабінет')
            markup.row(btn_1, btn_2)
            bot.send_message(message.chat.id, 'повернувся до вибору вертикалі', reply_markup=markup)
        else:
            bot.send_message(chat_id, f'Ви обрали: {vertical}')

