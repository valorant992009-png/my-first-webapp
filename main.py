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

def setup_menu_button():
    try:
        # Настраиваем ту самую профессиональную кнопку слева от поля ввода
        bot.set_chat_menu_button(
            menu_button=telebot.types.MenuButtonWebApp(
                type="web_app", 
                text="Анкета 🚀", 
                web_app=telebot.types.WebAppInfo(WEB_APP_URL)
            )
        )
        print("Красивая кнопка меню успешно настроена!")
    except Exception as e:
        print(f"Не удалось настроить кнопку меню: {e}")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    # При старте принудительно даем команду скрыть обычную клавиатуру
    remove_keyboard = telebot.types.ReplyKeyboardRemove()
    
    bot.send_message(
        message.chat.id, 
        "Привет! Для открытия приложения используй кнопку **«Анкета 🚀»** в левом нижнем углу экрана (рядом с полем ввода).", 
        reply_markup=remove_keyboard,
        parse_mode='Markdown'
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
            f"Отличный старт! Все данные сохранены, теперь мы можем приступать к работе. 💪"
        )
        
        # Важнейший момент: отправляем ответ и ЖЕСТКО удаляем обычную клавиатуру из кэша
        remove_keyboard = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, response_text, reply_markup=remove_keyboard, parse_mode='Markdown')
        
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при обработке анкеты: {e}")


# ==========================================
# 3. Запуск всего приложения
# ==========================================
if __name__ == '__main__':
    setup_menu_button()
    
    server_thread = Thread(target=run_server)
    server_thread.start()
    
    print("Бот запущен и готов к работе...")
    bot.infinity_polling()
