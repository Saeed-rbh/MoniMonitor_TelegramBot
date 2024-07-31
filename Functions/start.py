async def start(update, context) -> None:
    await update.message.reply_text(
        '----------\n'
        'Hi! I am your money monitor bot.'
        ' Send me a message with the format:\n\n'
        '• <b>Spending</b>(record your Spending):\n- Format:  "/s amount reason"\n-Example: <b>/s 50 Grocery</b>\n\n'
        '• <b>Income</b>(record your Income):\n- Format:  "/i amount reason"\n-Example: <b>/i 1500 Job Payment</b>\n'
        '----------\n',
        parse_mode='HTML')