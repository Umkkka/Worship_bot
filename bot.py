import config
import telebot
import datetime
import pendulum
from telebot import types
from SQLighter import SQLighter
from config import database, token

bot = telebot.TeleBot(config.token)
db_worker = SQLighter(config.database)
today = datetime.date.today()
admin = {'Naum': 561832414, 'Jenya_Puk': 326063163}
users = {'Naum': 561832414, 'Jenya_Puk': 326063163, 'Vlad': 964274162, 'Igor': 338175053, 'Kirill': 678879328,
         'Marina': 356501970, 'Markops':422232272, 'Mark': 1138998802, 'Nadya': 570692271, 'Nastya': 388372626,
         'Sasha': 382993622, 'Pasha': 573323558, 'Julia': 778328958, 'Yura': 991849878, 'Jenya_Pan': 542399943,
         'Diana': 847182943}

@bot.message_handler(commands = ['start'])
def start(message):
    if message.chat.id in users.values():
        mes = 'Привет! Я Bot-помощник для группы прославления TheMosChurch.' + '\n' + 'На данный момент я могу присылать ' \
          'тебе список хвал на нынешнюю и следующую неделю с помощью определенного списка команд. В дальнейшем будут ' \
          'добавлены новые функции.' + '\n' + 'Любые идеи можешь писать моему создателю - @b_qwn' + '\n'
        bot.send_message(message.chat.id, mes)

        bot.send_message(message.chat.id, "Список моих команд: \n \n - Сегодня \n - Нынешняя пятница \n - Нынешняя суббота \n - Нынешнее воскресенье"
                                      "\n - Следующая пятница \n - Следующая суббота \n - Следующее вокресенье")

        markup = types.ReplyKeyboardMarkup()
        item0 = types.KeyboardButton('Сегодня')
        item1 = types.KeyboardButton('Нынешняя пятница')
        item2 = types.KeyboardButton('Следующая пятница')
        item3 = types.KeyboardButton('Нынешняя суббота')
        item4 = types.KeyboardButton('Следующая суббота')
        item5 = types.KeyboardButton('Нынешнее воскресенье')
        item6 = types.KeyboardButton('Следующее воскресенье')
        markup.row(item0)
        markup.row(item1, item3, item5)
        markup.row(item2, item4, item6)
        bot.send_message(message.chat.id, 'Выбери команду:', reply_markup=markup)
    else:
        mes = 'Привет! Я Bot-помощник для группы прославления TheMosChurch.' + '\n' + 'К сожалению, я не могу помочь тебе' \
            ' чем-либо, так как ты не являешься членом группы прославления.' \
             '\n' + 'Если ты хочешь вступить в группу, то пиши нашему лидеру - @eugen_park' + '\n'
        bot.send_message(message.chat.id, mes)

@bot.message_handler(commands = ['help'])
def helper(message):
    bot.send_message(message.chat.id, "Список общедоступных команд: \n\n -Сегодня \n - Нынешняя пятница \n - Нынешняя суббота \n - Нынешнее воскресенье"
                                      "\n - Следующая пятница \n - Следующая суббота \n - Следующее вокресенье")

@bot.message_handler(commands = ['add_program'])
def add_program(message):
    if message.chat.id in admin.values():
        mes = str(message.text)[12:] # Сообщение без /add_program
        date = mes[1:6] # Дата
        songs = mes[7:] # Список хвал
        bot.send_message(message.chat.id, db_worker.add_program(date, songs))
    else: bot.send_message(message.chat.id, 'Извини, команда добавления нового расписания не доступна тебе')

@bot.message_handler(commands = ['update_program'])
def update_program(message):
    if message.chat.id in admin.values():
        mes = str(message.text)[15:]  # Сообщение без /update_program
        date = mes[1:6]  # Дата
        songs = mes[7:]  # Список хвал
        bot.send_message(message.chat.id, db_worker.update_program(date, songs))
    else: bot.send_message(message.chat.id, 'Извини, команда обновления расписания не доступна тебе')

@bot.message_handler(commands = ['delete_program'])
def delete_program(message):
    if message.chat.id in admin.values():
        mes = str(message.text)[15:]  # Сообщение без /delete_program
        date = mes[1:]  # Дата
        bot.send_message(message.chat.id, db_worker.delete_program(date))
    else: bot.send_message(message.chat.id, 'Извини, команда удаления расписания не доступна тебе')

@bot.message_handler(content_types = ['text'])
def schedule(message):
    welcome = ['привет', 'хай', 'ку', 'здарова', 'здаров', 'даров', 'дороу', 'hi', 'приветики', 'здравствуй', 'прив',
               'хэй', 'хей', 'шалом']
    if message.chat.id in users.values():
        try:
            if message.text == 'Сегодня':
                date = pendulum.now().strftime('%d.%m')
                bot.send_message(message.chat.id, 'Список на сегодня:')
                bot.send_message(message.chat.id, db_worker.songs(date))
            elif message.text == 'Нынешняя пятница':
                date = pendulum.now().next(pendulum.FRIDAY).strftime('%d.%m')
                bot.send_message(message.chat.id, 'Список на пятницу {}:'.format(date))
                bot.send_message(message.chat.id, db_worker.songs(date))
            elif message.text == 'Следующая пятница':
                date = (pendulum.now().next(pendulum.FRIDAY) + datetime.timedelta(days = 7)).strftime('%d.%m')
                bot.send_message(message.chat.id, 'Список на пятницу {}:'.format(date))
                bot.send_message(message.chat.id, db_worker.songs(date))
            elif message.text == 'Нынешняя суббота':
                date = pendulum.now().next(pendulum.SATURDAY).strftime('%d.%m')
                bot.send_message(message.chat.id, 'Список на субботу {}:'.format(date))
                bot.send_message(message.chat.id, db_worker.songs(date))
            elif message.text == 'Следующая суббота':
                date = (pendulum.now().next(pendulum.SATURDAY) + datetime.timedelta(days = 7)).strftime('%d.%m')
                bot.send_message(message.chat.id, 'Список на субботу {}:'.format(date))
                bot.send_message(message.chat.id, db_worker.songs(date))
            elif message.text == 'Нынешнее воскресенье':
                date = pendulum.now().next(pendulum.SUNDAY).strftime('%d.%m')
                bot.send_message(message.chat.id, 'Список на воскресенье {}:'.format(date))
                bot.send_message(message.chat.id, db_worker.songs(date))
            elif message.text == 'Следующее воскресенье':
                date = (pendulum.now().next(pendulum.SUNDAY) + datetime.timedelta(days = 7)).strftime('%d.%m')
                bot.send_message(message.chat.id, 'Список на воскресенье {}:'.format(date))
                bot.send_message(message.chat.id, db_worker.songs(date))
            elif message.text in welcome:
                bot.send_message(message.chat.id, 'Привет от Артёма)))')
            else:
                bot.send_message(message.chat.id, 'Отправь мне команду')
        except:
            bot.send_message(message.chat.id, 'Ошибка. Возможно программа на этот день еще не составлена')
    else:
        bot.send_message(message.chat.id, 'К сожалению, я не могу помочь тебе чем-либо')

if __name__ == '__main__':
     bot.polling(timeout = 20)