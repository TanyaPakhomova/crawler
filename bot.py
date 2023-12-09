from aiogram.utils.markdown import hlink
import json
from aiogram import F
from aiogram.filters import Command
import asyncio
import logging
import sys
import os
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.environ.get("BOT_TOKEN")

# Load data into memory
f = open('bot_data.json')
d = json.load(f)
category_id = d['data']['category']['id']
products = d['data']['products']['products']
f.close()


# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message(F.text, Command("min_price"))
async def min_price_handler(message: types.Message):
   text = message.text
   argument = text.strip("/min_price")
   if argument == '':
      argument = 1
   else:
     argument = int(argument)

   pps = find_cheapest(argument)
   for p in pps:
      await message.answer(p.display())

class Product:
    def __init__(self, name, brand, url, price): 
        self.name = name
        self.brand = brand 
        self.url = url
        self.price = price

    def display(self):
        return self.brand + '\n' + self.name + '\n' + str(self.price) + '\n\n----------\n' + str(self.url) 

def find_cheapest(cnt): 
    pps = []

    for p in products:
        price = p['price']['actual']['amount']
        url = hlink('ссылка', 'https://goldapple.ru' + p['url'])
        pps.append(Product(p['name'], p['brand'], url, price))
    
    result = sorted(pps, key=lambda x: x.price, reverse=False)
    return result[0:cnt]



async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
