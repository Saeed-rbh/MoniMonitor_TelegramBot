from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from Functions.read_from_db import read_from_db

async def history(update, context):

    user_id = str(update.message.from_user.id)

    message = await update.message.reply_text(
        '• Please wait...\n',
        parse_mode='HTML'
    )

    [daily_records,monthly_records] = read_from_db(user_id)

    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message.message_id)

    if len(daily_records) == 0 and len(monthly_records) == 0:
        message = ('----------\n'
                   '• <b>No History Found</b>\n'
                   '----------\n')
        
        inline_keyboard = [
            [InlineKeyboardButton("New Transaction", callback_data="new_transaction")],
            [InlineKeyboardButton("Ignore", callback_data="Hide_it")]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await update.message.reply_text(message, parse_mode='HTML',
                reply_markup=reply_markup)
    
        return

    listNum = 0
    Messagelength = 10
    if monthly_records is not None and len(monthly_records) > 0:
        listNum += 1
        message = (
        f'#List_{listNum}\n'
        '----------\n'
        '• <b>Your Monthly Transaction History</b>:\n'
        '----------\n')

        counter = 0
        
        for number,entry in enumerate(monthly_records):
            if entry['Category'] == 'Spending':
                BalanceIcon = '🔴'
            elif entry['Category'] == 'Income':
                BalanceIcon = '🟢'
            else:
                BalanceIcon = '⚪️'
            
            if number < counter+Messagelength:
                message += (
                    f"{BalanceIcon} #0{number+1} • {entry['Category']}\n"
                    f"• <b>Amount:</b> {entry['Amount']}\n"
                    f"• <b>Reason:</b> {entry['Reason']}\n\n"
                )
            elif number == counter+Messagelength:
                listNum += 1
                await update.message.reply_text(message, parse_mode='HTML')
                message = (
                f'#List_{listNum}\n'
                '----------\n'
                '• <b>Your Monthly Transaction History</b>:\n'
                '----------\n')
                message += (
                    f"{BalanceIcon} #0{number+1} • {entry['Category']}\n"
                    f"• <b>Amount:</b> {entry['Amount']}\n"
                    f"• <b>Reason:</b> {entry['Reason']}\n\n"
                )
                counter += Messagelength
        await update.message.reply_text(message, parse_mode='HTML')
    
    
    if daily_records is not None and len(daily_records) > 0:
        listNum += 1
        message = (
        f'#List_{listNum}\n'
        '----------\n'
        '• <b>Your Daily Transaction History</b>:\n'
        '----------\n')
        
        counter = 0
        for number,entry in enumerate(daily_records):
            if entry['Category'] == 'Expense':
                BalanceIcon = '🔴'
            elif entry['Category'] == 'Income':
                BalanceIcon = '🟢'
            else:
                BalanceIcon = '⚪️'
            if number < counter+Messagelength:
                message += (
                    f"{BalanceIcon} #{number+1} • {entry['Category']}\n"
                    f"• <b>Date:</b> {entry['Timestamp'][2:10]} - {entry['Timestamp'][11:]}\n"
                    f"• <b>Amount:</b> {entry['Amount']}\n"
                    f"• <b>Reason:</b> {entry['Reason']}\n\n"
                )
            elif number == counter+Messagelength:
                listNum += 1
                await update.message.reply_text(message, parse_mode='HTML')
                message = (
                    f'#List_{listNum}\n'
                    '----------\n'
                    '• <b>Your Daily Transaction History</b>:\n'
                    '----------\n')
                message += (
                    f"{BalanceIcon} #{number+1} • {entry['Category']}\n"
                    f"• <b>Date:</b> {entry['Timestamp'][2:10]} - {entry['Timestamp'][11:]}\n"
                    f"• <b>Amount:</b> {entry['Amount']}\n"
                    f"• <b>Reason:</b> {entry['Reason']}\n\n"
                )
                counter += Messagelength

   

    inline_keyboard = [
            [InlineKeyboardButton("Delete transaction", callback_data="Delete_transaction")],
            [InlineKeyboardButton("Modify transaction", callback_data="Modify_transaction")]
        ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    await update.message.reply_text(message, parse_mode='HTML',
            reply_markup=reply_markup)
   