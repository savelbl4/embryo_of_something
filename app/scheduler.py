from datetime import datetime
import schedule
import time
import random
from app.utils.text import replace
from app.data import chats, stickers
from app.utils.stats import get_server_stats
from app.tg import tb



def sayer():
    # schedule.every(1).to(60).minutes.do(send_weekends)  # хз как это работает
    # schedule.every().day.at("11:11:11").do(send_workdays)
    schedule.every().day.at("11:11:10").do(send_daily_stats)
    while True:
        schedule.run_pending()
        time.sleep(1)

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


def send_daily_stats():
    try:
        tb.send_message(chats[0], get_server_stats(), parse_mode='Markdown')
    except Exception as e:
        print(f"Ошибка отправки в чат {chats[0]}: {e}")
