import json
from datetime import date, datetime


def load_operations(file_name):
    """
    Загружает список банковских операций из файла
    :param file_name: имя файла
    :return: список банковских операций
    """
    with open(file_name, "r", encoding="utf8") as file:
        operations = json.load(file)
    return operations


def sort_operations(operations):
    """
    Сортирует банковские операции в порядке возрастания даты
    :param operations: список банковских операций
    :return: отсортированный список банковских операций
    """
    def sort_key(x): return datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f') \
        if ("date" in x) else datetime.fromtimestamp(0)
    return sorted(operations, key=sort_key)


def get_executed_operations(operations, limit=None):
    """
    Формирует список последних выполненных банковских операций в количестве limit
    :param operations: список банковских операций
    :param limit: количество банковских операций, подлежащих выборке
    :return: список выполненных банковских операций
    """
    executed_op = []
    for op in operations[::-1]:
        if len(executed_op) == limit:
            break
        if op["state"] == "EXECUTED":
            executed_op.append(op)
    return executed_op


def get_formatted_operations(operations):
    """
    Форматирует список банковских операций для вывода из на экран
    :param operations: список операций
    :return: список отформатированных операций
    """
    operation_list = []

    for op in operations:
        date_op = datetime.strptime(op["date"], '%Y-%m-%dT%H:%M:%S.%f')
        dict_op = {}

        source = masked_account(op["from"]) if "from" in op else ""
        destination = masked_account(op["to"]) if "to" in op else ""

        dict_op["date"] = date_op.strftime("%d.%m.%Y")
        dict_op["description"] = op["description"]
        dict_op["from"] = source
        dict_op["to"] = destination
        dict_op["amount"] = op["operationAmount"]["amount"]
        dict_op["currency"] = op["operationAmount"]["currency"]["name"]
        operation_list.append(dict_op)

    return operation_list


def masked_account(account):
    """
    Создает маску для банковских счетов и карт в формате XXXX XX** **** XXXX и **XXXX соответственно
    :param account: номер счета или карты
    :return: замаскированный номер счета или карты
    """
    masked = ""
    if account.lower().find("счет") == -1:
        masked = account[:-16] + account[-16:-12] + " " + account[-12:-10] + "** **** " + account[-4::]
    else:
        masked = "**" + account[-4::]
    return masked
