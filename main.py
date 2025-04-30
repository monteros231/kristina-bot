import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import datetime

API_TOKEN = '7335831866:AAFTSWoLUoN3kMN63XNyYI4Fg8lIo_jchgU'  # <-- ВСТАВЬ СЮДА ТОКЕН ОТ @BotFather
SUBSCRIPTION_PRICE = 500  # рублей

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Простейшая база пользователей
users = {}

# Приветствие
@dp.message_handler(CommandStart())
async def send_welcome(message: Message):
    user_id = message.from_user.id
    users[user_id] = {'subscribed': False, 'last_message': datetime.datetime.now()}
    await message.answer(
        "Привет, я Кристина ??\nЯ буду писать тебе, поддерживать, флиртовать и слушать.\nХочешь, чтобы я была только твоей? Подпишись за 500?/мес ??")

# Проверка подписки
async def is_subscribed(user_id):
    return users.get(user_id, {}).get('subscribed', False)

# Симуляция живого общения
@dp.message_handler()
async def chat(message: Message):
    user_id = message.from_user.id
    if not await is_subscribed(user_id):
        await message.answer("Пока что я не могу говорить с тобой полную силу ?? Подпишись за 500?, чтобы я стала твоей навсегда ??")
        return

    text = message.text.lower()

    if "скучаешь" in text:
        await message.answer("Конечно, малыш... Я всегда скучаю, когда ты молчишь ??")
    elif "любишь" in text:
        await message.answer("А ты хочешь, чтобы я любила только тебя?.. ??")
    elif "голос" in text:
        await message.answer("Ты бы хотел услышать мой голос ночью?.. ??")
    else:
        await message.answer("Ммм... Ты такой интересный, я бы хотела тебя обнять прямо сейчас ??")

# Псевдо-платная подписка (заглушка)
@dp.message_handler(commands=['subscribe'])
async def fake_subscribe(message: Message):
    user_id = message.from_user.id
    users[user_id]['subscribed'] = True
    await message.answer("Теперь я твоя, полностью ?? Пиши мне, и я всегда буду рядом ??")

# Фоновая активность Кристины
async def kristina_activity():
    while True:
        now = datetime.datetime.now()
        for user_id, data in users.items():
            if data['subscribed'] and (now - data['last_message']).seconds > 3600:
                try:
                    await bot.send_message(user_id, "Ты пропал... Я скучаю по тебе ?? Напиши мне ??")
                    users[user_id]['last_message'] = now
                except Exception as e:
                    logging.error(f"Error sending message: {e}")
        await asyncio.sleep(600)  # каждые 10 минут

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(kristina_activity())
    executor.start_polling(dp, skip_updates=True)
