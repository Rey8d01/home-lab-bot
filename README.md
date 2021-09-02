# [HLB] Home lab bot

[![Build Status](http://drone.melchior.reynet/api/badges/rey/home-lab-bot/status.svg)](http://drone.melchior.reynet/rey/home-lab-bot)

Чат бот для домашнего использования: если нужен простой API к своему домашнему серверу (aka home lab),
или просто нужен фронтенд в виде бота к какому-нибудь сервису.

* Нет жесткой зависимости от чат платформ. Поддерживается работа на (см. `core/gateways`): cli, telegram, gitter.
* Расширяем командами (см. `core/commands`).
* Требуется python 3.9

## todo

* оформить CONTRIBUTING.md
* автоматизировать локальный деплой

## Запуск

Бот с настройками по умолчанию запускается в режиме работы через CLI.

> python main.py

### Docker

Локальная сборка и запуск с настройкой через переменные окружения.

Подробнее о передаче параметров через env см. в `config/settings.toml`.
Так же можно скопировать файл `config/settings.toml` в `config/local_settings.toml`
и переопределить все настройки для сборки образа без использования env.

Постоянный внешний volume не является обязательным, он ссылается на директорию (в рамках проекта `./tmp` в `.gitignore`),
в которой хранятся логи в локальные кеши.

> docker build -t local/hlb:0.1.0 .
>
> docker volume create hlb-tmp
>
> docker run --rm -it -v hlb-tmp:/usr/src/app/tmp --env HLB_DEBUG=0 --name=hlb010 local/hlb:0.1.0

### Heroku

Procfile - Инструкции для запуска бота.
runtime.txt - Настройка версии python.
