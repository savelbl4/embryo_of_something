from vkbottle import Bot
from vkbottle.bot import Message
from app.utils.stats import get_server_stats
from app.utils.text import replace, im_here


from app.config import VK_TOKEN, VK_GROUP

vb = Bot(token=VK_TOKEN)

def vb_listener():
    try:
        vb.run_forever()
    except:
        print("Lost connection!")

@vb.on.message()
async def greet(message: Message):
    if not message.text:
        return
    text_lower = message.text.lower()
    print(text_lower)
    if 'ты где' in text_lower:
        await message.answer(im_here())
    if 'переведи' in text_lower:
        await message.answer(replace(text_lower))
    if 'статистика' in text_lower:
        await message.answer(get_server_stats())

