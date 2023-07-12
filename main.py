import json
import logging
import os
from asyncio import sleep
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import hlink
from background import keep_alive
from parse import main
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level='DEBUG', filename="logs.log", filemode="w")
# logging.getLogger('aiogram').setLevel('INFO')

token = os.environ['TOKEN_BOT']
bot = Bot(token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
category_bots = KeyboardButton(text='Чат-боты')
category_parsing = KeyboardButton(text='Парсинг')
keyboard.add(category_parsing).add(category_bots)

dev_id = 1578668223


# 0-parsing, 1-bots


async def on_startup(_):
    await bot.send_message(chat_id=dev_id, text='bot is running')


async def on_shutdown(_):
    await bot.send_message(chat_id=dev_id, text='bot is off')


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, text='Привет. Данный бот позволяет получать предложения о работе по выбранной категории с сайта FL.ru', reply_markup=keyboard)
    await bot.send_message(chat_id=dev_id, text=f'Новый пользователь с ником @{message.from_user.username}')


@dp.message_handler(lambda message: 'Парсинг' in message.text)
async def send_parsing_list(message: types.Message):
    await message.answer('Please waiting...')
    main()
    with open('all.json', 'r') as file:
        categories = json.load(file)
        for index, item in enumerate(categories[0]):
            if index % 20 == 0:
                await sleep(0)
            else:
                await bot.send_message(message.from_user.id, text=f"{hlink(item['title'], item['link'])}\n\n{item['description']}\n\n{item['date']}\n", disable_web_page_preview=True)


@dp.message_handler(lambda message: 'Чат-боты' in message.text)
async def send_bots_list(message: types.Message):
    await message.answer('Please waiting...')
    main()
    with open('all.json', 'r') as file:
        categories = json.load(file)
        for index, item in enumerate(categories[1]):
            if index % 20 == 0:
                await sleep(3)
            else:
                await bot.send_message(message.from_user.id, text=f"{hlink(item['title'], item['link'])}\n\n{item['description']}\n\n{item['date']}\n", disable_web_page_preview=True)


@dp.message_handler(commands='логи')
async def send_logs(message):
    await message.reply_document(open('logs.log', 'rb'))


if __name__ == '__main__':
    keep_alive()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
