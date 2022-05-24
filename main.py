from bs4 import BeautifulSoup
import requests
import telebot
from telebot import types
from database import Database
import re

token='5310980548:AAF6FyBYVmE421Gacv--lvlq9WvBFaxK48o'
URL = 'https://habr.com/ru/news/top/daily/'
response = requests.get(URL)
with open('response.txt','w',encoding='utf-8') as f:
    f.write(response.text)
db=Database('database.db')

def telegram_bot():
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start (message):
        if(not db.user_exists(message.from_user.id)):

            db.add_user(message.from_user.id)
            bot.send_message(message.from_user.id,'Set an nickname:')

    @bot.message_handler(content_types=['text'])

    def bot_message (message):
        if message.text == 'news':

            try:
                with open('response.txt','r',encoding='utf-8') as f:
                    response = f.read()
                soup = BeautifulSoup(response,'lxml')
                post = soup.find('div', class_='tm-articles-list').find_next()
                title= post.find('a', class_='tm-article-snippet__title-link').text
                link = post.find('a', class_='tm-article-snippet__title-link')['href']
                link = f'https://habr.com{link}'
                bot.send_message(message.chat.id,f'{title}\n{link}')
            except Exception as e:
                print(e)
                bot.send_message(message.chat.id, 'Error.')

        else:
            if '@' in message.text or '/' in message.text:
                bot.send_message(message.from_user.id, 'Prohibited symbol')
            else:
                db.set_nickname(message.from_user.id,message.text)
                db.set_signup(message.from_user.id,'done')
                bot.send_message(message.from_user.id, 'Signed up!' )
                markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1=types.KeyboardButton("news")
                markup.add(item1)
                bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)



    bot.polling()
if __name__ == '__main__':
    telegram_bot()
