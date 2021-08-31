# [HLB] Home lab bot

[![Build Status](http://drone.melchior.reynet/api/badges/rey/home-lab-bot/status.svg)](http://drone.melchior.reynet/rey/home-lab-bot)

Чат бот для домашнего использования: если нужен простой API к своему домашнему серверу (aka home lab),
или просто нужен фронтенд в виде бота к какому-нибудь сервису.

* Нет жесткой зависимости от чат платформ. Поддерживается работа на (см. `core/gateways`): cli, telegram, gitter.
* Расширяем командами (см. `core/commands`).

## todo

* упаковать в докер и автоматизировать сборку - протестировать вариант питоновского приложения в докере + хранение логов в волуме
* тесты пописать
* линтеры добавить

## Запуск

### Docker

Локальная сборка и запуск с настройкой через переменные окружения.

> docker build -t local/hlb:0.1.0 .

> docker run --rm -it --env HLB_DEBUG=0 --name=hlb010 local/hlb:0.1.0

### Heroku

Procfile - Инструкции для запуска бота.
runtime.txt - Настройка версии python.

### Локальная разработка

#### Requirements
python 3.9