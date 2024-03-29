import uvicorn

from os import listdir
from esse_gradio import *
from admin_gradio import *
from gradio import mount_gradio_app
from datetime import timedelta

from fastapi import HTTPException
from fastapi import Request, Form
from starlette.middleware.sessions import SessionMiddleware

from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, status
import jwt

from models import Token

templates = Jinja2Templates(directory="templates/html")

_SECRET = "Jn30u3qGv3k436lwd"

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=_SECRET, max_age=None)

@app.get('/signup')
async def signup_page(request : Request):
    return templates.TemplateResponse(
            name='signup.html',
            context={
                'request': request,
                'error' : ''
            }
        )

@app.get('/signin')
async def singin_page(request : Request):
    return templates.TemplateResponse(
            name='signin.html',
            context={
                'request': request,
                'error' : ''
            }
        )
'''
@app.get('/signup')
async def signup_page(request : Request):
    return templates.TemplateResponse(
            name='signup.html',
            context={
                'request': request,
                'error' : ''
            }
        )
'''

@app.get('/')
async def login_page(request : Request):
    db = DataBase()
    try:
        await db.get_user(request.session["username"])
        return RedirectResponse(url='/chat', status_code=status.HTTP_303_SEE_OTHER)
    except:
        return RedirectResponse(url='/signin', status_code=status.HTTP_303_SEE_OTHER)


@app.post("/login")
async def login_for_access_token(
    username = Form(), 
    password = Form(),
    request : Request = None
) -> Token:
    db = DataBase()
    user = db.auth(username, password)
    if not user:
        return templates.TemplateResponse(
        name='signin.html',
        context={
            'request': request,
            'error' : f"Incorrect username or password"
        }
    )
    access_token = jwt.encode({"sub": username}, _SECRET)
    request.session["access_token"] = access_token
    request.session["username"] = username
    return RedirectResponse(url='/chat', status_code=status.HTTP_303_SEE_OTHER)

'''
@app.post("/new-user")
async def signup_token(
    username = Form(), 
    password = Form(),
    password_again = Form(),
    request : Request = None
)-> Token:
    
    if password != password_again:
        return templates.TemplateResponse(
            name='signup.html',
            context={
                'request': request,
                'error' : 'Пароли не совпадают'
            }
        )
    db = DataBase()
    user = db.add_user(username, password)
    access_token = jwt.encode(
        {"sub": username}, _SECRET
    )
    request.session["access_token"] = access_token
    request.session["username"] = username
    return RedirectResponse(url='/chat', status_code=status.HTTP_303_SEE_OTHER)
'''

@app.get("/logout")
def logout(request : Request):
    request.session["access_token"] = ""
    return RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)

esse = Esse()
admin = Admin()
app = mount_gradio_app(app, esse.view(), path="/chat")
app = mount_gradio_app(app, admin.view(), path="/admin")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)