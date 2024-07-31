import json
import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from Functions.start import start
from Functions.monthly_Instructions import monthly_Instructions
from Functions.record import record_daily_Spending
from Functions.record import record_daily_Income
from Functions.record import record_monthly_Spending
from Functions.record import record_monthly_Income
from Functions.history import history
from Functions.clear_history import clear_history
from Functions.delete_transaction import delete_transaction
from Functions.modify_transaction import modify_transaction
from Functions.new_transaction import new_transaction

from Functions.record_button_click import record_button_click

# from Functions.user_password import user_password

# from Functions.send_files import send_files
# from Functions.analyze import analyze
# from Functions.user_password import user_password

# Initialize the bot with the token from environment variables
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')

async def process_update(update: dict, application):
    # Convert the update dictionary to an Update object and process it
    update_obj = Update.de_json(update, application.bot)
    await application.process_update(update_obj)

async def handle_event(event):
    # Create the Application instance
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("new", new_transaction))
    app.add_handler(CommandHandler("i", record_daily_Income))
    app.add_handler(CommandHandler("mi", record_monthly_Income))

    app.add_handler(CommandHandler("monthly", monthly_Instructions))
    app.add_handler(CommandHandler("history", history))
    app.add_handler(CommandHandler("clear", clear_history))
    app.add_handler(CommandHandler("s", record_daily_Spending))
    
    app.add_handler(CommandHandler("ms", record_monthly_Spending))
    
    app.add_handler(CommandHandler("d", delete_transaction))
    app.add_handler(CommandHandler("m", modify_transaction))
    
    app.add_handler(CallbackQueryHandler(record_button_click))

    # app.add_handler(CommandHandler("access", user_password))

    # app.add_handler(CommandHandler("analyze", analyze))
    
    # app.add_handler(CommandHandler("files", send_files))


    async with app:
        # Parse the incoming request body
        body = json.loads(event.get('body', '{}'))
        
        # Process the update from Telegram
        await process_update(body, app)
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Update processed successfully"})
        }

def lambda_handler(event, context):
    
    try:
        # Process the event asynchronously
        response = asyncio.run(handle_event(event))
        
        return response
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
