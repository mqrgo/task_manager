from typing import Union
from fastapi import APIRouter, Request, Form, status, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from src.auth.crud import add_user_in_db, get_user_from_db, get_user_tasks_from_db, add_task_in_db, change_task_status, delete_task
from src.auth.utils import decode_jwt

router = APIRouter(prefix='', tags=['user'])
templates = Jinja2Templates(directory='src/templates')


def check_token(request: Request):
    try:
        token = request.cookies['session_token']
        payload = decode_jwt(token)
        return payload
    except Exception:
        return False


@router.get('/login')
def login(request: Request, payload: Union[bool, dict] = Depends(check_token)):
    if payload is False:
        return templates.TemplateResponse('login.html', {'request': request})
    else:
        return RedirectResponse(url='user', status_code=status.HTTP_302_FOUND)


@router.post('/try-login')
def try_login(username=Form(), password=Form()):
    try:
        token = get_user_from_db(username=username, password=password)
        response = RedirectResponse(url='user', status_code=status.HTTP_302_FOUND)
        response.set_cookie(key='session_token', value=token, httponly=True)
        return response
    except HTTPException:
        return RedirectResponse(url='login', status_code=status.HTTP_301_MOVED_PERMANENTLY)




@router.get('/signup')
def signup(request: Request, payload: Union[bool, dict] = Depends(check_token)):
    if payload is False:
        return templates.TemplateResponse('signup.html', {'request': request})
    else:
        return RedirectResponse(url='user', status_code=status.HTTP_302_FOUND)


@router.post('/try-signup')
def try_signup(username=Form(), password=Form(), email=Form()):
    res = add_user_in_db(username, password, email)
    if res is True:
        return RedirectResponse(url='login', status_code=status.HTTP_301_MOVED_PERMANENTLY)
    else:
        return RedirectResponse(url='signup', status_code=status.HTTP_301_MOVED_PERMANENTLY)


@router.get('/user')
def user(request: Request, payload: Union[bool, dict] = Depends(check_token)):
    """
    The main page. Returns all user tasks. Trying to get user's tasks from db and redirect them on jinja html template
    """
    context = payload
    if context is False:
        return RedirectResponse(url='login', status_code=status.HTTP_301_MOVED_PERMANENTLY)
    else:
        res = get_user_tasks_from_db(context)
        DONE_TASKS = res[1]
        UNDONE_TASKS = res[0]
        return templates.TemplateResponse(
            'user_data.html',
            {
                'request': request,
                'context': context,
                'undone_tasks': UNDONE_TASKS,
                'done_tasks': DONE_TASKS,
            }
        )


@router.post('/add_task')
def add_task(new_task=Form(), payload: Union[bool, dict] = Depends(check_token)):
    """
     Adding new task on dashboard and reloading the page
    """
    if payload is False:
        return RedirectResponse(url='login', status_code=status.HTTP_301_MOVED_PERMANENTLY)
    else:
        try:
            add_task_in_db(task=new_task, payload=payload)
        except Exception as exp:
            return exp.args
        finally:
            return RedirectResponse(url='user', status_code=status.HTTP_302_FOUND)


@router.post('/task_done')
def task_done(task_id=Form(), payload: Union[bool, dict] = Depends(check_token)):
    """
    With press 'done' button updating task's status from False to True and reloading the page
    """
    if payload is False:
        return RedirectResponse(url='login', status_code=status.HTTP_301_MOVED_PERMANENTLY)
    else:
        try:
            task_id = int(task_id)
            if not change_task_status(task_id=task_id):
                raise ValueError
        except ValueError:
            print('not int')
        finally:
            return RedirectResponse(url='user', status_code=status.HTTP_302_FOUND)


@router.get('/user_info')
def user_info(request: Request, payload: Union[bool, dict] = Depends(check_token)):
    if payload is False:
        return RedirectResponse(url='login', status_code=status.HTTP_301_MOVED_PERMANENTLY)
    return templates.TemplateResponse('user_info.html', {'request': request, 'payload': payload})


@router.post('/task_delete')
def task_delete(task_id=Form(), payload: Union[bool, dict] = Depends(check_token)):
    if payload is False:
        return RedirectResponse(url='login', status_code=status.HTTP_301_MOVED_PERMANENTLY)
    else:
        if delete_task(task_id=task_id):
            return RedirectResponse(url='user', status_code=status.HTTP_302_FOUND)


@router.post('/logout')
def logout():
    """destroy user's cookie and redirect on 'login' page"""
    response = RedirectResponse(url='login', status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie('session_token')
    return response

