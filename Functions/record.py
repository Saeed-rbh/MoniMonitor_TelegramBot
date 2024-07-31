
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,Update
from telegram.ext import ContextTypes
from Functions.extract_float import extract_float

async def record_daily_Spending(update, context):
    await record(update, context, 'Spending', 'daily')

async def record_daily_Income(update, context):
    await record(update, context, 'Income', 'daily')

async def record_monthly_Spending(update, context):
    await record(update, context, 'Spending', 'monthly')

async def record_monthly_Income(update, context):
    await record(update, context, 'Income', 'monthly')

async def record(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str,Timescale: str) -> None:
    message = update.message.text

    parts = message.split(maxsplit=2)
    if len(parts) < 2:
        if category.lower()[0] == 'e':
            example = '50 Grocery'
        elif category.lower()[0] == 'i':
            example = '1500 Job Payment'
        await update.message.reply_text(
            '• Please use the valid format!!!\n'
            f'- Format: "/{category.lower()[0]} <amount> <reason>"\n'
            f'- Example: "/{category.lower()[0]} {example}"'
        )
        return

    amount = extract_float(parts[1])

    if amount is None:
        await update.message.reply_text(
            '• Please provide a valid number!!!\n'
            f'- Example: "{parts[0]} 50 {parts[2]}"'
        )

    try:
        reason = parts[2]
    except:
        reason = 'No Reason Provided'

    if Timescale == 'daily':
        callback = f"add_to_daily_wallet:{category}:{amount}:{reason}"
    elif Timescale == 'monthly':
        callback = f"add_to_monthly_wallet:{category}:{amount}:{reason}"

    inline_keyboard = [
        [InlineKeyboardButton(
            "Add to Wallet", callback_data=callback
        )],
        [InlineKeyboardButton("Modify", callback_data="modify")]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)

    await update.message.reply_text(
        f'• New <b>{Timescale} {category}</b>\n• Amount: $<b>{amount:.2f}</b>\n• Reason: <b>{reason}</b>',
        parse_mode='HTML',
        reply_markup=reply_markup
    )
