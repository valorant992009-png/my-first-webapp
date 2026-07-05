import os
from flask import Flask, send_from_directory
import telebot
from threading import Thread

# 1. Настройка веб-сервера (Flask)
import os

# Указываем Flask явный путь к папке public
app = Flask(__name__, static_folder='public', static_url_path='')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

def run_server():
    # Render автоматически передает порт в переменную окружения PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# 2. Настройка Telegram-бота
# Сюда Render сам подставит токен твоего бота, который мы настроим позже
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    # Создаем кнопку, которая откроет наше Web App
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    # ВАЖНО: ссылку на Web App мы заменим после деплоя на Render!
    web_app_info = telebot.types.WebAppInfo("https://my-first-webapp-dro4.onrender.com")
    web_app_button = telebot.types.KeyboardButton(text="Открыть Web App 🚀", web_app=web_app_info)
    markup.add(web_app_button)
    
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку ниже, чтобы открыть мини-приложение:", reply_markup=markup)

def run_bot():
    bot.infinity_polling()

# 3. Запуск всего вместе
if __name__ == '__main__':
    # Запускаем сервер Flask в отдельном потоке, чтобы он не мешал боту
    server_thread = Thread(target=run_server)
    server_thread.start()
    
    # Запускаем бота
    run_bot()
