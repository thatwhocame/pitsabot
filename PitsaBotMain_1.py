import telebot
import time
import logging
from io import StringIO
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
from random import randint, choice

Token      = '1469207995:AAFmAHVqs6yKQGdw7mpRh7MAflTmTH5s-1E'
Chat = '-1001480540421'
bot = telebot.TeleBot(Token)
start_mess = 'Pizza!\nWithout further interruption you can add me to your chat, let\'s celebrate and eat some pitsa!'
help_mess  = 'I can:\n//TODO: opportunites'
all_ping   = '@prostokvashka\nRazvodila\n@YegorSher\n@LizaZhdamirova\nBite Za Dusto\nSnezhanna\n@brutus1002\n@ktowh0\n@AcoDe113\nGrifn\n@Genabanila\n@AntiSep_tiK\nВладislove\nИсмаил\n@TimRudz\n@zizkooo\n@OIOIO101'

@bot.message_handler(commands=['pizza'])
def start_message(message):
    bot.send_message(Chat, start_mess)


def captcha_key():
    key = ''.join([choice('QWERTYUIOPLKJHGFDSAZXCVBNM1234567890') for i in range(5)])
    return key


Key = captcha_key()


def captcha_img(Key):
    img = Image.new('RGB', (100, 30), 0xffffff)
    draw = ImageDraw.Draw(img)

    for i in range(40):
        draw.line([(randint(0, 100), randint(0, 30)), (randint(0, 100), randint(0, 30))], randint(0, 0xffffff), 1)

    font = ImageFont.load_default()
    draw.text((0, 0), Key, 0, font)

    f = StringIO()
    img.save('kartinka', "JPEG")
    raw = f.getvalue()

    return img


Kartinka = captcha_img(Key)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(Chat, help_mess)

@bot.message_handler(commands=['all'])
def ping_all(message):
    bot.send_message(Chat, text=all_ping)


NameArr = ['Леонеля Меси', 'Леонардо Пепси', 'Жак Фреско', 'Жанна Фриске', 'Кристиан Бейл', 'Чайный Гриб',
           'Конфуций, 228г. до. н.э.', 'Стив Хуйс', 'Стив Джобс', 'Конфуций, 2012г', 'Альберт Эйнштейн',
           'Стивен Хоккинг', 'Вил Смит', 'Конфуций, вчера', 'Фирамир', 'Ала Пугачева', 'Мвемба А Нзига', 'Восточная мудрость', 'Владимир Владимирович Путин',
           'Гийяс-ад-Ди́н Абу-ль-Фатх Ома́р ибн-Эбрахи́м Хайя́м Нишапури́ (перс. غیاث الدین ابوالفتح عمر بن ابراهیم خیام نیشابورﻯ)']

@bot.message_handler(content_types=['voice'])
def Vois(message):
    bot.reply_to(message,
                 '\"' + ''.join([choice('абвг деёжзийклмно прстуфхцчш щъыьэ юя') for i in range(randint(5, 40))]) + '\" © ' + NameArr[randint(0, len(NameArr)-1)])


@bot.message_handler(commands=['captcha'])
def captcha_spam(message):
    bot.send_photo(Chat, Kartinka)
    bot.register_next_step_handler(message, check_captcha)


dict = {'ясно': 'хуясно', 'шо': 'каво', 'каво': 'шо', 'я хочу питси': 'а хуитси не хочешь дурак?',
        'я хочу пиццы': 'а хуиццы не хочешь дурак?',
        'я хочу питсы': 'а хуитсы не хочешь дурак?', 'я хочу пицци': 'а хуицци не хочешь дурак?',
        'я хочу пици': 'а хуици не хочешь дурак?', 'писрав': 'жидко',
        'я писрав': 'жидко?', 'ауе': 'лицо в говне', 'да': 'пизда', 'нет': 'пидора ответ', 'негры': 'пидорасы',
        'пидорасы': 'негры'}


@bot.message_handler(content_types=['text'])
def phrase_answer(message):
    if message.text.lower() in dict:
        bot.send_message(Chat, dict[message.text.lower()])


@bot.message_handler(content_types=['text'])
def check_captcha(message):
    # time.sleep(5)
    if message.text == Key:
        bot.reply_to(message, 'Верно!')
        # bot.send_message(Chat, 'Верно!')
        # time.sleep(5)
    if message.text != Key and message.text == "нет":
        # time.sleep(10)
        bot.reply_to(message, 'пидора ответ, неверно даун ебаный иди уроки учи')
        bot.register_next_step_handler(message, captcha_spam)
    else:
        bot.reply_to(message, 'Неверно!')
        # time.sleep(60)
        bot.register_next_step_handler(message, captcha_spam)


def main(use_logging, level_name):
    if use_logging:
        telebot.logger.setLevel(logging.getLevelName(level_name))
    bot.polling(none_stop=True, interval=.5)

bot.polling(none_stop=True)

if __name__ == '__main__':
    main(True, 'DEBUG')
