from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from random import shuffle
from req import get_memes
from tokens import DIALOGFLOW_TOKEN, TELEGRAM_TOKEN
import apiai
import json


# Обработка команд
def startCommand(bot, update):
    response = 'So, do you want to start speeking?'
    bot.send_message(chat_id=update.message.chat_id, text=response)


def memeCommand(bot, update):
    try:
        src = memes.pop() # TODO: make list for every char, not 1 for all
        bot.send_photo(chat_id=update.message.chat_id, photo=src)
    except IndexError:
        response = "No more memes :("
        bot.send_message(chat_id=update.message.chat_id, text=response)


def textMessage(bot, update):
    request = apiai.ApiAI(DIALOGFLOW_TOKEN).text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'TestNamelessBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='What did you say?')


if __name__ == "__main__":

    memes = get_memes()
    shuffle(memes)

    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    start_command_handler = CommandHandler('start', startCommand)
    meme_command_handler = CommandHandler('meme', memeCommand)
    text_message_handler = MessageHandler(Filters.text, textMessage)

    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(meme_command_handler)
    dispatcher.add_handler(text_message_handler)

    updater.start_polling(clean=True)

    updater.idle()
