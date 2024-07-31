async def monthly_Instructions(update, context) -> None:
    await update.message.reply_text(
        '----------\n'
        ' How to Monitor <b>Monthly</b> Transactions:\n\n'
        '• <b>Spending</b> (record <b>Monthly</b> Spending):\n- Format:  "/me amount reason"\n-Example: <b>/me 200 Phone Bill</b>\n\n'
        '• <b>Income</b> (record <b>Monthly</b> Income):\n- Format:  "/mi amount reason"\n-Example: <b>/mi 1500 Job Payment</b>\n'
        '----------\n',
        parse_mode='HTML'
    )