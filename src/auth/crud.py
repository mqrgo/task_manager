from fastapi import HTTPException
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from starlette import status
from src.config import db_url
from src.models import User, Task
from src.auth.shemas import UserData
from src.auth.utils import hash_password, check_password, create_jwt, decode_task, convert_data, encode_task
from src.user.schemas import UserTask

engine = create_engine(url=db_url)  # creating engine object
Session = sessionmaker(bind=engine)  # creating tool that can create new session with db


def add_user_in_db(username: str, password: str, email: str):
    """
    Add new user in db. If no email return exc.
    The application connects to the database and checks whether a user with that name exists.
    User data is validated using with pydantic scheme.
    The password hash is created
    If all is well, the new user is added to the database.
    """
    if email is None:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='no email')
    with Session() as session:
        for item in session.query(User).all():
            if item.username == username:
                return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='login already exist')
    try:
        new_user = UserData(username=username, password=password, email=email)
    except Exception as exp:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=exp.args)
    else:
        new_pass = hash_password(password)
        new_user = User(username=new_user.username, password=new_pass, email=new_user.email)
        with Session() as session:
            session.add(new_user)
            session.commit()
    return True


def get_user_from_db(username: str, password: str):
    """
    An exception is initialized.
    Trying to get user from db, if there's no such user return exc. If user exist, check password.
    If all is well, a token is created and returned.
    """
    exc = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='incorrect username or password')
    with Session() as session:
        res = session.query(User.id, User.username, User.password, User.email).filter(User.username == username).all()
    if len(res) == 0:
        raise exc
    res = res[0]
    if check_password(password, res.password):
        payload = {'id': res.id, 'username': res.username, 'email': res.email}
        token = create_jwt(payload)
        return token
    else:
        raise exc


def get_user_tasks_from_db(payload: dict):
    """
    The method accepts an ID from the payload, connects to the database and requests the user’s tasks using his ID.
    Next, all tasks are filtered into completed and uncompleted and decrypted.
    """
    id = int(payload['id'])
    try:
        with Session() as session:
            res = session.query(
                Task.id,
                Task.topic,
                Task.date,
                Task.is_done
            ).filter(
                Task.user_id == id,
            ).order_by(
                desc(
                    Task.id
                )
            ).all()
        done_data = []
        undone_data = []
        for item in res:
            if item.is_done is True:
                done_data.append(
                    {
                        'id': item.id,
                        'topic': decode_task(item.topic),
                        'is_done': item.is_done,
                        'date': convert_data(item.date)
                    }
                )
            else:
                undone_data.append(
                    {
                        'id': item.id,
                        'topic': decode_task(item.topic),
                        'is_done': item.is_done,
                        'date': convert_data(item.date)
                    }
                )

        return undone_data, done_data
    except Exception as exp:
        return exp.args


def add_task_in_db(task: str, payload: dict):
    """
    Method accepts the task and payload.
    The task is encrypted, validated using the pydantic scheme and transferred to the database.
    """
    try:
        task = encode_task(task)
        id = int(payload['id'])
        db_task = UserTask(topic=task, user_id=id)
        db_task = Task(**db_task.dict())
        with Session() as session:
            session.add(db_task)
            session.commit()
            return True
    except Exception as exp:
        return False


def change_task_status(task_id: int):
    """
    The method accepts a task ID and a payload. Next, the task state changes from False to True
    """
    try:
        with Session() as session:
            res = session.query(Task).get(task_id)
            res.is_done = True
            session.add(res)
            session.commit()
            return True
    except Exception as exp:
        return False


def delete_task(task_id: int):
    """
    The method accepts a task ID and a payload. Next, the task state changes from False to True
    """
    try:
        with Session() as session:
            res = session.query(Task).get(task_id)
            session.delete(res)
            session.commit()
            return True
    except Exception as exp:
        return False