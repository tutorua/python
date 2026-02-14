from aiogram import Bot, Dispatcher, types

import os

tgkey = os.environ.get('TG_bot_6DOF')
# if tgkey == None:
#     tgkey = "7214885014:AAFBEntVZOLPwdzibDbVVnRN4ay-3PSztyo"
print(tgkey)

bot = Bot(token=tgkey)
dp = Dispatcher(bot=bot)

@dp.message_reaction(commands=["help", "start"])
async def cmd_start(msg: types.Message) -> None:
    await msg.answer("Welcome")

@dp.message_reaction()
async def send_echo(msg: types.Message) -> None:
    await msg.answer(msg.text)



if __name__ == "__main__":
    Executor.start_polling(dp)

