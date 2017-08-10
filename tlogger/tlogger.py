from logging import Handler

from telegram.ext import Updater


class TelegramHalder(Handler):
    pass


from configparser import ConfigParser

if __name__ == '__main__':
    config = ConfigParser()
    config.read("token.ini")
    updater = Updater(token=config["DEFAULT"]["bot_token"])
    bot = updater.bot
    chat_id = bot.get_updates()[-1].message.chat_id
    bot.send_message(chat_id=chat_id, text="kek?")
