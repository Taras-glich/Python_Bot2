import requests
import telebot
from telebot import types

TOKEN = '6731771522:AAHNE6M9I00jN0ApmJUPd4yoiMfM_8mtUPY'
api_key = '64170c1550caf397df817b448156bf04'

bot = telebot.TeleBot(TOKEN)
movie_name = None


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Введіть назву фільма')


@bot.message_handler(content_types=['text'])
def s_movie(message):
    global movie_name
    movie_name = message.text.lower()
    url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}'
    response = requests.get(url)

    if response.status_code == 200:
        search_results = response.json()['results']
        for result in search_results[:4]:
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton('Переглянути сайт', url=f'https://www.themoviedb.org/movie/{result["id"]}')
            markup.row(btn1)

            poster_path = result.get('poster_path')
            if poster_path:
                poster_url = f'https://image.tmdb.org/t/p/w500{poster_path}'
                res = f"Назва фільму: {result['title']}\nРік випуску: {result['release_date']}"
                bot.send_photo(message.chat.id, photo=poster_url, caption=res, reply_markup=markup)

    else:
        print(f"Помилка: {response.status_code}")

bot.polling()
