import os
import json
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import telebot
from threading import Thread

# ==========================================
# 1. Настройка веб-сервера (Flask)
# ==========================================
app = Flask(__name__, static_folder='public', static_url_path='')
CORS(app)  # Жестко разрешаем любые запросы, чтобы не было блокировок браузера

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Сюда веб-страница будет присылать POST-запрос с данными
@app.route('/submit-data', methods=['POST'])
def submit_data():
    try:
        data = request.json
        user_id = data.get('userId')
        name = data.get('name')
        height = data.get('height')
        weight = data.get('weight')
        goal = data.get('goal')

        if user_id:
            response_text = (
                f"🎉 **Профиль успешно заполнен!**\n\n"
                f"👤 **Имя:** {name}\n"
                f"📏 **Рост:** {height} см\n"
                f"⚖️ **Вес:** {weight} кг\n"
                f"🎯 **Цель:** {goal}\n\n"
                f"Данные получены напрямую сервером! Всё работает. 💪"
            )
            # Отправляем сообщение пользователю по его ID
            bot.send_message(user_id, response_text, parse_mode='Markdown')
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "User ID missing"}), 400
            
    except Exception as e:
        print(f"Ошибка на сервере Flask: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def run_server():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# ==========================================
# 2. Настройка Telegram-бота (telebot)
# ==========================================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    remove_keyboard = telebot.types.ReplyKeyboardRemove(selective=False)
    bot.send_message(
        message.chat.id, 
        "Привет! Нажми на синюю кнопку меню слева внизу, чтобы открыть анкету.", 
        reply_markup=remove_keyboard
    )

# ==========================================
# 3. Запуск всего приложения
# ==========================================
if __name__ == '__main__':
    server_thread = Thread(target=run_server)
    server_thread.start()
    
    print("Бот и Flask запущены...")
    bot.infinity_polling()
