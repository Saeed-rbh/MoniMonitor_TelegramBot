    
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,Update
from telegram.ext import ContextTypes
from Functions.read_from_db import read_from_db

async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = int(update.message.from_user.id)

    message = await update.message.reply_text(
        '• Please wait...\n',
        parse_mode='HTML'
    )

    [daily_records,monthly_records] = read_from_db(user_id)

    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message.message_id)

    if len(daily_records) > 0 or len(monthly_records) > 0:
        message = ('----------\n'
                   '• <b>Do you want to clear your history?</b>\n'
                   '----------\n\n')
        if len(monthly_records) > 0:
            message += f'• <b>{len(monthly_records)}</b> Monthly Transactions\n'
        if len(daily_records) > 0:
            message += f'• <b>{len(daily_records)}</b> Daily Transactions\n'

        inline_keyboard = [
            [InlineKeyboardButton("Clear History!", callback_data=f"Clear_History:{user_id}")],
            [InlineKeyboardButton("Ignore", callback_data="Hide_it")]
        ]

    else:
        message = ('----------\n'
                   '• <b>No History Found</b>\n'
                   '----------\n')
        
        inline_keyboard = [
            [InlineKeyboardButton("New Transaction", callback_data="new_transaction")],
            [InlineKeyboardButton("Ignore", callback_data="Hide_it")]
        ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    await update.message.reply_text(message, parse_mode='HTML', reply_markup=reply_markup)
                                 
