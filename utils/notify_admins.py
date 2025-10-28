import logging
from aiogram import Bot

from core.config import ADMINS


async def on_startup_notify(bot: Bot):

    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=admin, text="Bot started working.")
        except Exception as err:
            logging.exception(err)


async def on_shutdown_notify(bot: Bot):

    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=admin, text="Bot stopped working.")
        except Exception as err:
            logging.exception(err)