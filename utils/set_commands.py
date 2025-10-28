from aiogram import types, Bot

def get_commands_kk():
    commands = [
        types.BotCommand(command="/start", description="Ботты іске қосу"),
        types.BotCommand(command="/info", description="Мәлімет"),
        types.BotCommand(command="/get_key", description="VPN кілтін алу")
    ]
    return commands

def get_commands_ar():
    commands = [
        types.BotCommand(command="/start", description="تشغيل البوت"),
        types.BotCommand(command="/info", description="معلومات"),
        types.BotCommand(command="/get_key", description="احصل على مفتاح الوصول إلى VPN")
    ]
    return commands

def get_commands_en():
    commands = [
        types.BotCommand(command="/start", description="Start the bot"),
        types.BotCommand(command="/info", description="Info"),
        types.BotCommand(command="/get_key", description="Get VPN key")
    ]
    return commands

def get_commands_ru():
    commands = [
        types.BotCommand(command="/start", description="Запустить бота"),
        types.BotCommand(command="/info", description="Информация"),
        types.BotCommand(command="/get_key", description="Получить ключ VPN")
    ]
    return commands



async def set_default_commands(bot: Bot):
    await bot.set_my_commands(get_commands_ar(), scope=types.BotCommandScopeAllPrivateChats(), language_code="ar")
    await bot.set_my_commands(get_commands_ru(), scope=types.BotCommandScopeAllPrivateChats(), language_code="ru")
    await bot.set_my_commands(get_commands_en(), scope=types.BotCommandScopeAllPrivateChats(), language_code="en")
    await bot.set_my_commands(get_commands_kk(), scope=types.BotCommandScopeAllPrivateChats(), language_code="kk")