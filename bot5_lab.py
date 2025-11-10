import telebot
from telebot import types
import pymysql
from random import randint

def connect_to_db():
    con = pymysql.connect(host="localhost",
                         user="root",
                         passwd="",
                         db="ЧатБот",
                        charset='utf8mb4')
    cur = con.cursor()
    return con, cur

def get_random_id(cur):
   cur.execute("SELECT MAX(id) FROM `Дост_Сам`")
   max_id = cur.fetchone()
   return randint(1, max_id[0])

def get_random_photo_text():
   con, cur = connect_to_db()
   rand_id = get_random_id(cur)
   cur.execute("SELECT photo, text FROM `Дост_Сам` WHERE id=" + str(rand_id))
   data = cur.fetchone()
   cur.close()
   con.close()
   return data[0], data[1]

def get_address_and_rating(attraction_id):
    con, cur = connect_to_db()
    cur.execute("SELECT Адрес, оценка FROM Адрес WHERE id = %s", (attraction_id,))
    data = cur.fetchone()
    cur.close()
    con.close()
    address, rating = data[0], data[1]
    return address, rating

def get_all_attractions():
    con, cur = connect_to_db()
    cur.execute("SELECT id, Достопримечательность FROM Адрес WHERE 1")
    data = cur.fetchall()
    cur.close()
    con.close()
    result_lines = [f"{row[0]} - {row[1]}" for row in data]
    return '\n'.join(result_lines)

def get_attraction_link(attraction_id):
    con, cur = connect_to_db()
    cur.execute("SELECT Сайт FROM Сайт WHERE id = %s", (attraction_id,))
    data = cur.fetchone()
    cur.close()
    con.close()
    return data[0]

bot = telebot.TeleBot('8221281978:AAGG4yKC0kUS5gzAtPT-TVcNGcItorHFhSs')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Покажи достопримечательность')
    btn2 = types.KeyboardButton('Адрес достопримечательности')
    btn3 = types.KeyboardButton('Все достопримечательности')
    btn_web_app = types.KeyboardButton('Ссылки', web_app=web_app)
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn_web_app)
    bot.send_message(message.chat.id, text="Привет! Я готов рассказать тебе немного о достопримечательностях Самары!", reply_markup=markup)

attraction_to_id = {
    'Самарский академический театр оперы и балета имени Шостаковича': 1,
    'Бункер Сталина': 2,
    'Жигулевский пивоваренный завод': 3,
    'Самарский академический театр драмы имени Горького': 4,
    'Храм Пресвятого Сердца Иисуса': 5,
    'Монумент Славы в честь работников авиапромышленности': 6,
    'Монумент ракета-носитель "Союз"': 7,
    'Софийская церковь': 8,
    'Памятник штурмовику Ил-2': 9,
    'Самарский областной историко-краеведческий музей': 10
}

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(web_app_message):
    attr_key = web_app_message.web_app_data.data
    print(f"Получены данные из интерфейса: {attr_key}")  # Для отладки

    attr_id = attraction_to_id.get(attr_key)

    if attr_id:
        link = get_attraction_link(attr_id)
        response = f"Ссылка на сайт \n {link}"
        bot.send_message(web_app_message.chat.id, response, parse_mode='HTML')
    else:
        bot.send_message(web_app_message.chat.id, "Достопримечательность не найдна")

@bot.message_handler(content_types=['text', 'photo'])
def get_text_messages(message):
    if message.text == "Покажи достопримечательность":
        photo, text = get_random_photo_text()
        bot.send_photo(message.from_user.id, photo, caption=text)
    elif message.text == "Адрес достопримечательности":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        for name in attraction_to_id.keys():
            markup.add(types.KeyboardButton(name))
        bot.send_message(message.chat.id, "Выбери интересующую достопримечательность", reply_markup=markup)
    elif message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Покажи достопримечательность')
        btn2 = types.KeyboardButton('Адрес достопримечательности')
        btn3 = types.KeyboardButton('Все достопримечательности')
        markup.add(btn1)
        markup.add(btn2)
        markup.add(btn3)
        bot.send_message(message.chat.id, "Возвращаемся к главному меню.", reply_markup=markup)
    elif message.text in attraction_to_id:
        attraction_id = attraction_to_id[message.text]
        address, rating = get_address_and_rating(attraction_id)
        response = f"Адрес: {address}\nОценка: {rating}"
        bot.send_message(message.chat.id, response)
    elif message.text == 'Все достопримечательности':
        text = get_all_attractions()
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю( Напиши /help.")

bot.polling(none_stop=True, interval=0)