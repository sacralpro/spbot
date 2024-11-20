import telebot
from telebot import types

TOKEN = '7813062295:AAFseqWrP3NwmCSdhGQ8TmJwA1Zjk-At0oI'  # Replace with your bot's token


bot = telebot.TeleBot(TOKEN)

# Global variables to store user language preferences and order details
user_language = {}
order_details = {}

# Replace with your Telegram User ID
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
    order_details[message.chat.id] = {}  # Initialize order details for the user

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
    item5 = types.KeyboardButton(text='Order Telegram Bot')  # Added new option
    markup.add(item1, item2, item3, item4, item5)
    return markup

def create_menu_ru():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(text='О компании Sacral Projects')
    item2 = types.KeyboardButton(text='Заказать сайт')
    item3 = types.KeyboardButton(text='Заказать мобильное приложение')
    item4 = types.KeyboardButton(text='Бесплатная консультация')
    item5 = types.KeyboardButton(text='Заказать Телеграм Бот')  # Added new option
    markup.add(item1, item2, item3, item4, item5)
    return markup

@bot.message_handler(func=lambda message: message.chat.id in user_language)
def menu_response(message):
    lang = user_language[message.chat.id]

    if lang == 'English':
        if message.text == 'Order Website':
            ask_name(message, lang)
        elif message.text == 'About Sacral Projects':
            bot.send_message(message.chat.id, "Sacral Projects is dedicated to delivering high-quality digital solutions (websites, mobile apps, telegram bots). We make people happy, clients successful, and businesses profitable.")
        elif message.text == 'Order Mobile App':
            ask_name(message, lang, is_mobile_app=True)
        elif message.text == 'Free Consultation':
            ask_name_for_consultation(message, lang)
        elif message.text == 'Order Telegram Bot':  # Handle the new option
            ask_bot_type(message, lang)

    elif lang == 'Русский':
        if message.text == 'Заказать сайт':
            ask_name(message, lang)
        elif message.text == 'О компании Sacral Projects':
            bot.send_message(message.chat.id, "Sacral Projects занимается разработкой качественных цифровых продуктов: веб-сайты, мобильные приложения, телеграм боты. Мы делаем людей счастливыми, клиентов успешными, бизнес прибыльным.")
        elif message.text == 'Заказать мобильное приложение':
            ask_name(message, lang, is_mobile_app=True)
        elif message.text == 'Бесплатная консультация':
            ask_name_for_consultation(message, lang)
        elif message.text == 'Заказать Телеграм Бот':  # Handle the new option
            ask_bot_type(message, lang)

def ask_bot_type(message, lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    standard_bot_button = types.KeyboardButton(text='Standard Bot (up to 4 menu items)')  # Changed to English
    unique_bot_button = types.KeyboardButton(text='Unique Bot')  # Changed to English
    markup.add(standard_bot_button, unique_bot_button)

    bot.send_message(message.chat.id, "Please choose the type of bot:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_bot_type_selection, lang)

def handle_bot_type_selection(message, lang):
    if lang == 'Русский':
        if message.text == 'Стандартный бот (до 4 пунктов меню)':
            ask_name_for_standard_bot(message, lang)
        elif message.text == 'Уникальный бот':
            bot.send_message(message.chat.id, "Ок, наш специалист свяжется с Вами.")  # Confirmation for unique bot in Russian
            start(message)  # Return to start
    else:  # English
        if message.text == 'Standard Bot (up to 4 menu items)':
            ask_name_for_standard_bot(message, lang)
        elif message.text == 'Unique Bot':
            bot.send_message(message.chat.id, "Okay, our specialist will contact you.")  # Confirmation for unique bot in English
            start(message)  # Return to start

def ask_name_for_standard_bot(message, lang):
    prompt = "Как вас зовут?" if lang == 'Русский' else "What is your name?"
    bot.send_message(message.chat.id, prompt)
    bot.register_next_step_handler(message, process_name_for_standard_bot, lang)

def process_name_for_standard_bot(message, lang):
    user_name = message.text
    order_details[message.chat.id]['name'] = user_name

    # Updated prompt for bot logic
    idea_prompt = "Опишите логику вашего бота (например: “В боте должно быть 3 кнопки меню(О компании, наши услуги, контакты), Услуги: заказать веб-сайт, заказать моб-приложение) и так далее.." if lang == 'Русский' else "Describe the logic of your bot (for example: “The bot should have 3 menu buttons (About Us, Our Services, Contact), Services: order a website, order a mobile app, etc..)"
    bot.send_message(message.chat.id, idea_prompt)
    bot.register_next_step_handler(message, process_logic_for_standard_bot, lang)

def process_logic_for_standard_bot(message, lang):
    order_details[message.chat.id]['logic'] = message.text
    user_name = order_details[message.chat.id]['name']

    # Confirmation message
    if lang == 'Русский':
        confirmation_message = "Благодарим, предварительная стоимость бота $50. Наш специалист свяжется с Вами."
    else:
        confirmation_message = "Thank you, the preliminary cost of the bot is $50. Our specialist will contact you."

    bot.send_message(message.chat.id, confirmation_message)

    # Send order details to the admin
    admin_message = f"Новый заказ от @{message.from_user.username}:\nИмя: {user_name}\nЛогика бота: {message.text}"
    bot.send_message(YOUR_USER_ID, admin_message)

    start(message)  # Return to start

def ask_name_for_consultation(message, lang):
    prompt = "Как вас зовут?" if lang == 'Русский' else "What is your name?"
    bot.send_message(message.chat.id, prompt)
    bot.register_next_step_handler(message, process_name_for_consultation, lang)

def process_name_for_consultation(message, lang):
    user_name = message.text
    order_details[message.chat.id]['name'] = user_name

    question_prompt = "Что вам подсказать?" if lang == 'Русский' else "What can I help you with?"
    bot.send_message(message.chat.id, question_prompt)
    bot.register_next_step_handler(message, process_question_for_consultation, user_name, lang)

def process_question_for_consultation(message, user_name, lang):
    user_question = message.text
    order_details[message.chat.id]['question'] = user_question

    # Send the admin the consultation request
    admin_message = f"Запрос на бесплатную консультацию от @{message.from_user.username}:\nИмя: {user_name}\nВопрос: {user_question}"
    
    # Send notification to admin
    bot.send_message(YOUR_USER_ID, admin_message)

    # Confirmation message to the user
    if lang == 'Русский':
        bot.send_message(message.chat.id, "Ваш запрос на консультацию принят! Мы свяжемся с вами в ближайшее время.")
    else:
        bot.send_message(message.chat.id, "Your consultation request has been accepted! We will contact you soon.")
    
    start(message)  # Return to start

@bot.message_handler(func=lambda message: message.text in ['Order Mobile App', 'Заказать мобильное приложение'])
def process_mobile_app_order(message):
    lang = user_language[message.chat.id]
    ask_name(message, lang, is_mobile_app=True)

def ask_name(message, lang, is_mobile_app=False):
    prompt = "Ваше Имя?" if lang == 'Русский' else "What is your name?"
    bot.send_message(message.chat.id, prompt)
    bot.register_next_step_handler(message, process_name, lang, is_mobile_app)

def process_name(message, lang, is_mobile_app):
    order_details[message.chat.id]['name'] = message.text
    # Updated prompt for app idea
    idea_prompt = "Опишите идею вашего приложения?" if lang == 'Русский' else "Please describe your app idea:"
    bot.send_message(message.chat.id, idea_prompt)
    bot.register_next_step_handler(message, process_idea, lang, is_mobile_app)

def process_idea(message, lang, is_mobile_app):
    order_details[message.chat.id]['idea'] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(text='1 неделя+') if lang == 'Русский' else types.KeyboardButton(text='1 week')
    item2 = types.KeyboardButton(text='1 месяц+') if lang == 'Русский' else types.KeyboardButton(text='1 month')
    item3 = types.KeyboardButton(text='Больше 1 месяца') if lang == 'Русский' else types.KeyboardButton(text='More than 1 month')
    markup.add(item1, item2, item3)

    if lang == 'Русский':
        bot.send_message(message.chat.id, "Желаемые сроки?", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Desired deadlines?", reply_markup=markup)

    bot.register_next_step_handler(message, process_deadline, lang, is_mobile_app)

def process_deadline(message, lang, is_mobile_app):
    order_details[message.chat.id]['deadline'] = message.text

    budget_prompt = "Выберите бюджет:\n$1000\n$3000\n$5000\n$10000" if lang == 'Русский' else "Choose your budget:\n$1000\n$3000\n$5000\n$10000"
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    budget_options = ['$1000+', '$3000+', '$5000+', '$10000+']  # Corrected budget options

    for option in budget_options:
        button = types.KeyboardButton(text=option)
        markup.add(button)

    bot.send_message(message.chat.id, budget_prompt, reply_markup=markup)
    bot.register_next_step_handler(message, process_budget, lang, is_mobile_app)

def process_budget(message, lang, is_mobile_app):
    order_details[message.chat.id]['budget'] = message.text

    user_name = order_details[message.chat.id]['name']
    user_username = message.from_user.username  # Get user's @username
    app_idea = order_details[message.chat.id]['idea']  # Updated for app
    deadline = order_details[message.chat.id]['deadline']
    budget = order_details[message.chat.id]['budget']

    # Admin notification
    if lang == 'Русский':
        admin_message = f"Новый заказ от @{user_username}:\n" \
                        f"Имя: {user_name}\n" \
                        f"Идея приложения: {app_idea}\n" \
                        f"Желаемые сроки: {deadline}\n" \
                        f"Бюджет: {budget}"
        confirmation_message = "Ваш заказ принят! Мы свяжемся с вами в ближайшее время."  # Confirmation message in Russian
    else:
        admin_message = f"New order from @{user_username}:\n" \
                        f"Name: {user_name}\n" \
                        f"App idea: {app_idea}\n" \
                        f"Desired deadlines: {deadline}\n" \
                        f"Budget: {budget}"
        confirmation_message = "Your order has been accepted! We will contact you soon."  # Confirmation message in English

    # Sending notification to admin
    bot.send_message(YOUR_USER_ID, admin_message)

    # Confirmation message to the user
    bot.send_message(message.chat.id, confirmation_message)

    start(message)  # Return to start

# Start the bot polling
bot.polling()
