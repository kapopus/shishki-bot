import telebot
from telebot import types
import os

TOKEN = os.getenv("BOT_TOKEN")  # Render использует переменные окружения
bot = telebot.TeleBot(TOKEN)

# 💾 Список цен
PRICES = {
    "1": 15,
    "2": 30,
    "5": 75
}

# 👋 Приветствие
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛒 Купить", "👤 Профиль", "🌐 Язык", "📜 Правила")
    bot.send_message(message.chat.id, 
        "Привет! Добро пожаловать в магазин 'Шишки' 🌲\nВыбери действие ниже:",
        reply_markup=markup)

# 🔘 Обработка кнопок
@bot.message_handler(func=lambda msg: msg.text == "🛒 Купить")
def buy_product(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("1 шт – $15", callback_data="buy_1"),
        types.InlineKeyboardButton("2 шт – $30", callback_data="buy_2"),
        types.InlineKeyboardButton("5 шт – $75", callback_data="buy_5")
    )
    bot.send_message(message.chat.id, "Выбери количество шишек 🍀:", reply_markup=markup)

# ➡️ Обработка выбора количества
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def select_payment(call):
    qty = call.data.split("_")[1]
    price = PRICES[qty]
    
    # Сохраняем выбор пользователя (если нужно — в БД или файл)
    # Можно добавить user_state[call.from_user.id] = {"qty": qty, "price": price}

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("💳 Перевод на счёт", callback_data=f"pay_transfer_{qty}"),
        types.InlineKeyboardButton("₿ Крипта (в разработке)", callback_data="pay_crypto")
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"Вы выбрали {qty} шт за ${price}.\nВыберите способ оплаты:",
        reply_markup=markup
    )

# 💰 Перевод на счёт
@bot.callback_query_handler(func=lambda call: call.data.startswith("pay_transfer_"))
def handle_transfer(call):
    qty = call.data.split("_")[-1]
    price = PRICES[qty]

    # Инструкция по переводу
    bot.send_message(call.message.chat.id, 
        f"✅ Чтобы оплатить {qty} шт за ${price}, переведите деньги на номер счёта:\n\n"
        "💳 **1234 5678 9012 3456**\n"
        "👤 Имя получателя: Иван Иванов\n\n"
        "После перевода отправьте чек админу или напишите в поддержку для подтверждения.\n"
        "📦 После подтверждения вы получите фото и геолокацию."
    )

# 🔒 Заглушка под крипту
@bot.callback_query_handler(func=lambda call: call.data == "pay_crypto")
def handle_crypto(call):
    bot.answer_callback_query(call.id, "Крипта пока в разработке ⚠️", show_alert=True)

# Запуск
print("Бот запущен...")
bot.polling()
