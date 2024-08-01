from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Updater, CommandHandler, CallbackContext


async def UserData(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    keyboard = [
        [InlineKeyboardButton("Open Mini App", web_app=WebAppInfo(url='https://saeedarabha.com/MoneyMonitor'))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Click the button below to open the mini app:", reply_markup=reply_markup)

