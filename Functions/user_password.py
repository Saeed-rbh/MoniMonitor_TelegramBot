import json
import boto3
from random import choice, shuffle
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


async def user_password(update, context):
    user_id = str(update.message.from_user.id)

    inputParams = {
            'status': 'passcode',
            "user_id"   : user_id,
        }
    recordClient = boto3.client('lambda')
    response = recordClient.invoke(
        FunctionName='arn:aws:lambda:us-east-1:533267242577:function:MoniMonitor_ToDB',
        InvocationType='RequestResponse',
        Payload=json.dumps(inputParams)
    )
    response_payload = json.loads(response['Payload'].read())
    passcode = response_payload['body']

    inline_keyboard = [
        [InlineKeyboardButton("Hide", callback_data="Hide_it")]
    ]
    message = f'• <b>username</b>: {user_id}\n• <b>password</b>: {passcode}'
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    await update.message.reply_text(message, parse_mode='HTML', reply_markup=reply_markup)
