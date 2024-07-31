async def start(update, context) -> None:
    await update.message.reply_text(
        "Hello! I’m your MoniMonitor Bot.\n\n"
        "To record your transactions, use the following formats:\n\n"
        "• <b>Income</b>:\n"
        "- <b>Daily</b>: /i amount reason\n"
        "  <i> E.g.   </i> <b>/i 1500 Job Job Bonus</b>\n"
        "- <b>Monthly</b>: /mi amount reason\n"
        "  <i> E.g.         </i> <b>/mi 1500 Salary</b>\n\n"
        "• <b>Expenses</b>:\n"
        "- <b>Daily</b>: /e amount reason\n"
        "  <i> E.g.   </i> <b>/e 50 Grocery</b>\n"
        "- <b>Monthly</b>: /me amount reason\n"
        "  <i> E.g.         </i> <b>/me 50 Subscription</b>\n\n"
        "• <b>Save & Invest</b>:\n"
        "- <b>Daily</b>: /s amount reason\n"
        "  <i> E.g.   </i> <b>/s 50 Stock</b>\n"
        "- <b>Monthly</b>: /ms amount reason\n"
        "  <i> E.g.         </i> <b>/ms 50 Retirement Fund</b>\n\n"
        "Send a message using these formats to track your finances.\n",
        parse_mode='HTML'
    )
