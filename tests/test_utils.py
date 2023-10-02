import pytest

from src.utils.utils import *


@pytest.fixture
def op_list():
    return load_operations("../operations.json")[:5]


def test_sort_operations(op_list):
    operations = sort_operations(op_list)
    dates = [op["date"].split("T")[0] for op in operations]
    assert dates == ["2018-03-23", "2018-06-30", "2019-04-04", "2019-07-03", "2019-08-26"]


def test_get_executed_operations(op_list):
    op_list[1]["state"] = "CANCELED"
    op_list = get_executed_operations(op_list, 3)
    assert len(op_list) == 3


def test_get_formatted_operations(op_list):
    op = get_formatted_operations(op_list)[0]
    assert op["date"] == "26.08.2019"
    assert op["from"] == "Maestro 1596 83** **** 5199"
    assert op["to"] == "**9589"
