"""Команды для конвертации валют."""

from core.commands.interfaces import TextCommandResult, CommandResult
from core.commands.utils import register_command
from core.repositories.currencies import get_rates_for_currency

INTERESTING_CURRENCIES = frozenset(("USD", "EUR", "RUB"))  # Валюта для которой будут показаны конвертации.


@register_command(aliases=("converter", "conv", "cur"))
def converter(raw_query: str, **kwargs) -> CommandResult:
    """Конвертер валют. Принимает сумму и название валюты (rub usd eur), отдает результат в других валютах: cur 300 usd"""
    try:
        raw_source_currency_sum, source_currency_type = raw_query.split(maxsplit=1)
        source_currency_sum = int(raw_source_currency_sum)
    except ValueError:
        return TextCommandResult("Ошибка обработки валют: укажите исходные данные в виде: 123 USD")

    source_currency_type = source_currency_type.upper()
    interesting_currency_rates = get_rates_for_currency(source_currency_type, INTERESTING_CURRENCIES)
    if not interesting_currency_rates:
        return TextCommandResult(f"Ошибка обработки валют: курс валют определить не удалось")

    printable_result = "; ".join(f"{source_currency_sum * rate:.2f} {currency}" for currency, rate in interesting_currency_rates.items())
    return TextCommandResult(f"Расчет валюты для {source_currency_sum} {source_currency_type}: {printable_result}")
