#from peewee_models import OpenAI as OAI
import openai
from openai import OpenAI
import os
import time
import json
import logging
logging.basicConfig(filename='_webEsse.log',encoding='utf-8',
                    level = logging.INFO,
                    format = '%(asctime)s-%(levelname)s-%(process)d--->%(message)s')

client = OpenAI(api_key='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')

# добавить проверку исключений на рэйт лимит
# gpt-3.5-turbo-0125
# gpt-4-0125-preview
def get_GPT(messages, model='gpt-4-0125-preview') -> str:
    try:
        competition = client.chat.completions.create(
            messages=messages,
            model=model,
        )
        # задача: нет логирования токенов! надо добавить
        logs={'request':messages, 'response':competition.choices[0].message.content, 
              'completion_tokens':competition.usage.completion_tokens,
              'prompt_tokens':competition.usage.prompt_tokens,
             'total_tokens':competition.usage.total_tokens}
        with open(f'logs/{str(int(time.time()))}.json', 'w') as f:
            json.dump(logs, f)

        return competition.choices[0].message.content, competition #competition.choices[0].message.content
    except Exception as err:
        logging.error(f'Error while getting competition with ChatGPT. Error: {err}, --> {type(err)}')
        return 'Ошибка вызова модели', None
        
        
#### собираю все ответы
def all_check(task,text) -> str:
    response='# Результат проверки эссе:\n\n'
    r, messages=check_esse_services(task, text)
    response+=r
    response+="\n\n# Ошибки допущенные в эссе:\n\n"
    r, messages = check_error_services(text, messages)
    response+= r
    response+="\n\n# Идеальное эссе:\n\n"
    r, messages = check_thebest_services(text, messages)
    response+=r
    return response
        
        
def check_esse_services(task: str,text: str) -> str:
    try:
        with open('esse_check_prompt.txt', 'r', encoding="utf-8") as f:
            prompt=f.read()
    except:
        response='Извините, произошла ошибка. Не смог прочитать промпт.'
        return response, messages
        
    messages=[{'role':'system', 'content':'Ты лучший в мире русскоязычный преподаватель английского языка. Объясняй максимально просто, как для 10 летнего ребенка!'},
              {'role':'user', 'content':prompt % (task, text)}]
    response, _ =  get_GPT(messages)
    messages.append({'role':'assistant', 'content':response})

    return response, messages


def check_error_services(text: str, messages: list) -> str:
    try:
        with open('prompt_for_error.txt', 'r', encoding="utf-8") as f:
            prompt=f.read()
    except:
        response='Извините, произошла ошибка. Не смог прочитать промпт.'
        #oai = OAI(request=text, response=response)
        #oai.save()
        return response, messages
        
    messages.append({'role':'user', 'content':prompt % text})
    response, _ =  get_GPT(messages)
    messages.append({'role':'assistant', 'content':response})

    return response, messages

def check_thebest_services(text: str, messages: list) -> str:
    try:
        with open('the_best_variant.txt', 'r', encoding="utf-8") as f:
            prompt=f.read()
    except:
        response='Извините, произошла ошибка. Не смог прочитать промпт.'
        return response, messages
        
    messages.append({'role':'user', 'content':prompt % text})
    response, _ =  get_GPT(messages)
    messages.append({'role':'assistant', 'content':response})
    #oai = OAI(request=text, response=response)
    #oai.save()
    return response, messages