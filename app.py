import telebot
from telebot import types

TOKEN = '7813062295:AAFseqWrP3NwmCSdhGQ8TmJwA1Zjk-At0oI'  # Замените токен на токен вашего бота

bot = telebot.TeleBot(TOKEN)

# Глобальные переменные для хранения предпочтений языков пользователей и деталей заказа
user_language = {}
order_details = {}

# Замените на ваш Telegram User ID
YOUR_USER_ID = 653154396  # Замените на ваш Telegram User ID

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(text='Русский')
    item2 = types.KeyboardButton(text='English')
    
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Please choose your language / Пожалуйста, выберите язык:", reply_markup=markup)

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
    item4 = types.KeyboardButton(text='Order Design')
    
    markup.add(item1, item2, item3, item4)
    return markup

def create_menu_ru():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(text='О компании Sacral Projects')
    item2 = types.KeyboardButton(text='Заказать сайт')
    item3 = types.KeyboardButton(text='Заказать мобильное приложение')
    item4 = types.KeyboardButton(text='Заказать дизайн')
    
    markup.add(item1, item2, item3, item4)
    return markup

@bot.message_handler(func=lambda message: message.chat.id in user_language)
def menu_response(message):
    lang = user_language[message.chat.id]
    
    if lang == 'English':
        if message.text == 'Order Website':
            ask_name(message, lang)
        elif message.text == 'About Sacral Projects':
            bot.send_message(message.chat.id, "Sacral Projects is dedicated to delivering high-quality digital solutions...")
        elif message.text == 'Order Mobile App':
            ask_name(message, lang, is_mobile_app=True)
            
    elif lang == 'Русский':
        if message.text == 'Заказать сайт':
            ask_name(message, lang)
        elif message.text == 'О компании Sacral Projects':
            bot.send_message(message.chat.id, "Sacral Projects занимается предоставлением качественных цифровых решений...")
        elif message.text == 'Заказать мобильное приложение':
            ask_name(message, lang, is_mobile_app=True)

def ask_name(message, lang, is_mobile_app=False):
    prompt = "Ваше Имя?" if lang == 'Русский' else "What is your name?"
    bot.send_message(message.chat.id, prompt)
    bot.register_next_step_handler(message, process_name, lang, is_mobile_app)

def process_name(message, lang, is_mobile_app):
    order_details[message.chat.id]['name'] = message.text
    idea_prompt = "Опишите идею вашего сайта?" if lang == 'Русский' else "Please describe your website idea:"
    bot.send_message(message.chat.id, idea_prompt)
    bot.register_next_step_handler(message, process_idea, lang, is_mobile_app)

def process_idea(message, lang, is_mobile_app):
    order_details[message.chat.id]['idea'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(text='1 неделя') if lang == 'Русский' else types.KeyboardButton(text='1 week')
    item2 = types.KeyboardButton(text='1 месяц') if lang == 'Русский' else types.KeyboardButton(text='1 month')
    item3 = types.KeyboardButton(text='Больше 1 месяца') if lang == 'Русский' else types.KeyboardButton(text='More than 1 month')
    
    markup.add(item1, item2, item3)
    
    if lang == 'Русский':
        bot.send_message(message.chat.id, "Желаемые сроки?", reply_markup=markup)  # Asking for deadlines in Russian
    else:
        bot.send_message(message.chat.id, "Desired deadlines?", reply_markup=markup)  # Asking for deadlines in English

    bot.register_next_step_handler(message, process_deadline, lang, is_mobile_app)

def process_deadline(message, lang, is_mobile_app):
    # Сохраняем данные о заказе
    order_details[message.chat.id]['deadline'] = message.text
    
    # Запрос бюджета
    budget_prompt = "Выберите бюджет:\n$1000\n$3000\n$5000\n$10000" if lang == 'Русский' else "Choose your budget:\n$1000\n$3000\n$5000\n$10000"
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    budget_options = ['$1000', '$3000', '$5000', '$10000']
    
    for option in budget_options:
        button = types.KeyboardButton(text=option)
        markup.add(button)
    
    bot.send_message(message.chat.id, budget_prompt, reply_markup=markup)
    bot.register_next_step_handler(message, process_budget, lang, is_mobile_app)

def process_budget(message, lang, is_mobile_app):
    order_details[message.chat.id]['budget'] = message.text
    
    # Собираем данные для отправки админу
    user_name = order_details[message.chat.id]['name']
    user_username = message.from_user.username  # Получение @username пользователя
    website_idea = order_details[message.chat.id]['idea']
    deadline = order_details[message.chat.id]['deadline']
    budget = order_details[message.chat.id]['budget']

    # Формируем сообщение для отправки админу
    if lang == 'Русский':
        admin_message = f"Новый заказ от @{user_username}:\n" \
                        f"Имя: {user_name}\n" \
                        f"Идея сайта: {website_idea}\n" \
                        f"Желаемые сроки: {deadline}\n" \
                        f"Бюджет: {budget}"
        confirmation_message = "Ваш заказ принят! Мы свяжемся с вами в ближайшее время."  # Confirmation message in Russian
    else:
        admin_message = f"New order from @{user_username}:\n" \
                        f"Name: {user_name}\n" \
                        f"Idea for the website: {website_idea}\n" \
                        f"Desired deadlines: {deadline}\n" \
                        f"Budget: {budget}"
        confirmation_message = "Your order has been accepted! We will contact you soon."  # Confirmation message in English

    # Отправка уведомления админу
    bot.send_message(YOUR_USER_ID, admin_message)
    
    # Подтверждение заказа пользователю
    bot.send_message(message.chat.id, confirmation_message)

# Обработка заказа для мобильного приложения аналогично
@bot.message_handler(func=lambda message: message.text in ['Order Mobile App', 'Заказать мобильное приложение'])
def process_mobile_app_order(message):
    lang = user_language[message.chat.id]
    ask_name(message, lang, is_mobile_app=True)

# Запускаем бота
bot.polling()
