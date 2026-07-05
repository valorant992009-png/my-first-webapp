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

# Твоя уникальная ссылка на Render
WEB_APP_URL = "https://my-first-webapp-dro4.onrender.com"

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    # Принудительно очищаем старые обычные клавиатуры, если они где-то остались
    remove_keyboard = telebot.types.ReplyKeyboardRemove(selective=False)
    
    # Создаем красивую Inline-кнопку под сообщением (данные из нее передаются отлично!)
    inline_keyboard = telebot.types.InlineKeyboardMarkup()
    web_app_info = telebot.types.WebAppInfo(WEB_APP_URL)
    inline_button = telebot.types.InlineKeyboardButton(text="Заполнить анкету 🚀", web_app=web_app_info)
    inline_keyboard.add(inline_button)
    
    bot.send_message(
        message.chat.id, 
        "Привет! Нажми на кнопку ниже, чтобы открыть анкету и заполнить свой профиль. Это быстро и удобно! 👇", 
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
            f"Всё сработало идеально, данные у меня! 💪"
        )
        
        bot.send_message(message.chat.id, response_text, parse_mode='Markdown')
        
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при обработке анкеты: {e}")


# ==========================================
# 3. Запуск всего приложения
# ==========================================
if __name__ == '__main__':
    server_thread = Thread(target=run_server)
    server_thread.start()
    
    print("Бот запущен и готов к работе...")
    bot.infinity_polling()
