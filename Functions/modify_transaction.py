from Functions.read_from_db import read_from_db
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import boto3
import json

async def modify_transaction(update, context):
    message = update.message.text
    parts = message.split(maxsplit=4)
    try:
        transaction_number_0 = parts[1]
        transaction_number = parts[1]
        InOut = parts[2]
        Amount = parts[3]
        continueprocess = True
    except:        
        await update.message.reply_text(
            '• Please use the valid format!!!\n'
            '- Format: "/m <Number> <Category(i or e)> <amount> <reason>"\n'
            '- Example: "/m 5 e 700 Tv"'
        )
        continueprocess = False

    if continueprocess:

        if InOut == 'i' or InOut == 'I' :
            Category = 'Income'
        elif InOut == 'e' or InOut == 'E':
            Category = 'Expense'
        
        message = update.message.text

        user_id = str(update.message.from_user.id)
        [daily_records, monthly_records] = read_from_db(user_id)

        if int(transaction_number[0]) != 0:
            message_type = 'daily'
            transaction_number = int(transaction_number)-1
            records = daily_records
        elif int(transaction_number[0]) == 0:
            message_type = 'monthly'
            transaction_number = int(str(transaction_number)[1:])-1
            records = monthly_records
        
        if transaction_number > len(records):
            await update.message.reply_text(f"Transaction {transaction_number_0} not found.")
            return
        
        toModify = records[transaction_number]
        
        try:    
            Reason = parts[4]
            recordClient = boto3.client('lambda')
            inputParams = {
                "record_entry"   : Reason,
            }
            response = recordClient.invoke(
                FunctionName='arn:aws:lambda:us-east-1:533267242577:function:MoniMonitor_Openai',
                InvocationType='RequestResponse',
                Payload=json.dumps(inputParams)
            )
            response_payload = json.loads(response['Payload'].read())
            label = response_payload['body']
        except:
            Reason = ''
            label = ''


        if message_type == 'daily':
            temp_message_Date= f"• <b>Date:</b> {toModify['Timestamp'][2:10]} - {toModify['Timestamp'][11:]}\n"
        elif message_type == 'monthly':
            temp_message_Date = ''

        transaction_id_check = (
            f"{toModify['Transaction_Id'][0]}"
            f"{toModify['Transaction_Id'][8]}"
            f"{toModify['Transaction_Id'][13]}"
            f"{toModify['Transaction_Id'][18]}"
            f"{toModify['Transaction_Id'][23]}"
            f"{toModify['Transaction_Id'][28]}"
            f"{toModify['Transaction_Id'][33]}"
        )

        modify_data = f"Modify_it:{message_type}:{transaction_id_check}:{Category}:{Amount}:{Reason}:{transaction_number_0}:{label}"
        ignore_data = "Ignore_it"
 

        inline_keyboard = [
            [InlineKeyboardButton("Modify it", callback_data=modify_data)],
            [InlineKeyboardButton("Ignore", callback_data=ignore_data)]
        ]

        message = ('• <b>Do you want to Modify following?</b>\n\n')
        message += (
                'From:\n'
                f"#{transaction_number+1} • {toModify['Category']}\n"
                f'{temp_message_Date}'
                f"• <b>Amount:</b> {toModify['Amount']}\n"
                f"• <b>Reason:</b> {toModify['Reason']}\n\n"

                'To:\n'
                f"#{transaction_number+1} • {Category}\n"
                f'{temp_message_Date}'
                f"• <b>Amount:</b> {Amount}\n"
                f"• <b>Reason:</b> {Reason}\n\n"
            )


        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await update.message.reply_text(message, parse_mode='HTML',
                reply_markup=reply_markup)
