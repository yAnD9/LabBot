import telebot
from telebot import types
import pymysql
from random import randint
import urllib.parse


def connect_to_db():
    try:
        con = pymysql.connect(host="localhost",
                              user="root",
                              passwd="",
                              db="ЧатБот",
                              charset='utf8mb4')
        cur = con.cursor()
        return con, cur
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        return None, None


def get_random_id(cur):
    try:
        cur.execute("SELECT MAX(id) FROM `Дост_Сам`")
        max_id = cur.fetchone()
        return randint(1, max_id[0]) if max_id and max_id[0] else 1
    except Exception as e:
        print(f"Ошибка получения случайного ID: {e}")
        return 1


def get_random_photo_text():
    con, cur = connect_to_db()
    if not con or not cur:
        return None, "Ошибка подключения к базе данных"

    try:
        rand_id = get_random_id(cur)
        cur.execute("SELECT photo, text FROM `Дост_Сам` WHERE id=%s", (rand_id,))
        data = cur.fetchone()
        if data:
            return data[0], data[1]
        else:
            return None, "Данные не найдены"
    except Exception as e:
        print(f"Ошибка получения данных: {e}")
        return None, "Ошибка получения данных"
    finally:
        if cur:
            cur.close()
        if con:
            con.close()


def get_address_and_rating(attraction_id):
    con, cur = connect_to_db()
    if not con or not cur:
        return "Ошибка подключения к БД", "N/A", None, None

    try:
        # Получаем адрес, рейтинг и координаты из базы
        cur.execute("SELECT Адрес, Оценка, Широта, Долгота FROM Адрес WHERE id = %s", (attraction_id,))
        data = cur.fetchone()
        if data:
            address = data[0] if data[0] else "Адрес не указан"
            rating = data[1] if data[1] else "N/A"
            latitude = float(data[2]) if data[2] else None
            longitude = float(data[3]) if data[3] else None
            return address, rating, latitude, longitude
        else:
            return "Адрес не найден", "N/A", None, None
    except Exception as e:
        print(f"Ошибка получения данных: {e}")
        return "Ошибка получения данных", "N/A", None, None
    finally:
        if cur:
            cur.close()
        if con:
            con.close()

def get_all_attractions():
    con, cur = connect_to_db()
    if not con or not cur:
        return "Ошибка подключения к базе данных"

    try:
        cur.execute("SELECT id, Достопримечательность FROM Адрес WHERE 1")
        data = cur.fetchall()
        result_lines = [f"{row[0]} - {row[1]}" for row in data]
        return '\n'.join(result_lines) if result_lines else "Достопримечательности не найдены"
    except Exception as e:
        print(f"Ошибка получения списка достопримечательностей: {e}")
        return "Ошибка получения списка"
    finally:
        if cur:
            cur.close()
        if con:
            con.close()


def get_attraction_link(attraction_id):
    con, cur = connect_to_db()
    if not con or not cur:
        return "Ошибка подключения к БД"

    try:
        cur.execute("SELECT Сайт FROM Сайт WHERE id = %s", (attraction_id,))
        data = cur.fetchone()
        return data[0] if data else "Ссылка не найдена"
    except Exception as e:
        print(f"Ошибка получения ссылки: {e}")
        return "Ошибка получения ссылки"
    finally:
        if cur:
            cur.close()
        if con:
            con.close()


bot = telebot.TeleBot('8221281978:AAGG4yKC0kUS5gzAtPT-TVcNGcItorHFhSs')

attraction_to_id = {
    'Самарский театр оперы и балета': 1,
    'Бункер Сталина': 2,
    'Жигулевский пивоваренный завод': 3,
    'Самарский драм. театр': 4,
    'Храм Пресвятого Сердца Иисуса': 5,
    'Монумент Славы "Человек с крыльями"': 6,
    'Монумент ракета-носитель "Союз"': 7,
    'Софийская церковь': 8,
    'Памятник штурмовику Ил-2': 9,
    'Музей им. Алабина': 10
}


@bot.message_handler(commands=['start'])
def start(message):
    web_app = types.WebAppInfo(url="https://yand9.github.io/LabBot/")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Покажи достопримечательность')
    btn2 = types.KeyboardButton('Адрес достопримечательности')
    btn3 = types.KeyboardButton('Все достопримечательности')
    btn_web_app = types.KeyboardButton('Открыть веб-приложение', web_app=web_app)
    markup.add(btn1, btn2)
    markup.add(btn3, btn_web_app)
    bot.send_message(message.chat.id,
                     text="Привет! Я готов рассказать тебе немного о достопримечательностях Самары!\n\n"
                          "Выбери одну из опций ниже или открой веб-приложение для просмотра достопримечательностей.",
                     reply_markup=markup)


@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(web_app_message):
    try:
        attr_key = web_app_message.web_app_data.data
        print(f"Получены данные из веб-приложения: {attr_key}")

        attr_id = attraction_to_id.get(attr_key)

        if attr_id:
            link = get_attraction_link(attr_id)
            response = f"🌐 Ссылка на сайт достопримечательности:\n{link}"
            bot.send_message(web_app_message.chat.id, response)
        else:
            bot.send_message(web_app_message.chat.id, "❌ Достопримечательность не найдена в базе данных")
    except Exception as e:
        print(f"Ошибка обработки web_app_data: {e}")
        bot.send_message(web_app_message.chat.id, "❌ Произошла ошибка при обработке запроса")


@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    try:
        if message.text == "Покажи достопримечательность":
            photo, text = get_random_photo_text()
            if photo:
                bot.send_photo(message.chat.id, photo, caption=text)
            else:
                bot.send_message(message.chat.id, text)

        elif message.text == "Адрес достопримечательности":
            # Создаем inline-клавиатуру с достопримечательностями
            keyboard = types.InlineKeyboardMarkup()

            # Создаем кнопки для каждой достопримечательности
            key_opera = types.InlineKeyboardButton(
                text='Самарский театр оперы и балета',
                callback_data='attraction_1'
            )
            keyboard.add(key_opera)

            key_bunker = types.InlineKeyboardButton(
                text='Бункер Сталина',
                callback_data='attraction_2'
            )
            keyboard.add(key_bunker)

            key_brewery = types.InlineKeyboardButton(
                text='Жигулевский пивоваренный завод',
                callback_data='attraction_3'
            )
            keyboard.add(key_brewery)

            key_drama = types.InlineKeyboardButton(
                text='Самарский драм. театр',
                callback_data='attraction_4'
            )
            keyboard.add(key_drama)

            key_temple = types.InlineKeyboardButton(
                text='Храм Пресвятого Сердца Иисуса',
                callback_data='attraction_5'
            )
            keyboard.add(key_temple)

            key_monument = types.InlineKeyboardButton(
                text='Монумент Славы "Человек с крыльями"',
                callback_data='attraction_6'
            )
            keyboard.add(key_monument)

            key_rocket = types.InlineKeyboardButton(
                text='Монумент ракета-носитель "Союз"',
                callback_data='attraction_7'
            )
            keyboard.add(key_rocket)

            key_sofia = types.InlineKeyboardButton(
                text='Софийская церковь',
                callback_data='attraction_8'
            )
            keyboard.add(key_sofia)

            key_airplane = types.InlineKeyboardButton(
                text='Памятник штурмовику Ил-2',
                callback_data='attraction_9'
            )
            keyboard.add(key_airplane)

            key_museum = types.InlineKeyboardButton(
                text='Музей им. Алабина',
                callback_data='attraction_10'
            )
            keyboard.add(key_museum)

            # Показываем все кнопки сразу
            bot.send_message(
                message.chat.id,
                text='🏛 **Выбери достопримечательность для получения адреса:**',
                reply_markup=keyboard,
                parse_mode="Markdown"
            )

        elif message.text == 'Все достопримечательности':
            text = get_all_attractions()
            bot.send_message(message.chat.id, f"📋 **Список всех достопримечательностей:**\n\n{text}",
                             parse_mode="Markdown")

        else:
            bot.send_message(message.chat.id, "❌ Я тебя не понимаю. Используй кнопки меню или напиши /start")

    except Exception as e:
        print(f"Ошибка обработки сообщения: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка при обработке запроса")


@bot.callback_query_handler(func=lambda call: call.data.startswith('attraction_'))
def handle_attraction_selection(call):
    try:
        # Извлекаем ID достопримечательности из callback_data
        attraction_id = int(call.data.split('_')[1])

        # Получаем название достопримечательности по ID
        attraction_name = None
        for name, id_num in attraction_to_id.items():
            if id_num == attraction_id:
                attraction_name = name
                break

        if attraction_name:
            # Получаем адрес, рейтинг и координаты
            address, rating, latitude, longitude = get_address_and_rating(attraction_id)
            response = f"📍 **{attraction_name}**\n\n🏠 **Адрес:** {address}\n⭐ **Оценка:** {rating}"

            if latitude and longitude:
                response += f"\n\n📍 **Координаты:** {latitude:.6f}, {longitude:.6f}"

            # Создаем inline-кнопку для Яндекс.Карт
            keyboard = types.InlineKeyboardMarkup()

            # Формируем ссылку на Яндекс.Карты с координатами
            yandex_maps_url = f"https://yandex.ru/maps/?ll={longitude},{latitude}&pt={longitude},{latitude}&z=17&l=map"
            button_text = "🗺️ Показать на картах"

            # Создаем кнопку с прямой URL ссылкой на Яндекс.Карты
            yandex_maps_button = types.InlineKeyboardButton(
                text=button_text,
                url=yandex_maps_url
            )
            keyboard.add(yandex_maps_button)

            # Отправляем информацию о достопримечательности
            bot.send_message(call.message.chat.id, response, parse_mode="Markdown", reply_markup=keyboard)

        else:
            bot.send_message(call.message.chat.id, "❌ Достопримечательность не найдена")

        # Подтверждаем получение callback
        bot.answer_callback_query(call.id)

    except Exception as e:
        print(f"Ошибка обработки выбора достопримечательности: {e}")
        bot.send_message(call.message.chat.id, "❌ Произошла ошибка при обработке запроса")
        bot.answer_callback_query(call.id)

if __name__ == '__main__':
    print("Бот запущен...")
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(f"Ошибка запуска бота: {e}")