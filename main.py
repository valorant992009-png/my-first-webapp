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

WEB_APP_URL = "https://my-first-webapp-dro4.onrender.com"

# Функция автоматической привязки веб-ссылки к синей кнопке «Анкета»
def setup_menu_button():
    try:
        bot.set_chat_menu_button(
            menu_button=telebot.types.MenuButtonWebApp(
                type="web_app", 
                text="Анкета 🚀", 
                web_app=telebot.types.WebAppInfo(WEB_APP_URL)
            )
        )
        print("Синяя кнопка меню успешно настроена!")
    except Exception as e:
        print(f"Ошибка настройки кнопки: {e}")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    # Полностью убираем нижнюю клавиатуру сообщений (ReplyKeyboardMarkup)
    remove_keyboard = telebot.types.ReplyKeyboardRemove(selective=False)
    
    bot.send_message(
        message.chat.id, 
        "Привет! Нажми на синюю кнопку **«Анкета 🚀»** слева от поля ввода текста.", 
        reply_markup=remove_keyboard,
        parse_mode='Markdown'
    )

# ЛОВИМ ДАННЫЕ ИЗ МИНИ-ПРИЛОЖЕНИЯ
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        # Десериализуем строку JSON, прилетевшую из tg.sendData
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
            f"Данные получены через tg.sendData() из синей кнопки! Экраны синхронизированы. 🚀"
        )
        
        bot.send_message(message.chat.id, response_text, parse_mode='Markdown')
        
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка обработки данных: {e}")


# ==========================================
# 3. Запуск всего приложения
# ==========================================
if __name__ == '__main__':
    setup_menu_button()
    
    server_thread = Thread(target=run_server)
    server_thread.start()
    
    print("Приложение успешно запущено...")
    bot.infinity_polling()
