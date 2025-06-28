import telebot
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

TG_TOKEN = os.getenv('TG_TOKEN')
VK_TOKEN = os.getenv('VK_TOKEN')
VK_GROUP = os.getenv('VK_GROUP')

tb = telebot.TeleBot(TG_TOKEN)
print(f"The Bot is online (id: {tb.get_me().id})...")
vb = SimpleLongPollBot(tokens=VK_TOKEN, group_id=VK_GROUP)

chats = [
    '2501359',
    '6267957',
    '-1001348677218',
]
stickers = [
    'CAACAgIAAxkBAAIS1mJEyRXuHigJTbrBMNuof5BQdMMKAAKEAQACy4gZETK1KP8R8jW1IwQ',
    'CAACAgIAAxkBAAIS1WJEx-fd_sZy3C36hTqNE_NeVr3XAAJIHgAC6VUFGJDLIuAKbjsWIwQ',
    'CAACAgQAAxkBAAEEStdiQL17uUKsMMmyghM9jQdj9LGjmAACAwIAAvAeaiEgvmSCXjXaWSME',
    'CAACAgIAAxkBAAIS12JEyzl6mRRJCtRo_1FS-OaKmgHlAAL_DgACB_GBScLPRvI6stG4IwQ',  # неа
    'CAACAgIAAxkBAAIS2GJEy3FKEn2sF9ei9PWay-x6-wPWAAIbCQACGELuCNy5pdXzSq7IIwQ',
    'CAACAgIAAxkBAAIS2WJEy9RFZaz3_yIEZFx7C3CU4GCZAAKZAAPLiBkRnMRwPqB1w3AjBA',
    'CAACAgEAAxkBAAIS2mJEzFzIvAKfPfFZ5KxvAnhuC-dOAAI6AAOhBQwN3srafQKK11kjBA',
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


def replace(string) -> str:
    arr = []
    for name in string:
        if i.get(name.upper()):
            arr.append(i.get(name.upper()))
        else:
            arr.append(name)
    return ''.join(arr)


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
            tb.send_message(replace(message.text.lower()))
        if 'федя' in message.text.lower():
            if 'ты как' in message.text.lower():
                tb.send_sticker(chatid, random.choice(stickers))
            if 'ты где' in message.text.lower():
                tb.send_message(chatid, im_here())


@tb.message_handler(content_types=['sticker'])
def handle_sticker(message):
    chatid = message.chat.id
    print(f"Sticker from {chatid}")
    print(message)
    # Здесь можешь отвечать на стикер, если хочешь
    tb.send_message(chatid, "Ты прислал стикер! 😎")

def im_here():
    res = requests.request('get', 'https://vk.com/upload.php?act=myip')
    ros = res.text
    pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
    ip_address = pattern.findall(ros)
    return f'я тут {ip_address[0]}'


def job():
    hour = datetime.now().hour
    if 9 < int(hour) < 20:
        tb.send_sticker('2501359', random.choice(stickers))


def send_weekend():
    if datetime.isoweekday(datetime.today()) <= 5:
        tb.send_message(chats[0], text='11:11')
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
    schedule.every(1).to(60).minutes.do(job)
    schedule.every().day.at("11:11:11").do(send_weekend)
    while True:
        schedule.run_pending()
        time.sleep(1)


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
