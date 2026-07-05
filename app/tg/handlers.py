import telebot
from telebot import types
import random
from app.utils.stats import get_server_stats
from app.utils.ssh import test_ssh
from app.utils.vpn import send_vpn_config
from app.data import chats, stickers, letters, smile
from app.config import TG_TOKEN
from app.utils.text import replace, im_here, lucky
from app.db import upsert_user, add_sticker_if_not_exists, get_random_sticker

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
    if upsert_user(message):
        tb.send_sticker(
            chatid,
            stickers[0],
            reply_markup=get_custom_keyboard()
        )
    else:
        tb.send_message(
            chatid,
            "а я тебя знаю",
            reply_markup = get_custom_keyboard()
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

@tb.message_handler(commands=["test_ssh"])
def handle_ssh(message):
    chatid = message.chat.id

    if str(chatid) not in chats:
        return

    tb.send_message(chatid, test_ssh())


@tb.message_handler(content_types=['sticker'])
def handle_sticker(message):
    chatid = message.chat.id
    sticker = message.sticker

    print(f"Sticker from {chatid}")
    print(sticker.file_id)

    is_new = add_sticker_if_not_exists(sticker)

    if is_new:
        print("New sticker added to DB")
    else:
        print("Sticker already exists")

    tb.send_message(chatid, lucky())

    # from pprint import pprint
    # pprint(message.json)


@tb.message_handler(func=lambda m: m.text == 'стикер')
def handle_button_sticker(message):
    chatid = message.chat.id
    tb.send_sticker(chatid, get_random_sticker())


@tb.message_handler(func=lambda m: m.text == 'где')
def handle_button_gde(message):
    chatid = message.chat.id
    tb.send_message(chatid, im_here())


@tb.message_handler(func=lambda m: m.text == 'мне повезёт')
def handle_button_mne(message):
    chatid = message.chat.id
    tb.send_message(chatid, lucky())


@tb.message_handler(func=lambda m: m.text == 'статистика')
def handle_button_stat(message):
    chatid = message.chat.id
    tb.send_message(chatid, get_server_stats(), parse_mode='Markdown')

@tb.message_handler(content_types=[
    'text',
    'sticker',
    'animation',
    'photo',
    'video',
    'document',
    'voice',
    'audio'
])
def handle_all_answer(message):
    chatid = message.chat.id
    # для дебага
    # print(chatid)
    # print(message)
    from pprint import pprint
    pprint(message.json)
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
    # else:
    #     from pprint import pprint
    #     pprint(message.json)
