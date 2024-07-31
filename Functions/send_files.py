from datetime import datetime
from telegram import Update
from telegram.ext import CallbackContext
import os
from Functions.get_transactions import get_transactions

async def send_files(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    user_data_dir = os.path.join('user_data', user_id)

    today_date = datetime.now()
    formatted_date = today_date.strftime("%B_%Y")
    
    daily_transactions_file = f'Daily_Transactions_{formatted_date}.csv'
    daily_transactions_path = os.path.join(user_data_dir, daily_transactions_file)

    monthly_transactions_file = 'Monthly_Transactions.csv'
    monthly_transactions_path = os.path.join(user_data_dir, monthly_transactions_file)

    os.makedirs(user_data_dir, exist_ok=True)

    daily_transactions = get_transactions(user_id, 'daily')
    monthly_transactions = get_transactions(user_id, 'monthly')

    daily_fieldnames = ['Timestamp', 'Category', 'Amount', 'Reason']
    monthly_fieldnames = ['Category', 'Amount', 'Reason']

    if daily_transactions:
        await update.message.reply_document(open(daily_transactions_path, 'rb'), caption='• Here is your <b>Daily</b> Transactions file', parse_mode='HTML')
    else:
        await update.message.reply_text('• No <b>Daily</b> Transactions file found.', parse_mode='HTML')

    if monthly_transactions:
        await update.message.reply_document(open(monthly_transactions_path, 'rb'), caption='• Here is your <b>Monthly</b> Transactions file', parse_mode='HTML')
    else:
        await update.message.reply_text('• No <b>Monthly</b> Transactions file found.', parse_mode='HTML')

