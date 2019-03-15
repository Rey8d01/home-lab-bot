"""Команды для работы с duckduckgo."""

from typing import Union

import requests

from . import register_command, ResultCommandText, ResultCommandTextPicture


@register_command(aliases=("s", "search", "ddg", "поиск"))
def _s(*args, **kwargs) -> Union[ResultCommandText, ResultCommandTextPicture]:
    """Search - простой поиск через duckduckgo, принимает строку для поиска."""
    raw_query = args[0]
    complete_query = "+".join(raw_query.split())
    request = requests.get(f"https://api.duckduckgo.com/?q={complete_query}&format=json")
    result_search_query = request.json()

    parsed_results = ""
    if result_search_query["Results"]:
        parsed_results = "\n".join(f"{item_found_result['Text']} {item_found_result['FirstURL']}"
                                   for item_found_result in result_search_query["Results"])

    abstract_result = ""
    if result_search_query["AbstractText"] or result_search_query["AbstractURL"]:
        abstract_result = f"{result_search_query['AbstractText']} {result_search_query['AbstractURL']}".strip()

    if not abstract_result and not parsed_results:
        return ResultCommandText("Ничего не получилось найти :(")
    common_results = f"{abstract_result}\n{parsed_results}"

    if result_search_query["Image"]:
        return ResultCommandTextPicture(common_results, result_search_query["Image"])
    return ResultCommandText(common_results)
