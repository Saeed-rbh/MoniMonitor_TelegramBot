from datetime import datetime
from Functions.read_from_db import read_from_db
from Functions.extract_by_date import extract_by_date
from Functions.analyze_transactions import analyze_transactions
from Functions.plot_by_date import plot_by_date
# from telegram import InputMediaPhoto
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


async def analyze(update, context):
    user_id = str(update.message.from_user.id)

    message = await update.message.reply_text(
        '• Please wait...\n',
        parse_mode='HTML'
    )

    # daily_transactions = read_from_db(user_id, 'Daily')
    # monthly_transactions = read_from_db(user_id, 'Monthly')
    [daily_transactions,monthly_transactions] = read_from_db(user_id)

    if len(daily_transactions) == 0 and len(monthly_transactions) == 0:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message.message_id)
        await update.message.reply_text(
            '----------\n'
        '• No transactions found !!!\n'
        '----------\n'
        ' Start tracking your transactions:\n\n'
        '• <b>Spending</b>(record your Spending):\n- Format:  "/e amount reason"\n- Example: <b>/e 50 Grocery</b>\n\n'
        '• <b>Income</b>(record your Income):\n- Format:  "/i amount reason"\n- Example: <b>/i 1500 Job Payment</b>\n'
        '----------\n',
        parse_mode='HTML')
        return
    
    else:
        daily_Income, daily_Spending = analyze_transactions(daily_transactions,'daily')
        monthly_Income, monthly_Spending = analyze_transactions(monthly_transactions,'monthly')
        Income = daily_Income + monthly_Income
        Spending = daily_Spending + monthly_Spending
        Balance = Income - Spending
        Date = datetime.now().strftime('%B - %Y')
        Balance_sign = '+' if Balance >= 0 else '-'
        Income_by_date = extract_by_date(daily_transactions,'Income')
        Spending_by_date = extract_by_date(daily_transactions,'Spending')

        balance_by_date = [Income - Spending for Income, Spending in zip(Income_by_date, Spending_by_date)]
        # Income_image = plot_by_date(Income_by_date,monthly_Income,'Income')
        # Spending_image = plot_by_date(Spending_by_date,-monthly_Spending,'Spending')
        # balance_by_date_image = plot_by_date(balance_by_date,monthly_Income-monthly_Spending,'Balance')
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message.message_id)

        message = ('----------\n'
                    '• <b>Your Balance to date</b>:\n'
                    f'• {Date}\n'
                    '----------\n'
                    f'• Total <b>Income:</b>  +${round(Income,2)}\n'
                    f'• Totla <b>Spending:</b> -${round(Spending,2)}\n'
                    f'• Current <b>Balance:</b>  ${Balance_sign}{round(abs(Balance),2)}\n'
                    '----------\n')
        
        # Income_image_bytes = Income_image.getvalue()
        # Spending_image_bytes = Spending_image.getvalue()

        # media_group = [
            # InputMediaPhoto(media=balance_by_date_image, caption=message, parse_mode='HTML'),
            # InputMediaPhoto(media=Income_image_bytes ),
            # InputMediaPhoto(media=Spending_image_bytes)
            
        # ]
        
        inline_keyboard = [
            [InlineKeyboardButton("Hide it", callback_data="Hide_it")]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)

        # await update.message.reply_media_group(media=media_group)
        await update.message.reply_text(message, parse_mode='HTML',
            reply_markup=reply_markup)
