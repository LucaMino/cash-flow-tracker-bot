import os
import helper
from MyOpenAI import MyOpenAI
from GoogleSheetService import GoogleSheetService
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# load .env
load_dotenv()

# retrieve telegram bot token
TOKEN = os.getenv('TELEGRAM_TOKEN')

# start function
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Ciao! Dimmi le spese di oggi o di qualunque giorno e traccierò tutto!')

# handle message function
async def handle_message(update: Update, context: CallbackContext) -> None:
    # retrieve message
    message = update.message.text

    await update.message.reply_text(f'Sto parlando con OpenAI...')

    # translate to json using openai
    openai = MyOpenAI()
    openai_response = openai.get_response(message)

    if openai_response is None:
        await update.message.reply_text(f'Ops! Non riesco a capire bene!')
    else:
        print('openai_response: ' + openai_response)

        await update.message.reply_text(f'Sto salvando...')

        try:
            # retrieve clean transactions structure
            transactions = helper.sanitize_response(openai_response)

            if not isinstance(transactions, list):
                raise TypeError("Decoded content is not a list")

            # create new GoogleSheetService
            g_sheet_service = GoogleSheetService()

            # loop transactions
            for transaction in transactions:
                # save on google sheets
                g_sheet_service.add_transaction(transaction)

            await update.message.reply_text(f'Salvato con successo')

        except Exception as e:
            await update.message.reply_text(f'Ops! Non riesco a salvare su google sheet!')

def main():
    # build application
    application = Application.builder().token(TOKEN).build()

    # set start() -> /start
    application.add_handler(CommandHandler('start', start))

    # create handler for all messages (not start with /)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # run bot
    application.run_polling()

if __name__ == '__main__':
    main()