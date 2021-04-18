FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./config ./config
COPY ./core ./core
COPY ./main.py .

CMD [ "python", "./main.py" ]
#сделать образ и запустить контейнер из образа но в момент запуска подменить переменную окружения дебаг