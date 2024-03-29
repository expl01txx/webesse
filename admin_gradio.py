import gradio as gr
from db import DataBase
import random
import string


def get_user_info(username):
    database = DataBase()
    user_info = database.get_user_info(username)
    return user_info

def add_user_tokens(user_tokens, username, value):
    database = DataBase()
    database.add_user_tokens(username, value)
    return int(user_tokens) + value

def get_all_user_esses(username):
    database = DataBase()
    esses = database.get_all_user_esses(username)
    return gr.update(choices=esses)

def get_esse(username, date):
    database = DataBase()
    if isinstance(username, list): return
    return database.get_esse(username, date)

def add_user(username, password):
    database = DataBase()
    try:
        database.add_user(username, password)
        return "Пользователь успешно добавлен"
    except:
        return "Ошибка добавления пользователя"

def random_password():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))

database = DataBase()

#admin panel
class Admin:
    def __init__(self):
        self.db = DataBase()
    
    def view(self):

        async def init_chat(request : gr.Request):
            if ("username" not in request.request.session or self.db.get_user(request.request.session['username']) == None):
                request.request.url = "/login"
                raise gr.Error("UNAUTHORIZED! Click \"Logout\" button to go to login page")

        with gr.Blocks() as admin:
            with gr.Tab("Управление"):
                select_user = gr.Dropdown(database.get_users(), label="Users")
                with gr.Row():
                    user_tokens = gr.Label(label="Количество Проверок")
                    user_checks = gr.Label(label="Всего проверенно")
                    user_last_ativity = gr.Label(label="Последняя активность")

                slider = gr.Slider(0, 100, value=1, label="Выберите количество проверок")
                btn_add = gr.Button("Добавить")
                btn_add.click(fn=add_user_tokens, inputs=[user_tokens, select_user, slider], outputs=user_tokens)


                select_esse = gr.Dropdown(label="Выбор Эссе", interactive=True)

                esse_task = gr.TextArea(label="Задание")
                with gr.Row():
                    esse_source = gr.TextArea(label="Эссе (источник)")
                    esse_result = gr.TextArea(label="Эссе (проверка)")

                select_user.change(fn=get_user_info, inputs=select_user, outputs=[user_tokens, user_checks, user_last_ativity])
                select_user.change(fn=get_all_user_esses, inputs=[select_user], outputs=select_esse)
                select_esse.change(fn=get_esse, inputs=[select_user, select_esse], outputs=[esse_task, esse_source, esse_result])

            with gr.Tab("Добалвение Пользователя"):
                user_login = gr.Textbox(label="Логин")
                user_pass = gr.Textbox(label="Пароль")
                result = gr.Textbox(label="Результат")
                with gr.Row():
                    with gr.Column(scale=3):
                        btn_add_user = gr.Button("Добавить")
                    with gr.Column(scale=1):
                        rnd_pass = gr.Button("Сгенерировать случайный пароль")
                btn_add_user.click(fn=add_user, inputs=[user_login, user_pass], outputs=result)
                rnd_pass.click(fn=random_password, outputs=user_pass)
        return admin