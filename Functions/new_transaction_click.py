async def new_transaction_click(update, context):
    """Handler function for when the "New Transaction" button is clicked."""
    query = update.callback_query
    await query.answer()
    
    await query.message.reply_text(
        'Instructions for recording a new transaction:\n\n'
        '• <b>Spending</b> (record your Spending):\n- Format: "/e amount reason"\n- Example: <b>/e 50 Grocery</b>\n\n'
        '• <b>Income</b> (record your Income):\n- Format: "/i amount reason"\n- Example: <b>/i 1500 Job Payment</b>\n',
        parse_mode='HTML'
    )