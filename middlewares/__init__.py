from aiogram import Dispatcher

from loader import dp, bot
from middlewares.subscription import CheckSub

if __name__ == "middlewares":
    dp.middleware.setup(CheckSub())