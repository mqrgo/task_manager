from dotenv import load_dotenv
from os import getenv
from pydantic import BaseModel

load_dotenv()

DB_USER = getenv('DB_USER')
DB_PASS = getenv('DB_PASS')
DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT')
DB_NAME = getenv('DB_NAME')
db_url = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


class AuthJWT(BaseModel):
    SECRET: str = getenv('SECRET')
    ALGORYTHM: str = getenv('ALGORYTHM')
    # expire: int = 15


auth_jwt = AuthJWT()

task_key = getenv('TASK_KEY').encode()
