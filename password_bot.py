import random
import telebot
from telebot import types
import config
bot = telebot.TeleBot(config.Token)

gen = 'Сгенерировать'
but = 'Изменить длину'
markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
markup.add(types.KeyboardButton(gen))
markup.add(types.KeyboardButton(but))
length = 12

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, f"<b>Привет {message.from_user.first_name} {message.from_user.last_name}!</b>\nДобро пожаловать!\n\nПо умолчанию длина пароля 12 символов. Если вы хотите изменить длину, нажмите на соответствующую кнопку", parse_mode='html',reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == but)
def ask_symbol(message):
    msg = bot.send_message(message.chat.id, "Укажите количество символов", parse_mode='html')
    bot.register_next_step_handler(msg, get_length)

@bot.message_handler(func=lambda message: message.text == gen)
def generate(message):
    symbols = (
        '0123456789'
        'abcdefghijklmnopqrstuvwxyz'
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        '!@#$%^&*()_+'
    )
    result = ''
    for i in range(length):
        result += random.choice(symbols)
    bot.send_message(message.chat.id, '<code>'+result+'</code>', parse_mode='html')

def get_length(message):
    global length
    get_length = message.text
    print(get_length)
    length = int(get_length)
    msg = bot.send_message(message.chat.id, "Установлена длина пароля: "+get_length)
    bot.register_next_step_handler(msg, generate)

bot.polling(none_stop=True)