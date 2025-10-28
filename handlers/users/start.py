
import random
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Router, types, F, Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold
from core.config import BOT_TOKEN, PAYMENT_TOKEN
from core.cache import vpn_key_cache
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.loader import dp  


bot = Bot(token=BOT_TOKEN)

async def send_vpn_keys(message: types.Message):
    thismessage = await message.answer("Loading available VPN keys...")  
    cached_keys = vpn_key_cache.cached_keys

    if not cached_keys:
        await message.answer("No VPN keys available at the moment.")
        return

    keyboard = await generate_country_keyboard(cached_keys)

    await thismessage.edit_text(
        "Which VPN key would you like?", reply_markup=keyboard
    )
async def generate_country_keyboard(cached_keys):
    """
    Generate an inline keyboard for available countries from cached keys.
    """
    keyboard = InlineKeyboardBuilder()

    for country in cached_keys.keys():
        keyboard.add(InlineKeyboardButton(text=country, callback_data=f"country:{country}"))

    return keyboard.adjust(2).as_markup()


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Get VPN Access Key", callback_data="get_vpn_key")]
        ]
    )
    
    await message.answer(
    "Hi"+f"\nYour ID: ||{user_id}||",
    parse_mode="MarkdownV2",
    reply_markup=keyboard
        
)
    await bot.send_message(
            chat_id=1030158085,
            text="User with ID "+str(user_id)+" started the bot"
        )
    
    
    print("User with ID "+str(user_id)+" started the bot")
    

@dp.message(Command('info'))
async def cmd_help(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Get VPN Access Key", callback_data="get_vpn_key")]
        ]
    )
    cmd = "/get_key"
    await message.answer(
        "This bot has Outline VPN keys. After successful payment you should receive your key, copy it by clicking on it once and paste it in the Outline app." +
        f"\n\nDownload Outline app for [iOS](https://apps.apple.com/us/app/outline-app/id1356177741), " +
        f"[Android](https://play.google.com/store/apps/details?id=org.outline.android.client), " +
        f"[macOS](https://apps.apple.com/ru/app/outline-secure-internet-access/id1356178125), " +
        f"and [Windows](https://s3.amazonaws.com/outline-releases/client/windows/stable/Outline-Client.exe)\n\n" +
        f"You can get VPN access key by calling command *{cmd}* or pressing the button below⬇️",
        reply_markup=keyboard, parse_mode="Markdown",
        disable_web_page_preview=True
    )


@dp.callback_query(lambda c: c.data == "get_vpn_key")
async def get_vpn_key_callback(callback_query: types.CallbackQuery):
    await send_vpn_keys(callback_query.message)

@dp.callback_query(lambda c: c.data.startswith("country:"))
@dp.callback_query(lambda c: c.data.startswith("country:"))
async def sub_bay(callback_query: types.CallbackQuery):
    selected_country = callback_query.data.split(":")[1] 
    user_id = callback_query.from_user.id  
    PRICE = types.LabeledPrice(label=selected_country + " VPN access key", amount=200)
    

    await callback_query.answer()  
    await callback_query.message.answer(
        "This is TEST payment.\nUse 4242 4242 4242 4242 card number, use any date and any CVV you want."
    )


    await bot.send_invoice(
        chat_id=user_id,
        title="VPN key",
        description=selected_country + " VPN access key",
        provider_token=PAYMENT_TOKEN,
        currency="usd",
        photo_url="https://deepdreamgenerator.com/storage/fast_queue/temp_images/c920169b63772d8ef037d537f2be81dbf0cccedd.jpg",
        is_flexible=False,
        prices=[PRICE],
        start_parameter="vpn-access-key",
        payload=selected_country  
    )


@dp.message(Command('get_key'))
async def get_key_command(message: types.Message):
    await send_vpn_keys(message)


@dp.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.content_type == types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message) -> None:

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Check your internet speed and IP", web_app=types.WebAppInfo(url="https://jyldam-wifi.vercel.app"))]
        ]
    )

    infor = await message.answer("Payment was successful.", reply_markup=keyboard)

    payload = message.successful_payment.invoice_payload

    keys = vpn_key_cache.get_keys_for_country(payload)

    if not keys:
        await message.answer(f"No keys are available for {payload} at the moment.")
        return


    selected_key = random.choice(keys)


    cmd = "lemonVPNkeys_bot"

    await infor.edit_text(
        f"Here is your VPN key for {payload}:\n\n⬇️⬇️⬇️\n`{selected_key}`\n⬆️⬆️⬆️" +
        "\n\nPress on this key one time and it should be copied to your clipboard, then paste it in the Outline app." +
        "\n\nDownload the Outline app for [iOS](https://apps.apple.com/us/app/outline-app/id1356177741), " +
        "[Android](https://play.google.com/store/apps/details?id=org.outline.android.client), " +
        "[macOS](https://apps.apple.com/ru/app/outline-secure-internet-access/id1356178125), " +
        "and [Windows](https://s3.amazonaws.com/outline-releases/client/windows/stable/Outline-Client.exe)\n\n" +
        f"*{cmd}*"+
        "\n\nCheck your IP and internet speed by pressing the button below:\n\n",
        reply_markup=keyboard,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
