async def new_transaction(update, context):
    await update.callback_query.message.reply_text(
        '----------\n'
        ' Send me a message with the format:\n\n'
        '• <b>Spending</b>(record your Spending):\n- Format:  "/e amount reason"\n-Example: <b>/e 50 Grocery</b>\n\n'
        '• <b>Income</b>(record your Income):\n- Format:  "/i amount reason"\n-Example: <b>/i 1500 Job Payment</b>\n'
        '----------\n',
        parse_mode='HTML'
    )
