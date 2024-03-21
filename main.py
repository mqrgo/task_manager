from contextlib import asynccontextmanager

from fastapi import FastAPI, Response, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from src.auth.router import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('START APP')
    yield
    print('STOP APP')


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
templates = Jinja2Templates(directory='src/templates')
app.mount('/static', StaticFiles(directory='src/static'), name='static')



@app.get('/')
def root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


