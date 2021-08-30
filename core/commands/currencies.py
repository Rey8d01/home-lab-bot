"""Команды для конвертации валют."""


from typing import Union

from . import register_command, ResultCommandText, ResultCommandTextPicture
from ..repositories.currencies import get_rates_for_currency

INTERESTING_CURRENCIES = frozenset(("USD", "EUR", "RUB"))  # Валюта для которой будут показаны конвертации.


@register_command(aliases=("converter", "conv", "cur"))
def converter(raw_query: str) -> Union[ResultCommandText, ResultCommandTextPicture]:
    """Конвертер валют. Принимает сумму и название валюты (rub usd eur), отдает результат в других валютах"""
    try:
        source_currency_sum, source_currency_type = raw_query.split(maxsplit=1)
        source_currency_sum = int(source_currency_sum)
    except ValueError:
        return ResultCommandText("Ошибка обработки валют: укажите исходные данные в виде: 123 USD")

    source_currency_type = source_currency_type.upper()
    interesting_currency_rates = get_rates_for_currency(source_currency_type, INTERESTING_CURRENCIES)
    if not interesting_currency_rates:
        return ResultCommandText(f"Ошибка обработки валют: курс валют определить не удалось")

    printable_result = "; ".join(f"{source_currency_sum * rate:.2f} {currency}" for currency, rate in interesting_currency_rates.items())
    return ResultCommandText(f"Расчет валюты для {source_currency_sum} {source_currency_type}: {printable_result}")
