import telebot
from telebot import types
from vkwave.bots import SimpleLongPollBot, SimpleBotEvent
from datetime import datetime
from pprint import pprint
import requests
import json
import re
import multiprocessing
import schedule
import time
import random
import os
import psutil
import platform

TG_TOKEN = os.getenv('TG_TOKEN')
VK_TOKEN = os.getenv('VK_TOKEN')
VK_GROUP = os.getenv('VK_GROUP')

tb = telebot.TeleBot(TG_TOKEN)
print(f"The Bot is online (id: {tb.get_me().id})...")
vb = SimpleLongPollBot(tokens=VK_TOKEN, group_id=VK_GROUP)

smile = [
    "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇", "🙂", "🙃", "😉", "😌", "😍", "😘", "😗", "😙",
    "😚", "😋", "😜", "😝", "😛", "🤑", "🤗", "🤓", "😎", "🤡", "🤠", "😏", "😒", "😞", "😔", "😟", "😕", "🙁",
    "😣", "😖", "😫", "😩", "😤", "😠", "😡", "😶", "😐", "😑", "😯", "😦", "😧", "😮", "😲", "😵", "😳", "😱",
    "😨", "😰", "😢", "😥", "🤤", "😭", "😓", "😪", "😴", "🙄", "🤔", "🤥", "😬", "🤐", "🤢", "🤧", "😷", "🤒",
    "🤕", "😈", "👿", "👹", "👺", "💩", "👻", "💀", "👽", "👾", "🤖", "🎃", "😺", "😸", "😹", "😻", "😼", "😽",
    "🙀", "😿", "😾", "👐", "🙌", "👏", "🙏", "🤝", "👍", "👎", "👊", "✊", "🤛", "🤜", "🤞", "🤘", "👌", "👈",
    "👉", "👆", "👇", "✋", "🤚", "🖐", "🖖", "👋", "🤙", "💪", "🖕", "🤳", "💅", "💍", "💄", "💋", "👄", "👅",
    "👂", "👃", "👁", "👀", "🗣", "👤", "👥", "👶", "👦", "👧", "👨", "👩", "👱", "👴", "👵", "👲", "👳", "👳",
    "👮", "👷", "💂", "🕵", "🤶", "🎅", "👸", "🤴", "👰", "🤵", "👼", "🤰", "🙇", "💁", "🙅", "🙆", "🙋", "🤦",
    "🤷", "🙎", "💇", "💆", "🕴", "💃", "🕺", "👯", "👯", "🚶", "🏃", "👭", "👬", "💑", "💏", "👪", "👚", "👕",
    "👖", "👔", "👗", "👙", "👘", "👠", "👡", "👢", "👞", "👟", "👒", "🎩", "🎓", "👑", "⛑", "🎒", "👝", "👛",
    "👜", "💼", "👓", "🕶", "🌂"
]

chats = [
    '2501359',
    '6267957',
    '-1001348677218',
]
stickers = [
    'CAACAgIAAxkBAAIYzWh0EYE619Vrw4dwBNk8hTXaaDuBAAK6DwACAsSYSq3W9HdybYh3NgQ',  # start
    'CAACAgIAAxkBAAIYdGh0EDnwYybZuj2qc2qamxRKQExDAAJOAAMiTA8MNM5spwKVQf42BA',
    'CAACAgIAAxkBAAIS1mJEyRXuHigJTbrBMNuof5BQdMMKAAKEAQACy4gZETK1KP8R8jW1IwQ',
    'CAACAgIAAxkBAAIS1WJEx-fd_sZy3C36hTqNE_NeVr3XAAJIHgAC6VUFGJDLIuAKbjsWIwQ',
    'CAACAgQAAxkBAAEEStdiQL17uUKsMMmyghM9jQdj9LGjmAACAwIAAvAeaiEgvmSCXjXaWSME',
    'CAACAgIAAxkBAAIS12JEyzl6mRRJCtRo_1FS-OaKmgHlAAL_DgACB_GBScLPRvI6stG4IwQ',  # неа
    'CAACAgIAAxkBAAIS2GJEy3FKEn2sF9ei9PWay-x6-wPWAAIbCQACGELuCNy5pdXzSq7IIwQ',
    'CAACAgIAAxkBAAIS2WJEy9RFZaz3_yIEZFx7C3CU4GCZAAKZAAPLiBkRnMRwPqB1w3AjBA',
    'CAACAgEAAxkBAAIS2mJEzFzIvAKfPfFZ5KxvAnhuC-dOAAI6AAOhBQwN3srafQKK11kjBA',
    'CAACAgIAAxkBAAITwmhgFZYervsBDFWiAAGcrkOx_nUwVQACbwEAAj0N6AQ5fyi7eC6__zYE',
    'CAACAgIAAxkBAAITumhgD2JJml586mfwZYH4oNZmaNriAAKrAQACEBptIni-vpHMVGzHNgQ',
    'CAACAgIAAxkBAAIT7GhgHy3YeyiN2WSIR5vh6paBJ32RAAImAAN7wH0TtNsrvlEETkI2BA',
]
i = {
    'А': '丹', 'Б': '石', 'В': '乃', 'Г': '厂', 'Д': '亼', 'Е': '仨', 'Ё': '仨', 'Ж': '水', 'З': '弓', 'И': '仈', 'Й': '订',
    'К': '长', 'Л': '人', 'М': '从', 'Н': '卄', 'О': '口', 'П': '刀', 'Р': '尸', 'С': '匚', 'Т': '丅', 'У': '丫', 'Ф': '中',
    'Х': '乂', 'Ц': '凵', 'Ч': '丩', 'Ш': '山', 'Щ': '山', 'Ъ': '乙', 'Ы': '辷', 'Ь': '乙', 'Э': '彐', 'Ю': '扣', 'Я': '牙'
}


# @bot.message_handler(bot.regex_filter(r'(?i)спасибо(.*?)'))
# async def my_pleasure(event: SimpleBotEvent):
#     await event.answer(message='Всегда рад помочь &#128521;')


# @bot.message_handler(bot.text_filter(["привет", "здарова", "хай"]))
# async def greet(event: SimpleBotEvent):
#     await event.answer('Привет!')


@vb.message_handler(vb.regex_filter(r'.*'))
async def greet(event: SimpleBotEvent):
    print(event.text.lower())
    if 'ты где' in event.text.lower():
        await event.answer(im_here())
    if 'переведи' in event.text.lower():
        await event.answer(replace(event.text.lower()))


def lucky():
    # Генерируем рандомный смаил
    return f"{random.choice(smile)}{random.choice(smile)}{random.choice(smile)}"


def replace(string) -> str:
    string = string.replace('переведи ', '')
    arr = []
    for name in string:
        if i.get(name.upper()):
            arr.append(i.get(name.upper()))
        else:
            arr.append(name)
    return ''.join(arr)


def get_custom_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('стикер'), types.KeyboardButton('где'))
    keyboard.row(types.KeyboardButton('мне повезёт'))
    keyboard.row(types.KeyboardButton('статистика'))
    return keyboard


@tb.message_handler(commands=['start'])
def handle_qwe(message):
    chatid = message.chat.id
    # tb.send_message(
    #     chatid,
    #     "Выберите действие:",
    #     reply_markup=get_custom_keyboard()
    # )
    tb.send_sticker(
        chatid,
        stickers[0],
        reply_markup=get_custom_keyboard()
    )


@tb.message_handler(func=lambda m: m.text == 'стикер')
def handle_sticker(message):
    chatid = message.chat.id
    tb.send_sticker(chatid, random.choice(stickers))


@tb.message_handler(func=lambda m: m.text == 'где')
def handle_gde(message):
    chatid = message.chat.id
    tb.send_message(chatid, im_here())


@tb.message_handler(func=lambda m: m.text == 'мне повезёт')
def handle_gde(message):
    chatid = message.chat.id
    tb.send_message(chatid, lucky())


@tb.message_handler(func=lambda m: True)
def answer(message):
    # pprint(dir(message.from_user))
    # print(message.from_user.full_name)
    chatid = message.chat.id
    print(chatid)
    print(message)
    if message.content_type == 'text' and str(chatid) in chats:
        if 'привет бот' in message.text:
            tb.send_message(chatid, 'привет')
        if 'переведи' in message.text.lower():
            tb.send_message(chatid, replace(message.text.lower()))
        if 'статистика' in message.text.lower():
            tb.send_message(chatid, get_server_stats(), parse_mode='Markdown')
        if 'федя' in message.text.lower():
            if 'ты как' in message.text.lower():
                tb.send_sticker(chatid, random.choice(stickers))
            if 'ты где' in message.text.lower():
                tb.send_message(chatid, im_here())


@tb.message_handler(content_types=['sticker'])
def handle_sticker(message):
    chatid = message.chat.id
    sticker = message.sticker
    stickerid1 = sticker.file_id
    # json_ = message.json
    # stickerid2 = json_.get('sticker').get('file_id')
    print(f"Sticker from {chatid}")
    print(stickerid1)
    if stickerid1 not in stickers:
        stickers.append(stickerid1)
    # print(stickerid2)
    # Здесь можешь отвечать на стикер, если хочешь
    tb.send_message(chatid, lucky())


def im_here():
    res = requests.request('get', 'https://vk.com/upload.php?act=myip')
    ros = res.text
    pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
    ip_address = pattern.findall(ros)
    return f'я тут {ip_address[0]}'


def send_weekends():
    day = datetime.isoweekday(datetime.today())
    hour = datetime.now().hour
    if int(day) not in [6, 7]:
        return
    if 9 < int(hour) < 20:
        tb.send_sticker(chats[0], random.choice(stickers))


def send_workdays():
    if datetime.isoweekday(datetime.today()) <= 5:
        tb.send_message(chats[0], text=replace('звери умрут'))
        # tb.send_message(chats[2], text='11:11')


def tb_listener():
    try:
        tb.infinity_polling(
            skip_pending=True,
            none_stop=True,
        )
    except:
        print("Lost connection!")


def vb_listener():
    try:
        vb.run_forever()
    except:
        print("Lost connection!")


def sayer():
    # schedule.every(1).to(60).minutes.do(send_weekends)  # хз как это работает
    # schedule.every().day.at("11:11:11").do(send_workdays)
    schedule.every().day.at("11:11:11").do(send_daily_stats)
    while True:
        schedule.run_pending()
        time.sleep(1)


def get_server_stats():
    """Возвращает статистику сервера в виде строки"""
    try:
        # CPU
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()

        # Память
        memory = psutil.virtual_memory()
        memory_total = round(memory.total / (1024 ** 3), 2)
        memory_used = round(memory.used / (1024 ** 3), 2)
        memory_percent = memory.percent

        # Диск
        disk = psutil.disk_usage('/')
        disk_total = round(disk.total / (1024 ** 3), 2)
        disk_used = round(disk.used / (1024 ** 3), 2)
        disk_percent = disk.percent

        # Загрузка системы
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time

        # Формируем сообщение
        message = f"📊 *Статистика сервера*\n\n"
        message += f"🖥️ *CPU*: {cpu_usage}% ({cpu_count} ядер)\n"
        message += f"💾 *Память*: {memory_used}GB / {memory_total}GB ({memory_percent}%)\n"
        message += f"💿 *Диск*: {disk_used}GB / {disk_total}GB ({disk_percent}%)\n"
        message += f"⏰ *Аптайм*: {str(uptime).split('.')[0]}\n"
        message += f"🖥️ *ОС*: {platform.system()} {platform.release()}\n"
        message += f"⏱️ *Время*: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        print(f"отправка в чат\n {message}")

        return message

    except Exception as e:
        return f"❌ Ошибка получения статистики: {e}"


# ДОБАВЛЯЕМ ОБРАБОТЧИК КОМАНДЫ /stats
@tb.message_handler(commands=['stats'])
def handle_stats(message):
    """Обработчик команды /stats"""
    chatid = message.chat.id
    stats_message = get_server_stats()
    print(f"отправка в чат {chatid}")
    tb.send_message(chatid, stats_message, parse_mode='Markdown')


# ДОБАВЛЯЕМ ОБРАБОТЧИК ДЛЯ КНОПКИ 'статистика'
@tb.message_handler(func=lambda m: m.text == 'статистика')
def handle_stats_button(message):
    """Обработчик кнопки статистики"""
    chatid = message.chat.id
    stats_message = get_server_stats()
    tb.send_message(chatid, stats_message, parse_mode='Markdown')


# ДОБАВЛЯЕМ РАСПИСАНИЕ ДЛЯ ОТПРАВКИ СТАТИСТИКИ
def send_daily_stats():
    """Отправка ежедневной статистики"""
    try:
        stats_message = get_server_stats()
        try:
            print(f"отправка в чат {chats[0]}")
            tb.send_message(chats[0], stats_message, parse_mode='Markdown')
        except Exception as e:
            print(f"Ошибка отправки в чат {chats[0]}: {e}")
    except Exception as e:
        print(f"Ошибка формирования статистики: {e}")


if __name__ == '__main__':
    # tb_listener()
    # vb_listener()
        # search_path = input(
        #             "\nпиши, ёптель: "
        #         ).strip()
        # print(replace(search_path))

    processes = {
        # 'p1': multiprocessing.Process(target=tb_listener, name='listener1'),
        'p2': multiprocessing.Process(target=vb_listener, name='listener2'),
        'p3': multiprocessing.Process(target=sayer, name='sayer'),
    }
    for process in processes.values():
        process.start()
    time.sleep(1)
    tb_listener()
    # answer = ''
    # while answer != 'stop':
    #     answer = input('').strip()
    #     if answer == 'stop':
    #         for process in processes.values():
    #             print(process)
    #             process.kill()
