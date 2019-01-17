import json
import requests
import telegram
from telegram.ext import Updater,CommandHandler, MessageHandler, Filters
import logging
from functools import wraps

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

botToken = '741258542:AAFy3s30tO-LDaG4SxpmAysFjY5EWFiRreg'
URL =  "https://api.telegram.org/bot{}/".format(botToken)
bot = telegram.Bot(token = botToken)
update = Updater(botToken)
dispatcher = update.dispatcher
typeQuery = 0
question = list(map(lambda x: str(x),list(range(1,6))))

'''Restricted List'''
LIST_OF_ADMINS = []

def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

''' Handler and Misc'''



'''DB Handler'''
query = {1:{'Hint':1,'Answer':2},2:{'Hint':3,'Answer':4},3:{'Hint':5,'Answer':6},4:{'Hint':7,'Answer':8},5:{'Hint':9,'Answer':10}}


''' UI '''
keyboard1 = [['Hint','Answer']]
reply1 = telegram.ReplyKeyboardMarkup(keyboard1)
keyboard2 = [['1','2','3','4','5']]
reply2 = telegram.ReplyKeyboardMarkup(keyboard2)
'''Functionality'''
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="I'm Mr Khoh's Proxy, which means throw all your Chemistry Questions my way and I will try to resolve them",
                     reply_markup = reply1)
def q1(bot,update):
    text = update.message.text
    global typeQuery
    if text == 'Hint':
        typeQuery = 'Hint'
        bot.send_message(chat_id=update.message.chat_id,
                     text="Looking for a hint? Which Question?",
                     reply_markup = reply2)
    elif text == 'Answer':
        typeQuery = 'Answer'
        bot.send_message(chat_id=update.message.chat_id,
                     text="Looking for an answer? It seems you have fallen to the dark side. Which Question?",
                     reply_markup = reply2)
    elif text in question and (typeQuery == 'Hint' or typeQuery == 'Answer'):
        question_num = int(text)
        answer = query[question_num][typeQuery]
        bot.send_message(chat_id=update.message.chat_id,text= answer)

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

def done(bot,update):
    bot.send_message(chat_id=update.message.chat_id, text="Alright, hope that helped you :)",reply_markup = telegram.ReplyKeyboardRemove())


@restricted
def setup(bot,update):
    question_string = list(map(lambda x: str(x),range(51)))
    global query
    setup_qns = 0
    bot.send_message(chat_id=update.message.chat_id,
                     text="Setting up for next Tutorial? How many question?")
    while update.message.text:
        if update.message.text in question_string:
            setup_qns = int(update.message.text)
            for i in range (setup_qns):
                num = i+1
                texty = "Please key in Hint for Question " + str(num)
                bot.send_message(chat_id=update.message.chat_id,
                        text= texty)
                hint = update.message.text
                query[i] = {'Hint':hint, 'Answer':0}
                texty = "Please key in Hint for Answer " + str(num)
                bot.send_message(chat_id=update.message.chat_id,
                        text= texty)
                answer = update.message.text
                query[i]['Answer'] = answer

start_handler = CommandHandler(command = "start",callback = start)
setup_handler = CommandHandler(command = "setup",callback = setup)
done_handler = CommandHandler(command = "done",callback = done)
q1_handler = MessageHandler(Filters.text, q1)
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(setup_handler)
dispatcher.add_handler(done_handler)
dispatcher.add_handler(q1_handler)
dispatcher.add_handler(unknown_handler)

update.start_polling()

