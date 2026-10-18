import telebot
from telebot import types
from flask import Flask
from threading import Thread

# Ваш токен от BotFather
TOKEN = '8979608664:AAGTTtJNxs5zfYWMHnI896kv8J9DhM_POl8'

# ⚠️ ВНИМАНИЕ: Замените на ваш числовой Telegram ID от @userinfobot
ADMIN_ID = 8979608664  

bot = telebot.TeleBot(TOKEN)

# Данные Kaspi
KASPI_PHONE = "+7 777 557 81 03"
KASPI_NAME = "Гаухар А."

# --- МИНИ-СЕРВЕР ДЛЯ БЕСПЛАТНОГО RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ------------------------------------------

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("✨ Всё включено — 15 000 ₸", callback_data="tariff_15000")
    btn2 = types.InlineKeyboardButton("📚 Только уроки — 10 000 ₸", callback_data="tariff_10000")
    btn3 = types.InlineKeyboardButton("📖 Журнал визажиста — 5 000 ₸", callback_data="tariff_5000")
    markup.add(btn1, btn2, btn3)
    
    text = (
        "Приветствую! 👋\n\n"
        "Вы попали в официальный бот записи на онлайн-курсы по макияжу «Сам себе визажист».\n"
        "Выберите интересующий вас тариф ниже:"
    )
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('tariff_'))
def callback_tariff(call):
    tariff_prices = {
        "tariff_15000": ("Всё включено", "15 000 ₸"),
        "tariff_10000": ("Только уроки", "10 000 ₸"),
        "tariff_5000": ("Журнал визажиста", "5 000 ₸")
    }
    
    name, price = tariff_prices.get(call.data, ("Тариф", ""))
    
    text = (
        f"💳 **Вы выбрали тариф: {name}**\n"
        f"Стоимость: **{price}**\n\n"
        f"**Шаг 1:** Сделайте перевод на карту Kaspi:\n"
        f"• Номер: `{KASPI_PHONE}`\n"
        f"• Получатель: {KASPI_NAME}\n\n"
        f"**Шаг 2:** После перевода **отправьте скриншот чека** прямо сюда, в этот чат в виде фотографии.\n\n"
        f"После проверки чека мы сразу вышлем вам ссылку на доступ!"
    )
    
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if ADMIN_ID == 123456789:
        bot.reply_to(message, "Ошибка: администратор не настроен в коде бота.")
        return
    
    user = message.from_user
    user_info = (
        f"📩 **Новый чек от ученицы!**\n"
        f"• Имя: {user.first_name}\n"
        f"• Username: @{user.username if user.username else 'нет'}\n"
        f"• ID: `{user.id}`"
    )
    
    bot.send_message(ADMIN_ID, user_info, parse_mode="Markdown")
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    
    bot.reply_to(message, "✅ Ваш чек успешно отправлен на проверку! Мы проверим оплату и свяжемся с вами.")

@bot.message_handler(func=lambda message: True)
def handle_all_text(message):
    bot.reply_to(message, "Пожалуйста, выберите тариф с помощью команды /start или отправьте скриншот чека в виде фото после оплаты.")

if __name__ == '__main__':
    keep_alive()  # Запускаем мини-сервер для удержания бота в сети
    print("Бот успешно запущен и ждет сообщения...")
    bot.infinity_polling()
