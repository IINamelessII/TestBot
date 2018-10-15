from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from tokens import DIALOGFLOW_TOKEN, TELEGRAM_TOKEN
import apiai
import json


# Обработка команд
def startCommand(bot, update):
    response = 'So, do you want to start speeking?'
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


updater = Updater(token=TELEGRAM_TOKEN)
dispatcher = updater.dispatcher
# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
