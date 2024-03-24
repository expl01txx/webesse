import functools
import gradio as gr
import json
from services import all_check
from db import DataBase
import logging
logging.basicConfig(filename='_webEsse.log',encoding='utf-8',
                    level = logging.INFO,
                    format = '%(asctime)s-%(levelname)s-%(process)d--->%(message)s')


def auth_func(username, password):
    database = DataBase()
    logging.log(logging.INFO, str(database.auth(username, password)))
    return database.auth(username, password)

def load_user(request : gr.Request):
    database = DataBase()
    return request.username, database.get_user_tokens(request.username), gr.update(choices=database.get_user_esses_list(request.username))

def get_esse(date, request: gr.Request):
    database = DataBase()
    return database.get_esse(request.username, date)

database = DataBase()
    
def check_esse(inp_task, inp_esse, request : gr.Request):
    database = DataBase()
    # добавить сохранение попыток
    # собирать текст, в том числе и рекомендации по ошибкам
    #return(f"{request.username}Hey! " + input + ", Take care! ")
    if not database.can_use(request.username):
        return 'Прошу прощения, у вас закончилось количество попыток.'
        
    if inp_esse=='':
        return 'Ошибка, недостает данных'
    if inp_task=='':
        return 'Ошибка, недостает данных'
    
    database.add_usage(request.username)
    database.add_log(request.username, inp_task, inp_esse, "output")
    return "output" #all_check(inp_task, inp_esse)


with gr.Blocks() as demo:
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



demo.launch(server_name='0.0.0.0', server_port=7860, 
            show_api=False, 
            auth = auth_func, 
            auth_message= "Введите пароль или запросите его у владельца TG @aikula", 
            share=False,
            )

