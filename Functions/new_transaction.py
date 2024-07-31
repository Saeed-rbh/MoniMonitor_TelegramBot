async def new_transaction(update, context):
    await update.message.reply_text(
        "To record your transactions, please use the following formats:\n\n"
        "• <b>Income</b> (to record income):\n"
        "  - Format: /i amount reason\n"
        "  - Example: <b>/i 1500 Job Payment</b>\n\n"
        "• <b>Expenses</b> (to record expenses):\n"
        "  - Format: /e amount reason\n"
        "  - Example: <b>/e 50 Grocery</b>\n\n"
        "• <b>Save & Invest</b> (to record savings or investments):\n"
        "  - Format: /s amount reason\n"
        "  - Example: <b>/s 50 Stock</b>\n\n"
        "Send me a message using these formats to track your finances.\n",
        parse_mode='HTML')