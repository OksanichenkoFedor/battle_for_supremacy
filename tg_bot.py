import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from consts import HEX_COLORS, HEX_COLORS_NAMES, ADMIN_ID, HEX_COLORS_DICT

bot = telebot.TeleBot("token", parse_mode=None)
ids_colors = {}


COLOR_DATA = {
    'Красный': {'emoj':'🔴'},
    'Салатовый': {'emoj':'🟢'},
    'Синий': {'emoj':'🔵'},
    'Жёлтый': {'emoj':'🟡'},
    'Фиолетовый': {'emoj':'🟣'},
    'Бирюзовый': {'emoj':'🧪'}
}

id_to_color = {}
colors_used = []



def create_color_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2  # 2 кнопки в строке

    buttons = []
    for i in range(len(HEX_COLORS)):
        color_text = HEX_COLORS_NAMES[i] + " " + COLOR_DATA[HEX_COLORS_NAMES[i]]["emoj"]
        buttons.append(InlineKeyboardButton(color_text, callback_data=f"color_{i}"))

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
    #print(f"Пользователь {message.from_user.id} запустил бота")


# Обработчик нажатий на инлайн-кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_color_selection(call):
    # Извлекаем номер цвета из callback_data
    if call.data.startswith("color_"):
        color_index = int(call.data.split("_")[1])
        color_name = HEX_COLORS_NAMES[color_index]

        # Выводим информацию в консоль
        """
        print(f"=== Выбор цвета ===")
        print(f"ID пользователя: {call.from_user.id}")
        print(f"Имя: {call.from_user.first_name}")
        print(f"Фамилия: {call.from_user.last_name}")
        print(f"Username: @{call.from_user.username}")
        print(f"Номер кнопки: {color_index}")
        print(f"Цвет: {color_name}")
        print("=" * 30)
        """
        if color_name in colors_used:
            pass
        else:
            colors_used.append(color_name)
            COLOR_DATA[color_name]["id"] = call.from_user.id
            COLOR_DATA[color_name]["name"] = call.from_user.first_name+" "+call.from_user.last_name
            COLOR_DATA[color_name]["user_name"] = "@"+call.from_user.username
            COLOR_DATA[color_name]["color"] = HEX_COLORS[color_index]
            COLOR_DATA[color_name]["num_in_arr"] = HEX_COLORS_DICT[color_name]
            id_to_color[call.from_user.id] = color_name
            print(COLOR_DATA[color_name])
        for admin_name in ADMIN_ID:
            bot.send_message(
                ADMIN_ID[admin_name],
                f"Выбран цвет: {COLOR_DATA[color_name]["color"]}\n"
                f"Номер кнопки: {COLOR_DATA[color_name]["num_in_arr"]}\n"
                f"ID выбравшего: {COLOR_DATA[color_name]["id"]}\n"
                f"username выбравшего: {COLOR_DATA[color_name]["user_name"]}\n"
                f"Фамилия Имя выбравшего: {COLOR_DATA[color_name]["name"]}\n"
            )


# Обработчик текстовых сообщений (для демонстрации)
@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    if message.from_user.id in id_to_color:
        curr = COLOR_DATA[id_to_color[message.from_user.id]]
        for admin_name in ADMIN_ID:
            bot.send_message(
                ADMIN_ID[admin_name],
                "Пишет: "+curr["emoj"]+" "+curr["name"]+"\nТекст:\n"+
                message.text
            )
    elif message.from_user.id in ADMIN_ID.values():
        for user_id in id_to_color:
            bot.send_message(
                user_id,
                message.text
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