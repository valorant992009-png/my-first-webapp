import os
import json
from flask import Flask, send_from_directory
import telebot
from threading import Thread

# ==========================================
# 1. Настройка веб-сервера (Flask)
# ==========================================
app = Flask(__name__, static_folder='public', static_url_path='')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

def run_server():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# ==========================================
# 2. Настройка Telegram-бота (telebot)
# ==========================================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# ВАЖНО: Замени ' profile ' на то короткое имя (short name), 
# которое ты указал в BotFather в самом конце создания /newapp (Шаг 8)
APP_SHORT_NAME = "tetstss" 

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    # Удаляем к чертям все застрявшие старые клавиатуры с экрана
    remove_keyboard = telebot.types.ReplyKeyboardRemove(selective=False)
    
    # Получаем имя бота динамически, чтобы собрать правильную ссылку
    bot_username = bot.get_me().username
    # Собираем официальную ссылку на Mini App (t.me/имя_бота/короткое_имя_приложения)
    web_app_inline_url = f"https://t.me/{bot_username}/{APP_SHORT_NAME}"
    
    # Создаем ПРАВИЛЬНУЮ кнопку под сообщением, которая запускает Mini App, а не просто сайт
    inline_keyboard = telebot.types.InlineKeyboardMarkup()
    inline_button = telebot.types.InlineKeyboardButton(
        text="Заполнить анкету 🚀", 
        url=web_app_inline_url
    )
    inline_keyboard.add(inline_button)
    
    bot.send_message(
        message.chat.id, 
        "Привет! Нажми на кнопку ниже, чтобы открыть официальную анкету. Теперь данные прилетят 100%!", 
        reply_markup=inline_keyboard
    )

# Обработчик данных, которые приходят из формы авторизации Web App
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        data = json.loads(message.web_app_data.data)
        
        name = data.get('name')
        height = data.get('height')
        weight = data.get('weight')
        goal = data.get('goal')
        
        response_text = (
            f"🎉 **Профиль успешно заполнен!**\n\n"
            f"👤 **Имя:** {name}\n"
            f"📏 **Рост:** {height} см\n"
            f"⚖️ **Вес:** {weight} кг\n"
            f"🎯 **Цель:** {goal}\n\n"
            f"Наконец-то всё сработало как надо! Связка запущена. 💪"
        )
        
        bot.send_message(message.chat.id, response_text, parse_mode='Markdown')
        
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при обработке анкеты: {e}")


# ==========================================
# 3. Запуск всего приложения
# ==========================================
if __name__ == '__main__':
    server_thread = Thread(target=run_server)
    server_thread.start()
    
    print("Бот запущен...")
    bot.infinity_polling()
