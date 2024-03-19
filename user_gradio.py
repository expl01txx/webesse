import gradio as gr
from db import DataBase

def auth_func(username, password):
    database = DataBase()
    success = database.auth(username, password)
    if database.is_admin(username) and success:
        return True
    return False

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
    return esses

database = DataBase()

#admin panel
with gr.Blocks() as admin:
    with gr.Tab("Admin panel"):
        select_user = gr.Dropdown(database.get_users(), label="Users")
        with gr.Row():
            user_tokens = gr.Label(label="Количество токенов")
            user_checks = gr.Label(label="Всего проверенно")
            user_last_ativity = gr.Label(label="Последняя активность")

        slider = gr.Slider(0, 100, value=1, label="Количество токенов")
        btn_add = gr.Button("Добавить токены")
        btn_add.click(fn=add_user_tokens, inputs=[user_tokens, select_user, slider], outputs=user_tokens)


        select_esse = gr.Dropdown(label="Эссе")
        all_esses = gr.TextArea(label="Все проверенные эссэ")

        select_user.change(fn=get_user_info, inputs=select_user, outputs=[user_tokens, user_checks, user_last_ativity])
        select_user.change(fn=get_all_user_esses, inputs=select_user, outputs=select_esse.choices)
        

admin.launch(server_name='127.0.0.1', server_port=7861, 
            show_api=False, 
            auth = auth_func, 
            auth_message= "Введите пароль или запросите его у владельца TG @aikula", 
            share=False,
            )