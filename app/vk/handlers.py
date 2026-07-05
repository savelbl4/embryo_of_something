from vkbottle import Bot
from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule
from app.utils.stats import get_server_stats
from app.utils.text import replace, im_here
from app.db import upsert_identity, link_by_code


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

@vb.on.message(text=["/link <code>", "!link <code>"])
async def link_vk(message: Message, code: str):
    identity_id = upsert_identity(
        platform="vk",
        platform_user_id=message.from_id,
        platform_chat_id=message.peer_id,
        username=None,
        display_name=None,
    )

    if link_by_code(identity_id, code):
        await message.answer("VK успешно привязан к Telegram.")
    else:
        await message.answer("Код неверный или уже истёк.")


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
    if not message.text:
        return

    text = message.text.strip()
    text_lower = text.lower()

    print(text_lower)
