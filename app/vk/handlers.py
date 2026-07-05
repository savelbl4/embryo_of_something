from vkbottle import Bot
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule
from app.utils.stats import get_server_stats
from app.utils.text import replace, im_here
from app.db import upsert_identity, link_by_code, get_linked_identity


from app.config import VK_TOKEN, VK_GROUP

vb = Bot(token=VK_TOKEN)


class TextStartsWithRule(ABCRule[Message]):
    def __init__(self, prefix: str):
        self.prefix = prefix.lower()

    async def check(self, message: Message) -> bool:
        return bool(message.text) and message.text.lower().startswith(self.prefix)


def vb_listener():
    try:
        vb.run_forever()
    except:
        print("Lost connection!")

async def get_vk_user_info(user_id: int):
    users = await vb.api.users.get(
        user_ids=[user_id],
        fields=["domain", "screen_name"]
    )

    if not users:
        return None

    user = users[0]

    return {
        "display_name": f"{user.first_name} {user.last_name}",
        "username": getattr(user, "domain", None) or getattr(user, "screen_name", None),
    }

async def ensure_identity(message: Message) -> int:
    info = await get_vk_user_info(message.from_id)

    return upsert_identity(
        platform="vk",
        platform_user_id=message.from_id,
        platform_chat_id=message.peer_id,
        username=info["username"] if info else None,
        display_name=info["display_name"] if info else None,
    )

def get_identity_keyboard():
    keyboard = Keyboard(one_time=False, inline=False)

    keyboard.add(
        Text("Идентификация"),
        color=KeyboardButtonColor.PRIMARY,
    )

    return keyboard

def get_main_keyboard():
    keyboard = Keyboard(one_time=False, inline=False)

    keyboard.add(
        Text("кнопка"),
        color=KeyboardButtonColor.PRIMARY,
    )

    keyboard.add(
        Text("статистика"),
        color=KeyboardButtonColor.PRIMARY,
    )

    keyboard.add(
        Text("федя ты где"),
        color=KeyboardButtonColor.PRIMARY,
    )

    return keyboard

def is_vk_linked(identity_id: int) -> bool:
    linked_tg = get_linked_identity(identity_id, "telegram")
    return linked_tg is not None

@vb.on.message(text="Идентификация")
async def identify(message: Message):
    identity_id = await ensure_identity(message)

    if is_vk_linked(identity_id):
        await message.answer("VK уже привязан к Telegram.")
        return

    await message.answer(
        (
            "Чтобы привязать VK к Telegram:\n\n"
            "1. Напиши Telegram-боту команду /link\n"
            "2. Получи код\n"
            "3. Отправь сюда команду:\n\n"
            "/link КОД"
        )
    )

@vb.on.message(text=["/link <code>", "!link <code>"])
async def link_vk(message: Message, code: str):
    identity_id = await ensure_identity(message)

    if link_by_code(identity_id, code):
        await message.answer(
            "VK успешно привязан к Telegram.",
            keyboard=get_main_keyboard()
        )
    else:
        await message.answer(
            "Код неверный или уже истёк.",
            keyboard=get_identity_keyboard()
        )


@vb.on.message(text=["ты где", "федя ты где"])
async def where_are_you(message: Message):
    await message.answer(im_here())


@vb.on.message(text=["/stats", "!stats", "статистика"])
async def stats(message: Message):
    await message.answer(get_server_stats())


@vb.on.message(TextStartsWithRule("переведи"))
async def translate(message: Message):
    await message.answer(replace(message.text.lower()))


@vb.on.message()
async def fallback(message: Message):
    from pprint import pprint
    pprint(message)

    identity_id = await ensure_identity(message)

    if not is_vk_linked(identity_id):
        await message.answer(
            "VK пока не привязан к Telegram.",
            keyboard=get_identity_keyboard()
        )
        return
    else:
        await message.answer(
            "чего изволите?",
            keyboard=get_main_keyboard()
        )

    if not message.text:
        return

    text = message.text.strip()
    text_lower = text.lower()

    print(text_lower)
