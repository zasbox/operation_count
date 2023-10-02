from src.utils.utils import *

operations = get_formatted_operations(
    get_executed_operations(
        sort_operations(
            load_operations("../operations.json")), 5))

for op in operations:
    _str = (op["date"] + " " + op["description"] + "\n" + op["from"] + " -> " + op["to"] + "\n" +
            op["amount"] + " " + op["currency"] + "\n")
    print(_str)
