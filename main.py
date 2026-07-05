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

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    web_app_url = "https://my-first-webapp-dro4.onrender.com"
    
    web_app_info = telebot.types.WebAppInfo(web_app_url)
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = telebot.types.KeyboardButton(text="Открыть Web App 🚀", web_app=web_app_info)
    keyboard.add(button)
    
    bot.send_message(
        message.chat.id, 
        "Привет! Нажми на кнопку ниже, чтобы открыть мини-приложение и заполнить профиль:", 
        reply_markup=keyboard
    )

# Обработчик данных, которые приходят из формы авторизации Web App
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        # Получаем строку JSON от Web App и превращаем в словарь Python
        data = json.loads(message.web_app_data.data)
        
        name = data.get('name')
        height = data.get('height')
        weight = data.get('weight')
        goal = data.get('goal')
        
        # Формируем красивый структурированный ответ
        response_text = (
            f"🎉 **Профиль успешно заполнен!**\n\n"
            f"👤 **Имя:** {name}\n"
            f"📏 **Рост:** {height} см\n"
            f"⚖️ **Вес:** {weight} кг\n"
            f"🎯 **Цель:** {goal}\n\n"
            f"Отличный старт! Все данные сохранены, теперь мы можем приступать к работе. 💪"
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
