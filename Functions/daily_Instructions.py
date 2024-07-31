async def daily_Instructions(update, context) -> None:
    await update.message.reply_text(
        '----------\n'
        ' How to Monitor <b>Daily</b> Transactions:\n\n'
        '• <b>Spending</b> (record <b>Daily</b> Spending):\n- Format:  "/e amount reason"\n-Example: <b>/e 50 Grocery</b>\n\n'
        '• <b>Income</b>(record <b>Daily</b> Income):\n- Format:  "/i amount reason"\n-Example: <b>/i 1500 Stock Intrest</b>\n'
        '----------\n',
        parse_mode='HTML'
    )