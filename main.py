from ast import Str
from curses import use_default_colors
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import os
from urllib.parse import urlparse
import sys


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Send download link to me, I'll send it back to you :)")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    response = requests.post("https://dl.linknim.ir/file.php",
                             data={'url': url}, stream=True, timeout=10000000)
    total_length = response.headers.get('content-length')
    dl = 0
    total_length = int(total_length)
    file = open('temp', 'wb+')
    current = 0
    message = await context.bot.send_message(chat_id=update.effective_chat.id, text=str(current))
    for data in response.iter_content(chunk_size=4096):
        dl += len(data)
        file.write(data)
        if ((dl / total_length * 100) - current > 0.01):
            current = dl / total_length * 100
            await context.bot.edit_message_text(
                message_id=message.id, chat_id=update.effective_chat.id, text=str(current))
    a = urlparse(url)
    file.close()
    file = open('temp', 'rb')
    await context.bot.send_document(chat_id=update.effective_chat.id, document=file.read(), filename=os.path.basename(a.path))

if __name__ == '__main__':
    application = ApplicationBuilder().token(
        os.environ['TOKEN']).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    application.run_polling()
