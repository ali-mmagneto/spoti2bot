import logging
import os

from handlers import sender
from handlers.helpers import spotifydl
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater



logger = logging.getLogger(__name__)


def setup_logging():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
 
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="""
Spotify Download Bot 🙂
       
Uses:-  
• Can download any spotify song.
• Can download any spotify playlist-(slow)
• Premium song supported
• Free to use

• for more info use /help
""")
     
def help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="""
Uses\n
• SINGLE  - Type /spotify "Song url" or "song name"
• PLAYLIST- Type /spotify "Playlist url" (SLOW)""")
    
def error(update: Update, context: CallbackContext, error):
    logger.warning('Update "%s" caused error "%s"', update, error)
    

def main():
    TOKEN = os.environ.get('TOKEN')
    APP_NAME = os.environ.get('APP_NAME')

    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    # Set up the Updater

    updater = Updater(
        TOKEN,
        use_context=True,
    )
    dp = updater.dispatcher
    # Add handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_error_handler(error)

    dp.add_handler(
        CommandHandler(
            'spotify',
            sender.botify,
            pass_args=True,
            pass_job_queue=True,
            pass_chat_data=True
        )
    )
    dp.add_handler(
        CommandHandler(
            'spotifydl',
            sender.botify,
            pass_args=True,
            pass_job_queue=True,
            pass_chat_data=True
        )
    )    
    dp.add_handler(CommandHandler(
            'help',
            sender.botify,
            pass_args=True,
            pass_job_queue=True,
            pass_chat_data=True
        )
    )    

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
