import telebot
from telebot import types

TOKEN = '7813062295:AAFseqWrP3NwmCSdhGQ8TmJwA1Zjk-At0oI'  # Replace with you r bot's token

bot = telebot.TeleBot(TOKEN)

# Глобальные переменные для хранения языковых предпочтений и условий заказов пользователей
user_language = {}
order_details = {}

# Замените на ваш Telegram User ID
YOUR_USER_ID = 653154396 

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(text='Русский')
    item2 = types.KeyboardButton(text='English')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Пожалуйста, выберите язык / Please choose your language:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['Русский', 'English'])
def set_language(message):
    user_language[message.chat.id] = message.text
    order_details[message.chat.id] = {}  # Инициализация деталей заказа для пользователя

    if message.text == 'Русский':
        reply_markup = create_menu_ru()
        bot.send_message(message.chat.id, "Вы выбрали русский язык. Вот ваше меню:", reply_markup=reply_markup)
    else:
        reply_markup = create_menu_en()
        bot.send_message(message.chat.id, "You have chosen English. Here is your menu:", reply_markup=reply_markup)

def create_menu_en():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(text='About Sacral Projects')
    item2 = types.KeyboardButton(text='Order Website')
    item3 = types.KeyboardButton(text='Order Mobile App')
    item4 = types.KeyboardButton(text='Free Consultation')
    item5 = types.KeyboardButton(text='Order Telegram Bot')  # Опция для заказа бота
    markup.add(item1, item2, item3, item4, item5)
    return markup

def create_menu_ru():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(text='О компании Sacral Projects')
    item2 = types.KeyboardButton(text='Заказать сайт')
    item3 = types.KeyboardButton(text='Заказать мобильное приложение')
    item4 = types.KeyboardButton(text='Бесплатная консультация')
    item5 = types.KeyboardButton(text='Заказать Телеграм Бот')  # Опция для заказа бота
    markup.add(item1, item2, item3, item4, item5)
    return markup

@bot.message_handler(func=lambda message: message.chat.id in user_language)
def menu_response(message):
    lang = user_language[message.chat.id]

    if lang == 'English':
        if message.text == 'Order Website':
            ask_name(message, lang, is_mobile_app=False)
        elif message.text == 'About Sacral Projects':
            bot.send_message(message.chat.id, "Sacral Projects is dedicated to delivering high-quality digital solutions (websites, mobile apps, telegram bots). We make people happy, clients successful, and businesses profitable.")
        elif message.text == 'Order Mobile App':
            ask_name(message, lang, is_mobile_app=True)
        elif message.text == 'Free Consultation':
            ask_name_for_consultation(message, lang)
        elif message.text == 'Order Telegram Bot':
            ask_bot_type(message, lang)  # Запрос типа бота

    elif lang == 'Русский':
        if message.text == 'Заказать сайт':
            ask_name(message, lang, is_mobile_app=False)  # Убедитесь, что используется правильная логика
        elif message.text == 'О компании Sacral Projects':
            bot.send_message(message.chat.id, "Sacral Projects занимается разработкой качественных цифровых продуктов: веб-сайты, мобильные приложения, телеграм боты. Мы делаем людей счастливее, клиентов успешными, бизнес прибыльным.")
        elif message.text == 'Заказать мобильное приложение':
            ask_name(message, lang, is_mobile_app=True)
        elif message.text == 'Бесплатная консультация':
            ask_name_for_consultation(message, lang)
        elif message.text == 'Заказать Телеграм Бот':
            ask_bot_type(message, lang)  # Запрос типа бота

# Запрос имени для сайта или приложения
def ask_name(message, lang, is_mobile_app=False):
    prompt = "Ваше Имя?" if lang == 'Русский' else "What is your name?"
    bot.send_message(message.chat.id, prompt)
    bot.register_next_step_handler(message, process_name, lang, is_mobile_app)

def process_name(message, lang, is_mobile_app):
    order_details[message.chat.id]['name'] = message.text
    idea_prompt = (
        "Опишите идею вашего сайта?" if not is_mobile_app else "Опишите идею вашего приложения?" 
        if lang == 'Русский' else 
        "Please describe your website idea?" if not is_mobile_app else "Please describe your app idea:"
    )
    bot.send_message(message.chat.id, idea_prompt)
    bot.register_next_step_handler(message, process_idea, lang, is_mobile_app)

def process_idea(message, lang, is_mobile_app):
    order_details[message.chat.id]['idea'] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(text='1 неделя+') if lang == 'Русский' else types.KeyboardButton(text='1 week+')
    item2 = types.KeyboardButton(text='1 месяц+') if lang == 'Русский' else types.KeyboardButton(text='1 month+')
    item3 = types.KeyboardButton(text='Больше 1 месяца') if lang == 'Русский' else types.KeyboardButton(text='More than 1 month')
    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, "Желаемые сроки?" if lang == 'Русский' else "Desired deadlines?", reply_markup=markup)
    bot.register_next_step_handler(message, process_deadline, lang, is_mobile_app)

# Запрос и обработка бюджета и других деталей заказа
def process_deadline(message, lang, is_mobile_app):
    order_details[message.chat.id]['deadline'] = message.text

    budget_prompt = (
        "Выберите бюджет:\n$1000\n$3000\n$5000\n$10000"
        if lang == 'Русский'
        else "Choose your budget:\n$1000\n$3000\n$5000\n$10000"
    )
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    budget_options = ['$1000+', '$3000+', '$5000+', '$10000+']

    for option in budget_options:
        button = types.KeyboardButton(text=option)
        markup.add(button)

    bot.send_message(message.chat.id, budget_prompt, reply_markup=markup)
    bot.register_next_step_handler(message, process_budget, lang, is_mobile_app)

def process_budget(message, lang, is_mobile_app):
    order_details[message.chat.id]['budget'] = message.text

    user_name = order_details[message.chat.id]['name']
    user_username = message.from_user.username  # Получение @username пользователя
    app_idea = order_details[message.chat.id]['idea']
    deadline = order_details[message.chat.id]['deadline']
    budget = order_details[message.chat.id]['budget']

    admin_message = (
        f"Новый заказ от @{user_username}:\nИмя: {user_name}\nИдея {'сайта' if not is_mobile_app else 'приложения'}: {app_idea}\nЖелаемые сроки: {deadline}\nБюджет: {budget}"
        if lang == 'Русский' 
        else f"New order from @{user_username}:\nName: {user_name}\nIdea {'of website' if not is_mobile_app else 'for the app'}: {app_idea}\nDesired deadlines: {deadline}\nBudget: {budget}"
    )

    confirmation_message = (
        "Ваш заказ принят! Мы свяжемся с вами в ближайшее время."
        if lang == 'Русский' 
        else "Your order has been accepted! We will contact you soon."
    )

    # Отправка уведомления администратору
    bot.send_message(YOUR_USER_ID, admin_message)

    # Подтверждение заказа пользователю
    bot.send_message(message.chat.id, confirmation_message)

    start(message)  # Возврат к началу

# Функции заказа бота и консультаций остаются без изменений

@bot.message_handler(func=lambda message: message.text in ['Заказать_mobile_app', 'Заказать Телеграм Бот'])
def ask_bot_type(message):
    lang = user_language[message.chat.id]
    if message.text == 'Заказать Телеграм Бот':
        handle_telegram_bot_order(message, lang)
    # Здесь можно добавить логику для обработки заказа мобильного приложения

def handle_telegram_bot_order(message, lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    standard_bot_button = types.KeyboardButton(text='Стандартный бот (до 4 пунктов меню)')
    unique_bot_button = types.KeyboardButton(text='Уникальный бот')
    markup.add(standard_bot_button, unique_bot_button)

    bot.send_message(message.chat.id, "Пожалуйста, выберите тип бота:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_bot_type_selection, lang)

def handle_bot_type_selection(message, lang):
    if lang == 'Русский':
        if message.text == 'Стандартный бот (до 4 пунктов меню)':
            ask_name_for_bot(message, lang, is_standard_bot=True)
        elif message.text == 'Уникальный бот':
            bot.send_message(message.chat.id, "Ок, наш специалист свяжется с вами.")
            start(message)  # Возврат к началу
    else:  # English
        if message.text == 'Standard Bot (up to 4 menu items)':
            ask_name_for_bot(message, lang, is_standard_bot=True)
        elif message.text == 'Unique Bot':
            bot.send_message(message.chat.id, "Okay, our specialist will contact you.")
            start(message)  # Return to start

def ask_name_for_bot(message, lang, is_standard_bot):
    prompt = "Как вас зовут?" if lang == 'Русский' else "What is your name?"
    bot.send_message(message.chat.id, prompt)
    bot.register_next_step_handler(message, process_name_for_bot, lang)

def process_name_for_bot(message, lang):
    user_name = message.text
    order_details[message.chat.id]['name'] = user_name

    idea_prompt = (
        "Опишите логику вашего бота?" 
        if lang == 'Русский' else 
        "Please describe the logic of your bot:"
    )
    bot.send_message(message.chat.id, idea_prompt)
    bot.register_next_step_handler(message, process_logic_for_bot, lang)

def process_logic_for_bot(message, lang):
    order_details[message.chat.id]['logic'] = message.text
    user_name = order_details[message.chat.id]['name']

    confirmation_message = (
        "Благодарим, наш специалист свяжется с вами." 
        if lang == 'Русский' 
        else "Thank you, our specialist will contact you."
    )
    bot.send_message(message.chat.id, confirmation_message)

    # Уведомление администратору
    admin_message = (
        f"Новый заказ бота от @{message.from_user.username}:\nИмя: {user_name}\nЛогика: {message.text}"
        if lang == 'Русский' 
        else f"New bot order from @{message.from_user.username}:\nName: {user_name}\nLogic: {message.text}"
    )
    bot.send_message(YOUR_USER_ID, admin_message)

    start(message)  # Возврат к началу

# Запускаем бота
bot.polling()
