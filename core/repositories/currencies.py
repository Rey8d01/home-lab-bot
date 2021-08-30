"""Репозиторий запросов к сервисам информации с валютой.

https://www.live-rates.com/rates

"""

import json
import time
from collections import defaultdict
from typing import Iterable, Dict, Optional

import requests

from config import LOCAL_TMP_PATH


__currencies_info_created: Optional[float] = None  # Переменная модуля для локального отслеживания времени жизни кеша данных о валютах.
CURRENCIES_CACHE_PATH = LOCAL_TMP_PATH / "currencies_cache.json"  # Путь до локального кеша валют.


def receive_currencies_info() -> Optional[Dict]:
    """Получение информации о валютах и кеширование ее в локальный файл."""
    global __currencies_info_created
    current_time = time.time()
    if not __currencies_info_created or (current_time - __currencies_info_created) > 3600:  # ttl local cache.
        __currencies_info_created = current_time

        rates_request = requests.get(f"https://www.live-rates.com/rates")
        try:
            rates_request.json()  # Если json парсится нормально и не выбрасывает ошибок, значит можно его закешировать.
            with open(CURRENCIES_CACHE_PATH, "w", encoding="utf-8") as currencies_cache:
                currencies_cache.write(rates_request.text)
        except ValueError:
            pass

    if not CURRENCIES_CACHE_PATH.exists():
        return None

    with open(CURRENCIES_CACHE_PATH) as currencies_cache_file:
        raw_currency_rates = json.load(currencies_cache_file)
    return raw_currency_rates


def get_all_currency_rates() -> Dict[str, Dict[str, float]]:
    """Вернет все коэффициенты валют между собой."""
    raw_currencies_info = receive_currencies_info()
    currency_rates = defaultdict(lambda: defaultdict(float))
    for raw_currency_info in raw_currencies_info:
        if "/" in raw_currency_info["currency"]:
            currency_from, currency_to = raw_currency_info["currency"].split("/", maxsplit=1)

            try:
                currency_rate = float(raw_currency_info["rate"])
            except ValueError:
                # Все ошибки с неправильным преобразованием игнорируем.
                continue
            currency_rates[currency_from][currency_to] = currency_rate
            # Рассчитывается сразу обратное отношение валют на случай если они отсутствуют в исходных данных.
            currency_rates[currency_to][currency_from] = 1 / currency_rate

    return currency_rates


def get_rates_for_currency(source_currency: str, interesting_currencies: Iterable[str]) -> Optional[Dict[str, float]]:
    """Вернет коэффициенты интересующих валют по отношению к исходной."""
    all_currency_rates = get_all_currency_rates()
    if source_currency not in all_currency_rates:
        return None

    interesting_currency_rates = {
        interesting_currency: all_currency_rates[source_currency][interesting_currency]
        for interesting_currency in interesting_currencies
        if interesting_currency != source_currency
    }

    return interesting_currency_rates
