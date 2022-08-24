from main_as import collect_data, collect_data_xbox
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiofiles import os
from config import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['XBOX GAME PASS', 'XBOX S']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('Please select a key', reply_markup=keyboard)


@dp.message_handler(Text(equals='XBOX GAME PASS'))
async def game_pass(message: types.Message):
    await message.answer('Please waiting...')
    chat_id = message.chat.id
    await send_data(chat_id=chat_id)


@dp.message_handler(Text(equals='XBOX S'))
async def xbox_s(message: types.Message):
    await message.answer('Please waiting...')
    chat_id = message.chat.id
    await send_data_xbox(chat_id=chat_id)


async def send_data(chat_id=''):
    xbox_card = await collect_data()
    for key, value in xbox_card.items():
        await bot.send_message(chat_id=chat_id,
                               text=f'{key}\n'
                                    f'ЦЕНА: {value[1]}, ЦЕНА СО СКИДКОЙ: {value[2]} \n'
                                    f'Ссылка: {value[0]} ')


async def send_data_xbox(chat_id=''):
    xbox_card = await collect_data_xbox()
    for key, value in xbox_card.items():
        await bot.send_message(chat_id=chat_id,
                               text=f'{key}\n'
                                    f'Статус: {value[0]}\n'
                                    f'ЦЕНА: {value[1]} \n'
                                    f'Ссылка: {value[2]} ')


if __name__ == '__main__':
    executor.start_polling(dp)
