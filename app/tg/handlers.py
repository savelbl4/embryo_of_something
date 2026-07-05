import telebot
from telebot import types
import random
from app.utils.stats import get_server_stats
from app.utils.ssh import test_ssh
from app.utils.vpn import send_vpn_config
from app.data import chats, stickers, letters, smile
from app.config import TG_TOKEN, VK_TOKEN, VK_GROUP, PUBLIC_IP
from app.utils.text import replace, im_here, lucky
from app.db import upsert_user

tb = telebot.TeleBot(TG_TOKEN)


def get_custom_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('стикер'), types.KeyboardButton('где'))
    keyboard.row(types.KeyboardButton('мне повезёт'))
    keyboard.row(types.KeyboardButton('статистика'))
    return keyboard


def tb_listener():
    try:
        print(f"The Bot is online (id: {tb.get_me().id})...")
        tb.infinity_polling(
            skip_pending=True,
            none_stop=True,
        )
    except:
        print("Lost connection!")


@tb.message_handler(commands=['start'])
def handle_start(message):
    chatid = message.chat.id
    # tb.send_message(
    #     chatid,
    #     "Выберите действие:",
    #     reply_markup=get_custom_keyboard()
    # )
    upsert_user(message)
    tb.send_sticker(
        chatid,
        stickers[0],
        reply_markup=get_custom_keyboard()
    )


@tb.message_handler(commands=['stats'])
def handle_stats(message):
    chatid = message.chat.id
    print(f"отправка в чат {chatid}")
    tb.send_message(chatid, get_server_stats(), parse_mode='Markdown')


@tb.message_handler(commands=["vpn"])
def handle_vpn(message):
    chatid = message.chat.id
    if str(chatid) not in chats:
        return
    bio, msg = send_vpn_config()

    if bio == 0:
        tb.send_message(chatid, msg)

    print(f"отправка vpn в чат {chatid}")

    tb.send_photo(
        chatid,
        bio,
        caption=msg,
        parse_mode="HTML"
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
def handle_mne(message):
    chatid = message.chat.id
    tb.send_message(chatid, lucky())


@tb.message_handler(func=lambda m: m.text == 'статистика')
def handle_stat(message):
    chatid = message.chat.id
    tb.send_message(chatid, get_server_stats(), parse_mode='Markdown')

@tb.message_handler(commands=["test_ssh"])
def handle_ssh(message):
    chatid = message.chat.id

    if str(chatid) not in chats:
        return

    tb.send_message(chatid, test_ssh())

@tb.message_handler(func=lambda m: True)
def answer(message):
    chatid = message.chat.id
    # для дебага
    # print(chatid)
    # print(message)
    if message.content_type == 'text' and str(chatid) in chats:
        if 'привет бот' in message.text:
            tb.send_message(chatid, 'привет')
        if 'переведи' in message.text.lower():
            tb.send_message(chatid, replace(message.text.lower()))
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
