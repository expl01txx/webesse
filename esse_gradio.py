import functools
import gradio as gr
import json
from services import all_check
from db import DataBase
import logging
logging.basicConfig(filename='_webEsse.log',encoding='utf-8',
                    level = logging.INFO,
                    format = '%(asctime)s-%(levelname)s-%(process)d--->%(message)s')


def load_user(request : gr.Request):
    database = DataBase()
    username = request.request.session['username']
    return username, database.get_user_tokens(username), gr.update(choices=database.get_user_esses_list(username))

def get_esse(date, request: gr.Request):
    database = DataBase()
    username = request.request.session['username']
    return database.get_esse(username, date)
    
def check_esse(inp_task, inp_esse, request : gr.Request):
    database = DataBase()
    username = request.request.session['username']
    if not database.can_use(username):
        return 'Прошу прощения, у вас закончилось количество попыток.'
        
    if inp_esse=='':
        return 'Ошибка, недостает данных'
    if inp_task=='':
        return 'Ошибка, недостает данных'
    
    database.add_usage(username)
    database.add_log(username, inp_task, inp_esse, "output")
    return "output" #all_check(inp_task, inp_esse)

class Esse:
    def __init__(self):
        self.db = DataBase()


    def view(self):
        async def init_chat(request : gr.Request):
            if ("username" not in request.request.session or self.db.get_user(request.request.session['username']) == None):
                raise gr.Error("UNAUTHORIZED! Click \"Logout\" button to go to login page")
                

        with gr.Blocks() as demo:
            demo.load(fn=init_chat, inputs=None, outputs=None)
            with gr.Tab("Проверить эссе"):
                gr.Markdown("""# Проверка английского эссе.
                
            В первое окно введите задание на эссе.
            Второе окно само эссе и нажмите кнопку проверить.""")
                with gr.Row():
                    with gr.Column(scale=2):
                        inp_task = gr.Textbox(label='Задание', placeholder="Внестите сюда текст задания на эссе.", lines=3)
                        inp_esse=gr.Textbox(label='Эссе', placeholder="Внестите сюда текст эссе.", lines=5)
                        btn = gr.Button("Проверить")
                    with gr.Column(scale=3):
                        out = gr.Markdown("# Результаты проверки\n\nЗдесь вы увидите результаты проверки эссе.")
                btn.click(fn=check_esse, inputs=[inp_task, inp_esse], outputs=out)
            
            with gr.Tab("Личный кобинет"):
                user_login = gr.Textbox(label="Логин", interactive=False)
                user_tokens = gr.Textbox(label="Количество доступных проверок", interactive=False)
                
                gr.Button("Пополнить счет")

                select_esse = gr.Dropdown(label="Выбор Эссе", interactive=True)
                esse_task = gr.TextArea(label="Задание")
                with gr.Row():
                    esse_source = gr.TextArea(label="Эссе (источник)")
                    esse_result = gr.TextArea(label="Эссе (проверка)")

                select_esse.change(fn=get_esse, inputs=[select_esse], outputs=[esse_task, esse_source, esse_result])
                demo.load(load_user, inputs=None, outputs=[user_login, user_tokens, select_esse])
        return demo
    



