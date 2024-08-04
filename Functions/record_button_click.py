import os
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from Functions.record_to_db import record_to_db
from Functions.backup_database import backup_database
from Functions.delete_item import delete_item
from Functions.get_item import get_item
from Functions.update_item import update_item
from Functions.read_from_db import read_from_db

async def record_button_click(update, context):
    query =  update.callback_query
    await query.answer()

    data = query.data.split(':')
    action = data[0]

    user_id = str(update.callback_query.from_user.id)
    user_data_dir = os.path.join('user_data', user_id)

    if action == "add_to_daily_wallet":
        category = data[1]
        amount = float(data[2])
        reason = data[3]      

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        printabletimestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M').strftime('%H:%M - %d/%m/%Y')

        record_entry = {'Timestamp': timestamp,
                        'Category': category.replace(" ", ""), 'Amount': amount, 'Reason': reason, 'Label': ''}

        user_id = str(update.callback_query.from_user.id)
        record_type = "daily"


        message = await query.message.reply_text(
            '• Please wait...\n',
            parse_mode='HTML'
        )
        
        record_to_db(record_entry,user_id,record_type)
        
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message.message_id)

        inline_keyboard = [
            [InlineKeyboardButton("New Transaction", callback_data="new_transaction")]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)

        await query.message.reply_text(
            '----------\n'
            f'  Successfully added to <b>Daily</b> Wallet:\n\n• New <b>Daily {category}</b>\n• Amount: $<b>{amount:.2f}</b>\n• Reason: <b>{reason}</b>\n• Time: <b>{printabletimestamp}</b>\n'
            '----------\n',
            parse_mode='HTML',
            reply_markup=reply_markup
        )
        await query.message.delete()

    elif action == "add_to_monthly_wallet":
            category = data[1]
            amount = float(data[2])
            reason = data[3]

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

            record_entry = {'Timestamp': timestamp,
                        'Category': category.replace(" ", ""), 'Amount': amount, 'Reason': reason, 'Label': ''}

            user_id = str(update.callback_query.from_user.id)
            record_type = "monthly"
            
            message = await query.message.reply_text(
                '• Please wait...\n',
                parse_mode='HTML'
            )
            
            record_to_db(record_entry,user_id,record_type)
            
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message.message_id)

            inline_keyboard = [
                [InlineKeyboardButton("New Transaction", callback_data="new_transaction")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard)

            await query.message.reply_text(
                '----------\n'
                f'  Successfully added to <b>Monthly</b> Wallet:\n\n• New <b>Monthly {category}</b>\n• Amount: $<b>{amount:.2f}</b>\n• Reason: <b>{reason}</b>\n'
                '----------\n',
                parse_mode='HTML',
                reply_markup=reply_markup
            )
            await query.message.delete()        

    elif action == "modify":
        await query.message.delete()
        await query.message.reply_text(
                'To record new transactions, use the following formats:\n\n'
                '• <b>Spending</b> (record your spending):\n'
                '- Format: /e amount reason\n'
                '- Example: <b>/e 50 Grocery</b>\n\n'
                '• <b>Income</b> (record your income):\n'
                '- Format: /i amount reason\n'
                '- Example: <b>/i 1500 Job Payment</b>\n',
                parse_mode='HTML')
        
    elif action == "new_transaction":
        await query.message.reply_text(
                'To record new transactions, use the following formats:\n\n'
                '• <b>Spending</b> (record your spending):\n'
                '- Format: /e amount reason\n'
                '- Example: <b>/e 50 Grocery</b>\n\n'
                '• <b>Income</b> (record your income):\n'
                '- Format: /i amount reason\n'
                '- Example: <b>/i 1500 Job Payment</b>\n',
                parse_mode='HTML')
        
    elif action == "Delete_transaction":
        message = ('----------\n'
                   '<b>Deleting Instraction</b>:\n\n'
                   '- Format:  /d Number\n-Example: <b>/d 4</b>\n'
                   '----------\n')
        await query.message.reply_text(message, parse_mode='HTML')

    elif action == "Ignore_it":
        temporary_filename = 'Temporary.csv'
        temp_file = os.path.join(user_data_dir, temporary_filename)
        os.remove(temp_file)
        await query.message.delete()
    
    elif action == "Hide_it":
        await query.message.delete()

    elif action == "Delete_it":
        type = data[1]
        record_id = data[2]
        TransactionNumber = data[3]

        message = await query.message.reply_text(
            '• Please wait...\n',
            parse_mode='HTML'
        )
        
        temporary_records=get_item(user_id, record_id)
        delete_item(user_id, record_id)
        
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message.message_id)
        
        await query.message.delete()
        if type == 'Daily':
            message = (
                '----------\n'
                '<b>Successfully Deleted Transaction</b>:\n\n'
                f"• <b>{type}</b> Transaction:\n"
                f"• #{TransactionNumber} • {temporary_records['Category']}\n"
                f"• <b>Date:</b> {temporary_records['Timestamp'][2:10]} - {temporary_records['Timestamp'][11:]}\n"
                f"• <b>Amount:</b> {temporary_records['Amount']}\n"
                f"• <b>Reason:</b> {temporary_records['Reason']}\n"
                '----------\n'
            )
        elif type == 'Monthly':
            message = (
                '----------\n'
                '<b>Successfully Deleted Transaction</b>:\n\n'
                f"• <b>{type}</b> Transaction:\n"
                f"• #0{TransactionNumber} • {temporary_records['Category']}\n"
                f"• <b>Amount:</b> {temporary_records['Amount']}\n"
                f"• <b>Reason:</b> {temporary_records['Reason']}\n"
                '----------\n'
            )

        await query.message.reply_text(message, parse_mode='HTML')

    elif action == "Modify_transaction":
        message = ('----------\n'
                   '• <b>Modify Instraction</b>:\n\n'
                   '- Format:  /m Number Category(i or e) amount reason\n-Example: <b>/m 3 e 50 Grocery</b>\n'
                   '----------\n')
        await query.message.reply_text(message, parse_mode='HTML')

    elif action == "Modify_it":
        
        type = data[1]
        transactionid = data[2]
        Category = data[3]
        Amount = data[4]
        Reason = data[5]
        transaction_number = data[6]
        index = data[7]

        message = await query.message.reply_text(
            '• Please wait...\n',
            parse_mode='HTML'
        )

        [daily_records, monthly_records] = read_from_db(user_id)

        if int(transaction_number[0]) != 0:
            transaction_number = int(transaction_number)-1
            records = daily_records
        elif int(transaction_number[0]) == 0:
            transaction_number = int(str(transaction_number)[1:])-1
            records = monthly_records
              
        toModify = records[transaction_number]
        transactionid_check = f'{toModify["Transaction_Id"][0]}{toModify["Transaction_Id"][8]}{toModify["Transaction_Id"][13]}{toModify["Transaction_Id"][18]}{toModify["Transaction_Id"][23]}{toModify["Transaction_Id"][28]}{toModify["Transaction_Id"][33]}'
        if transactionid_check == transactionid:
            pass
        else:
            await query.message.reply_text(f"Transaction {transaction_number+1} not found.")
            return

        expense_categories = [
            "Housing & Utilities",
            "Transportation",
            "Groceries & Dining",
            "Medical & Health",
            "Education & Training",
            "Leisure & Recreation"
            "Other"
        ]

        Income_categories = [
            "Employment Income", 
            "Employee Benefits", 
            "Government Benefits",
            "Investment Income" 
            "Other"
        ]

        SaveInvest_categories = [
            "Savings Account", 
            "Stocks", 
            "Cryptocurrency",
            "Real Estate" 
            "Other"
        ]
        
        if Category == 'income' :
            categories = Income_categories
        elif Category == 'Expense':
            categories = expense_categories
        elif Category == 'Save & Invest':
            categories = SaveInvest_categories

        Label = categories[index] if index != '' else toModify['Label'],

        updateToDB = {
            "Timestamp": toModify['Timestamp'],
            "Category": Category,
            "Amount": Amount,
            "Reason": Reason if Reason != '' else toModify['Reason'],
            "Type": type,
            "Label": Label,
        }
        

        update_item(user_id, toModify['Transaction_Id'],updateToDB)

        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message.message_id)
        
        await query.message.delete()
        if type == 'daily':
            message_date = f"• <b>Date:</b> {updateToDB['Timestamp'][2:10]} - {updateToDB['Timestamp'][11:]}\n"
        elif type == 'monthly':
            message_date = ''
        message = (
            '----------\n'
            f'<b>Modified <b>{type}</b> Transaction</b>:\n\n'
            f"• {updateToDB['Category']}\n"
            f"{message_date}"
            f"• <b>Amount:</b> {updateToDB['Amount']}\n"
            f"• <b>Reason:</b> {updateToDB['Reason']}\n"
            '----------\n'
        )  
        await query.message.reply_text(message, parse_mode='HTML')
    
    elif action == "Clear_History":

        user_id = data[1]

        message = await query.message.reply_text(
            '• Please wait...\n',
            parse_mode='HTML'
        )
        
        backup_database(user_id)
        
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message.message_id)

        await query.message.delete()
        inline_keyboard = [
            [InlineKeyboardButton("New Trasaction", callback_data=f"new_transaction")],
        ]
        message = ('----------\n'
                '• <b>Your History successfully Cleared</b>\n'
                '----------\n')
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await query.message.reply_text(message, parse_mode='HTML',
                reply_markup=reply_markup)
