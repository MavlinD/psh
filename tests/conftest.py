from typing import Generator

import pytest

from _pytest.main import Session
from _pytest.nodes import Item

from rich.console import Console

console = Console()


def pytest_configure() -> None:
    """предотвратить поломку основной БД"""
    ...
    # if not config.TESTING:
    #     log.warning(
    #         "Переведите приложение в режим тестирования:\n" "установите переменную TESTING=True"
    #     )
    #     pytest.exit("Условие запуска тестов")


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir: str) -> Generator:
    """Fixture to execute asserts before and after a test is run"""
    print()
    yield


def pytest_sessionstart(session: Session) -> None:  # noqa
    """пусть будет"""
    pass


def pytest_runtest_call(item: Item) -> None:
    """печатает заголовок теста"""
    console.rule(f"[green]{item.parent.name}[/]::[yellow bold]{item.name}[/]")
