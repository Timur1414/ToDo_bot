import datetime
import logging
from typing import List, Type, Optional
from sqlalchemy import Integer, Column, String, Boolean, DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase): pass

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    done = Column(Boolean, default=False)
    start_time = Column(DateTime, default=datetime.datetime.now)
    end_time = Column(DateTime, nullable=True, default=None)

    def open(self):
        update_task(self.id, done=False)
        logging.info(f'task {self.id} opened.')

    def close(self):
        update_task(self.id, done=True)
        logging.info(f'task {self.id} closed.')

    def __str__(self):
        return f'{self.id} - {self.title}'

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    telegram_id = Column(Integer)
    chat_id = Column(Integer)

engine = create_engine('sqlite:///db.sqlite3')
Base.metadata.create_all(engine)

def create_user(username: str, first_name: str, last_name: str, telegram_id: int, chat_id: int):
    with Session(autoflush=False, bind=engine) as db:
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            telegram_id=telegram_id,
            chat_id=chat_id
        )
        db.add(user)
        db.commit()
        logging.info('user created.')

def is_user_in_db(username: str) -> bool:
    with Session(autoflush=False, bind=engine) as db:
        logging.info(f'check user {username} in db.')
        return db.query(User).filter(User.username == username).count() > 0

def get_user(username: str) -> Optional[Type[User]]:
    with Session(autoflush=False, bind=engine) as db:
        logging.info(f'get user {username}.')
        return db.query(User).filter(User.username == username).first()

def create_task(title: str, description: str, start_time: datetime.datetime = None, end_time: datetime.datetime = None):
    with Session(autoflush=False, bind=engine) as db:
        task = Task(
            title=title,
            description=description,
            start_time=datetime.datetime.now() if start_time is None else start_time,
            end_time=end_time
        )
        db.add(task)
        db.commit()
        logging.info('task created.')

def get_all_tasks() -> List[Type[Task]]:
    with Session(autoflush=False, bind=engine) as db:
        logging.info('get all tasks.')
        return db.query(Task).all()

def get_all_open_tasks() -> List[Type[Task]]:
    with Session(autoflush=False, bind=engine) as db:
        logging.info('get all open tasks.')
        return db.query(Task).filter(Task.done == False).all()

def get_task(id: int) -> Optional[Type[Task]]:
    with Session(autoflush=False, bind=engine) as db:
        logging.info(f'get task {id}.')
        return db.get(Task, id)

def update_task(id: int, title: str = None, description: str = None, done: bool = None, start_time: datetime.datetime = None, end_time: datetime.datetime = None):
    with Session(autoflush=False, bind=engine) as db:
        task = db.get(Task, id)
        if task:
            task.title = title if title is not None else task.title
            task.description = description if description is not None else task.description
            task.done = done if done is not None else task.done
            task.start_time = start_time if start_time is not None else task.start_time
            task.end_time = end_time if end_time is not None else task.end_time
            db.commit()
            logging.info(f'task {id} updated.')
        else:
            logging.warning(f'task {id} not found.')

def delete_task(id: int):
    with Session(autoflush=False, bind=engine) as db:
        task = db.get(Task, id)
        if task:
            db.delete(task)
            db.commit()
            logging.info(f'task {id} deleted.')
        else:
            logging.warning(f'task {id} not found.')
