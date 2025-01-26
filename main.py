import os
import telebot
from dotenv import load_dotenv
import logging
from telebot import types
from models import create_task, get_task, get_all_tasks, update_task, get_all_open_tasks


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
        keyboard = types.InlineKeyboardMarkup()
        key_list = types.InlineKeyboardButton(text='/list', callback_data='list')
        keyboard.add(key_list)
        key_done = types.InlineKeyboardButton(text='/done <id задачи>', callback_data='done')
        keyboard.add(key_done)
        key_open = types.InlineKeyboardButton(text='/open <id задачи>', callback_data='open')
        keyboard.add(key_open)
        key_task = types.InlineKeyboardButton(text='/task <id задачи>', callback_data='task')
        keyboard.add(key_task)
        key_create = types.InlineKeyboardButton(text='/create', callback_data='create')
        keyboard.add(key_create)
        bot.send_message(message.chat.id, 'Привет, ты написал мне /start\nСписок команд:', reply_markup=keyboard)

    @bot.message_handler(commands=['list'])
    def list_tasks(message):
        logging.info('Received /list command.')
        tasks = get_all_open_tasks()
        bot.send_message(message.chat.id, f'Список задач ({len(tasks)}):')
        for task in tasks:
            bot.send_message(message.chat.id, task)

    @bot.message_handler(commands=['done'])
    def done_task(message):
        logging.info('Received /done command.')
        cmd = message.text.split()
        if len(cmd) == 1:
            bot.send_message(message.chat.id, 'Введите /done <id задачи>')
            logging.warning('No task id provided.')
        else:
            try:
                task_id = int(cmd[1])
                if task_id <= 0:
                    raise ValueError
                task = get_task(task_id)
                task.close()
                bot.send_message(message.chat.id, f'Задача {task_id} закрыта.')
                logging.info(f'Task {task_id} closed.')
            except (ValueError, AttributeError):
                bot.send_message(message.chat.id, 'Некорректный id задачи.')
                logging.warning('Incorrect task id.')

    @bot.message_handler(commands=['open'])
    def open_task(message):
        logging.info('Received /open command.')
        cmd = message.text.split()
        if len(cmd) == 1:
            bot.send_message(message.chat.id, 'Введите /open <id задачи>')
            logging.warning('No task id provided.')
        else:
            try:
                task_id = int(cmd[1])
                if task_id <= 0:
                    raise ValueError
                task = get_task(task_id)
                task.open()
                bot.send_message(message.chat.id, f'Задача {task_id} открыта.')
                logging.info(f'Task {task_id} opened.')
            except (ValueError, AttributeError):
                bot.send_message(message.chat.id, 'Некорректный id задачи.')
                logging.warning('Incorrect task id.')

    @bot.message_handler(commands=['task'])
    def task(message):
        logging.info('Received /task command.')
        cmd = message.text.split()
        if len(cmd) == 1:
            bot.send_message(message.chat.id, 'Введите /task <id задачи>')
            logging.warning('No task id provided.')
        else:
            try:
                task_id = int(cmd[1])
                if task_id <= 0:
                    raise ValueError
                task = get_task(task_id)
                bot.send_message(message.chat.id, task)
                bot.send_message(message.chat.id,f'Description: {task.description}\nDone: {task.done}\nStart time: {task.start_time}\nEnd time: {task.end_time}')
                logging.info(f'Task {task_id} sent.')
            except (ValueError, AttributeError):
                bot.send_message(message.chat.id, 'Некорректный id задачи.')
                logging.warning('Incorrect task id.')

    @bot.message_handler(commands=['create'])
    def create(message):
        logging.info('Received /create command.')
        cmd = message.text.split()
        if len(cmd) == 1:
            bot.send_message(message.chat.id, 'Введите /create <title> <description> [<start_time>] [<end_time>]')
            logging.warning('No task data provided.')
        else:
            try:
                title = cmd[1]
                description = cmd[2]
                start_time = None if len(cmd) < 4 else cmd[3]
                end_time = None if len(cmd) < 5 else cmd[4]
                create_task(title, description, start_time, end_time)
                bot.send_message(message.chat.id, 'Задача создана.')
                logging.info('Task created.')
            except Exception as e:
                bot.send_message(message.chat.id, 'Некорректные данные задачи.')
                logging.warning(f'Incorrect task data: {e}')

    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call):
        if call.data == 'list':
            list_tasks(call.message)
        elif call.data == 'done':
            done_task(call.message)
        elif call.data == 'open':
            open_task(call.message)
        elif call.data == 'task':
            task(call.message)
        elif call.data == 'create':
            create(call.message)

    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
