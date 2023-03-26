import telebot
from telebot import types
from database import Database

bot = telebot.TeleBot('6123229478:AAFu7RcqAmeeZwa5RdNkZND33qLelBKVx_o')

db = Database('db.db')

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Looking partner')
    markup.add(item1)

    bot.send_message(message.chat.id, 'Hello', reply_markup=markup)

@bot.message_handler(commands=["menu"])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Looking partner')
    markup.add(item1)

    bot.send_message(message.chat.id, 'Menu', reply_markup=markup)

@bot.message_handler(commands=["stop"])
def stop(message):
    chat_info = db.get_active_chat(message.chat.id)
    if chat_info != False:
        db.delet_chat(chat_info[0])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Looking partner')
        markup.add(item1)

        bot.send_message(chat_info[1], 'Partner left chat', reply_markup=markup)
        bot.send_message(message.chat.id, 'You left chat', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "You didn't start chat", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == "private":
        if message.text == "Looking partner":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Stop looking')
            markup.add(item1)

            chat_two = db.get_chat()

            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id)
                bot.send_message(message.chat.id, 'prizrak Looking partner', reply_markup=markup)
            else:
                mess = "Partner found, stop diolog write /stop"
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("/stop")
                markup.add(item1)

                bot.send_message(message.chat.id, mess, reply_markup=markup)
                bot.send_message(chat_two, mess, reply_markup=markup)

        elif message.text == "Stop looking":
            db.delete_queue(message.chat.id)
            bot.send_message(message.chat.id, "Looking stoped, wirte /menu")
        
        else:
            chat_info = db.get_active_chat(message.chat.id)
            bot.send_message(chat_info[1], message.text)
            
bot.polling()