import telebot
import config
import translator
import users
from telebot import types


bot = telebot.TeleBot(config.TOKEN)
users_dict = users.server_start(config.FILE_WITH_USERS, bot)


@bot.message_handler(commands=['start'])
def welcome(message):
    global users_dict

    users.serch_write(users_dict, message.chat.id)

    stik = open('sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, stik)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!"
                     "\n\nЯ - бот созданный переводить введеный тобой текст, на один из 16 доступный языков."
                     "\n\nВсё что от тебя нужно, выбрать язык, на который нужно перевести текст, а остальное я сделаю сам.\n"
                     "По умолчанию стоит английский язык."
                     "\n\n/lang - чтобы изменить языка".format(message.from_user, bot.get_me()),
                     parse_mode='html')


@bot.message_handler(commands=['lang'])
def сhange_language(message):
    bot.delete_message(message.chat.id, message.message_id)
    markup = types.InlineKeyboardMarkup(row_width=4)
    item1 = types.InlineKeyboardButton("English", callback_data='English en ')
    item2 = types.InlineKeyboardButton("Italian", callback_data='Italian it')
    item3 = types.InlineKeyboardButton("Spanish", callback_data='Spanish es')
    item4 = types.InlineKeyboardButton("Chinese", callback_data='Chinese zh')
    item5 = types.InlineKeyboardButton("German", callback_data='German de')
    item6 = types.InlineKeyboardButton("Norwegian", callback_data='Norwegian no')
    item7 = types.InlineKeyboardButton("Polish", callback_data='Polish pl')
    item8 = types.InlineKeyboardButton("Portuguese", callback_data='Portuguese pt')
    item9 = types.InlineKeyboardButton("Russian", callback_data='Russian ru')
    item10 = types.InlineKeyboardButton("Turkish", callback_data='Turkish tr')
    item11 = types.InlineKeyboardButton("Ukrainian", callback_data='Ukrainian uk')
    item12 = types.InlineKeyboardButton("French", callback_data='French fr')
    item13 = types.InlineKeyboardButton("Czech", callback_data='Czech cs')
    item14 = types.InlineKeyboardButton("Hindi", callback_data='Hindi hi')
    item15 = types.InlineKeyboardButton("Esperanto", callback_data='Esperanto eo')
    item16 = types.InlineKeyboardButton("Japanese", callback_data='Japanese ja')
    markup.add(item1, item2, item3, item4, item5, item6, item7, item8,
               item9, item10, item11, item12, item13, item14, item15, item16)
    bot.send_message(message.chat.id,
                     "Выбери язык, сейчас установлен " + users.serch_write(users_dict, message.chat.id)[0]
                     + ":".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def translat(message):
    bot.send_message(message.chat.id,
                     translator.trans(message.text,
                                      users_dict.get(str(message.chat.id))[1]))


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global users_dict

    users_dict.update({str(call.message.chat.id): call.data.split()})

    bot.delete_message(call.message.chat.id, call.message.message_id)

    bot.send_message(call.message.chat.id,
                     "Вы выбрали " + users_dict.get(str(call.message.chat.id))[0])


print("Чтобы коректно закончить работу сервера: CTRL+C и нажать ENTER")
bot.polling(none_stop=True)

users.servef_stop(users_dict)
