from Functions.read_from_db import read_from_db
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def delete_transaction(update, context):
    message = update.message.text

    try:
        transaction_number = message.split()[-1]
    except ValueError:
        await update.message.reply_text(
            'Invalid format. Please use the format: "/d <Number>"')
        return
    
    user_id = str(update.message.from_user.id)

    [daily_records, monthly_records] = read_from_db(user_id)

    if int(transaction_number[0]) != 0:
        message_type = 'Daily'
        transaction_number = int(transaction_number)-1
        records = daily_records
    elif int(transaction_number[0]) == 0:
        message_type = 'Monthly'
        transaction_number = int(str(transaction_number)[1:])-1
        records = monthly_records
   
    if transaction_number > len(records):
        await update.message.reply_text(f"Transaction {transaction_number} not found.")
        return
    
    toDelete = records[transaction_number]

    message = ('• <b>Do you want to deleted it?</b>\n\n')
    message += (
            f"• <b>{message_type}</b> Transaction:\n"
            f"• #{transaction_number+1} • {toDelete['Category']}\n"
        )
    if message_type == 'daily':
        message += (
                f"• <b>Date:</b> {toDelete['Month']}/{toDelete['Day']} - {toDelete['Time']}\n"
            )
    message += (
            f"• <b>Amount:</b> {toDelete['Amount']}\n"
            f"• <b>Reason:</b> {toDelete['Reason']}\n\n"
        )

    inline_keyboard = [
            [InlineKeyboardButton("Delete it", callback_data=f"Delete_it:{message_type}:{toDelete['Transaction_Id']}:{transaction_number+1}")],
            [InlineKeyboardButton("Ignore", callback_data="Ignore_it")]
        ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    await update.message.reply_text(message, parse_mode='HTML',
            reply_markup=reply_markup)
    