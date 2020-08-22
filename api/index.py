import logging
import requests
import random
import re
import os

from bs4 import BeautifulSoup

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Bot, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

Menu_keyboard = [['New Skills', 'Motivation'], ['Recent', 'Random'], ['Contact Us']]

def start(update, context):
    update.message.reply_text("Welcome to fitradio.in\nFor help use /help", 
                              reply_markup = ReplyKeyboardMarkup(Menu_keyboard, one_time_keyboard=False))
    
    file1 = open("myfile.txt","r+")
    users = []
    lines = file1.readlines()
    
    for line in lines:
        c = int(line)
        users.append(c)
    if update.message.chat.id not in users:    
        file1.write(str(update.message.chat.id)+"\n")
    file1.close()
 
def menu(update, context):
    update.message.reply_text("Welcome to fitradio.in\nFor help use /help", 
                              reply_markup = ReplyKeyboardMarkup(Menu_keyboard, one_time_keyboard=False))
        
def help_command(update, context):
    update.message.reply_text("Use /start to list menu\nChoose any category to get an article")
   
def get_Title(url):
    if "https://fitradio.in/wp/" in url:
        title = url[23:-1]
    elif "https://fitradio.in/" in url:
        title = url[20:-1]
    else:
        title = "Not Found"
    title = title.replace('-', ' ').capitalize()
    return title
             
def echo(update, url):
    source = requests.get(url)
    soup = BeautifulSoup(source.text, "lxml")
    links = soup.find_all('a', href=True, text=True)
    s = []
    sb = []
    
    for x in range(0, len(links)):
        if links[x]['href'].startswith("https://fitradio.in/"):
            if links[x]['href'] not in s:
                s.append(links[x]['href'])
                sb.append(links[x].text)
               
    return s, sb
        
def new_skills(update, context):
    update.message.reply_text("Here is an article to learn something new...")
    url = "https://fitradio.in/new-skills/"
    arr, arrb = echo(update, url)
    arr = arr[5 : len(arr)-2]
    arrb = arrb[5 : len(arrb)-2]
    x = random.randint(0, len(arr)-1)
    
    update.message.reply_text(arrb[x] + "\n" + arr[x])
    
def motivation(update, context):
    update.message.reply_text("Here you go motivated...")
    url = "https://fitradio.in/motivation/"
    arr, arrb = echo(update, url)
    arr = arr[5 : len(arr)-2]
    arrb = arrb[5 : len(arrb)-2]
    x = random.randint(0, len(arr)-1)
    
    update.message.reply_text(arrb[x] + "\n" + arr[x])
    
def randomm(update, context):
    update.message.reply_text("Hmm.. For your read.")
    url = "https://fitradio.in/blog/"
    arr, arrb = echo(update, url)
    arr = arr[5 : len(arr)-2]
    arrb = arrb[5 : len(arrb)-2]
    x = random.randint(0, len(arr)-1)
    
    update.message.reply_text(arrb[x] + "\n" + arr[x])

def recent(update, context):
    update.message.reply_text("Recent blog from fitradio.in")
    url = "https://fitradio.in/blog/"
    arr, arrb = echo(update, url)
    
    update.message.reply_text(arrb[5] + "\n" + arr[5])  
 
def contact(update, context): 
    dict = {"Instagram: @fitradio.in":"https://www.instagram.com/fitradio.in/",
            "Facebook: BasavRaj.Sonar.007":"https://www.facebook.com/BasavRaj.Sonar.007/"}
    buttons = []
    for key, value in dict.items():
        buttons.append([InlineKeyboardButton(text=key, url=value)])
        Keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text("Our Social Media Handles:",reply_markup = Keyboard)
    
def preview(update, context):
    update.message.reply_text('<a href="https://www.youtube.com/">Youtube</a>', parse_mode='html', disable_web_page_preview=True )
    
def send_link(update, context):
    print(update.message.chat.id)
    file1 = open("myfile.txt","r")
    users = []
    lines = file1.readlines()
    
    for line in lines:
        c = int(line)
        users.append(c)
    if (update.message.chat.id == 337365645) or (update.message.chat.id == 505078768):
        for user in users:
            context.bot.send_message(chat_id=user, text=update.message.text[13:])
    file1.close()



    
def main():
    token = "1384259183:AAHW7Ks093ACxTywO6yK58sGLFbW5iZP96U"
    updater = Updater(token, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("menu", menu))
    dp.add_handler(MessageHandler(Filters.regex('^(New Skills)$'), new_skills))
    dp.add_handler(MessageHandler(Filters.regex('^(Motivation)$'), motivation))
    dp.add_handler(MessageHandler(Filters.regex('^(Random)$'), randomm))
    dp.add_handler(MessageHandler(Filters.regex('^(Recent)$'), recent))
    dp.add_handler(MessageHandler(Filters.regex('^(Contact Us)$'), contact))
    dp.add_handler(CommandHandler("hellyoufuck", send_link))
    dp.add_handler(CommandHandler("preview", preview))
    
    #PORT = int(os.environ.get('PORT', '8443'))
    #print(PORT)
    #updater.start_webhook(listen="0.0.0.0",port=PORT, url_path = token)
    #updater.bot.set_webhook("https://3f4f0da6fba9.ngrok.io" + token)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()