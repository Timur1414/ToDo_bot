import os
import telebot
from dotenv import load_dotenv
import logging


def main():
    load_dotenv()
    token = os.environ.get('TELEGRAM_TOKEN')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s [%(levelname)s]: %(message)s',
        handlers=[logging.FileHandler('bot.log', 'w', 'utf-8')]
    )
    bot = telebot.TeleBot(token)
    logging.info('Bot started')

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
