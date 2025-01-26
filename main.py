import os
import telebot
from dotenv import load_dotenv
import logging

from models import create_task, get_task, get_all_tasks, update_task


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s [%(levelname)s]: %(message)s',
        handlers=[logging.FileHandler('bot.log', 'w', 'utf-8')]
    )
    load_dotenv()
    token = os.environ.get('TELEGRAM_TOKEN')
    logging.info('Loaded api key.')
    bot = telebot.TeleBot(token)
    logging.info('Bot started.')



    @bot.message_handler(commands=['start'])
    def start_message(message):
        logging.info('Received /start command.')
        tasks = get_all_tasks()
        bot.send_message(message.chat.id, 'Привет, ты написал мне /start\nСписок задач:')
        for task in tasks:
            bot.send_message(message.chat.id, task.title)

    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
