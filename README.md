# geth

[![Build Status](http://drone.melchior.reynet/api/badges/rey/geth/status.svg)](http://drone.melchior.reynet/rey/geth)

> core bot

## Цели

* сделать базовый интерфейс бота который принимал бы тестовые команды и реагировал на них
* упаковать в докер и автоматизировать сборку - протестировать вариант питоновского приложения в докере
* написать еще пару команд

## Запуск

### Docker

Локальная сборка и запуск с настройкой через переменные окружения.

> docker build -t local/geth:0.1.0 .

> docker run --rm -it --env GETH_DEBUG=0 --name=geth010 local/geth:0.1.0

### Heroku

Procfile - Инструкции для запуска бота.
runtime.txt - Настройка версии python.

### Локальная разработка

#### Requirements
python 3.9