FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

VOLUME /usr/src/app/tmp

COPY ./config ./config
COPY ./core ./core
COPY ./main.py .

CMD [ "python", "./main.py" ]
