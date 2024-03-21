from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from fastapi.requests import Request
import bcrypt
import jwt
from datetime import datetime
from src.config import auth_jwt, task_key


def hash_password(password: str) -> bytes:
    """
    making hash out of password
    :param password:
    :return: hashed_password
    """
    salt = bcrypt.gensalt()
    pwd = password.encode()
    return bcrypt.hashpw(pwd, salt)


def encode_task(task: str, key: bytes = task_key) -> bytes:
    fernet = Fernet(key)
    enc_task = fernet.encrypt(task.encode())
    return enc_task


def decode_task(encoded_task: bytes, key: bytes = task_key) -> str:
    fernet = Fernet(key)
    dec_task = fernet.decrypt(encoded_task)
    return dec_task.decode()


def convert_data(data: datetime) -> str:
    new_data = data.strftime("%H:%M %d-%m-%Y")
    return new_data


def check_password(password: str, hashed_password: bytes) -> bool:
    """
    checking if introduced password is correct
    :param hashed_password:
    :param user's password :
    :return:
    """
    return bcrypt.checkpw(password.encode(), hashed_password)


def create_jwt(data: dict, key=auth_jwt.SECRET, algorithm=auth_jwt.ALGORYTHM) -> str:
    to_encode = data.copy()
    to_encode.update({'iat': datetime.utcnow()})
    token = jwt.encode(to_encode, key, algorithm)
    # print(to_encode)
    # print(token, type(token))
    return token


def decode_jwt(token: str, key=auth_jwt.SECRET, algorithm=auth_jwt.ALGORYTHM):
    payload = jwt.decode(token, key=key, algorithms=algorithm)
    return payload
