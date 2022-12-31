import pytest
from loguru import logger
from rich import print as rpr

from scripts.ll import ll
from scripts.docker_ps import dps

skip = False
# skip = True
reason = "Temporary off!"


@pytest.mark.skipif(skip, reason=reason)
def test_ll() -> None:
    """test shell ls"""
    logger.debug(f"test of {ll.__doc__}")
    print("")

    return
    with open("tests/dps_mock.txt") as fo:
        dps_mock = fo.read()
    # dps_mock = None

    if dps_mock:
        result = dps(dps_mock, sort=1)
        assert (
            result.__dict__["columns"][0]._cells[-1] == "fauth-db-v2"
        ), "последний элемент таблицы не совпадает"
        result = dps(dps_mock)
        assert (
            result.__dict__["columns"][0]._cells[-1] == "auth-api-neo"
        ), "последний элемент таблицы не совпадает"
    else:
        dps(sort=1)
        dps()
