# [HLB] Home lab bot

[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)

Чат бот для домашнего использования: если нужен простой API к своему домашнему серверу (aka home lab),
или просто нужен фронтенд в виде бота к какому-нибудь сервису.

* Бот поддерживает простое синхронное общение вида запрос-ответ.
* Нет жесткой зависимости от чат платформ. Поддерживается работа на (см. `./core/gateways`): cli, telegram, gitter.
* Расширяем командами (см. `./core/commands`).
* Требуется python 3.9

Положения по дизайну описаны в CONTRIBUTING.md

## Запуск

Бот с настройками по умолчанию запускается в режиме работы через CLI.

> python main.py

### Docker

Локальная сборка и запуск с настройкой через переменные окружения.
Подробнее о передаче параметров через env см. в `./config/settings.toml`.

Постоянный внешний volume не является обязательным, он ссылается на директорию (в рамках проекта `./tmp` в `.gitignore`),
в которой хранятся логи в локальные кеши.

> docker build -t local/hlb:0.1.0 .
>
> docker volume create hlb-tmp
>
> docker run --rm -it -v hlb-tmp:/usr/src/app/tmp --env HLB_DEBUG=0 --name=hlb010 local/hlb:0.1.0

### Heroku

Файлы `Procfile` и `runtime.txt` нужны для запуска бота через Heroku Git.
Buildpacks: `heroku/python`. Настройки передавать в разделе Settings/Config Vars как переменные окружения (детали см. в `./config/`).
