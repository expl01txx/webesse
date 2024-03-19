#создаем срезу, запускаем через docker-compose.yaml
#скопилируем образ
#docker build -t python_image .
#фиксируем версию
FROM python:3.11-bookworm

WORKDIR /usr/app

#можно и лучше через requirements.txt
#COPY requirements.txt .

RUN pip install openai gradio

#использовать если запускаем как Dockerfile
#COPY . .
#
#RUN ls -la
#CMD python3 bot.py