import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot("7947796403:AAGIFYeh-VGlN3f-guPPBMg2APV1tAQyEDU", parse_mode=None)
ids_colors = {}


# Цвета для выбора (те же что и в Pygame)
HEX_COLORS = [
    "🔴 Красный",
    "🟢 Салатовый",
    "🟣 Фиолетовый",
    "🔵 Синий",
    "🟠 Оранжевый",
    "🩵 Бирюзовый"
]


# Создаем клавиатуру с кнопками цветов
def create_color_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2  # 2 кнопки в строке

    buttons = []
    for i, color in enumerate(HEX_COLORS):
        buttons.append(InlineKeyboardButton(color, callback_data=f"color_{i}"))

    # Распределяем кнопки по строкам (по 2 в каждой)
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.add(buttons[i], buttons[i + 1])
        else:
            markup.add(buttons[i])

    return markup


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
    Выберете цвет вашей команды

    Выберите один из доступных цветов:
    """
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=create_color_keyboard()
    )
    print(f"Пользователь {message.from_user.id} запустил бота")


# Обработчик нажатий на инлайн-кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_color_selection(call):
    # Извлекаем номер цвета из callback_data
    if call.data.startswith("color_"):
        color_index = int(call.data.split("_")[1])
        color_name = HEX_COLORS[color_index]

        # Выводим информацию в консоль
        print(f"=== Выбор цвета ===")
        print(f"ID пользователя: {call.from_user.id}")
        print(f"Имя: {call.from_user.first_name}")
        print(f"Фамилия: {call.from_user.last_name}")
        print(f"Username: @{call.from_user.username}")
        print(f"Номер кнопки: {color_index}")
        print(f"Цвет: {color_name}")
        print("=" * 30)

        # Отправляем подтверждение пользователю
        bot.answer_callback_query(
            call.id,
            f"Вы выбрали: {color_name}",
            show_alert=False
        )

        # Обновляем сообщение или отправляем новое
        bot.send_message(
            call.message.chat.id,
            f"🎉 Отлично! Вы выбрали: {color_name}\n"
            f"📝 Номер кнопки: {color_index}\n"
            f"🆔 Ваш ID: {call.from_user.id}"
        )


# Обработчик текстовых сообщений (для демонстрации)
@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    if message.text != '/start':
        bot.reply_to(
            message,
            "Используйте команду /start для выбора цвета"
        )

'''
@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    # Выводим информацию о сообщении в консоль
    print(f"=== Новое сообщение ===")
    print(f"Время: {message.date}")
    print(f"ID пользователя: {message.from_user.id}")
    print(f"Имя: {message.from_user.first_name}")
    print(f"Фамилия: {message.from_user.last_name}")
    print(f"Username: @{message.from_user.username}")
    print(f"Текст сообщения: {message.text}")
    print("=" * 30)
'''
bot.polling()