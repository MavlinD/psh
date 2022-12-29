from rich import print as rprint
from rich.console import Console
import sh
import pytest
from loguru import logger
from rich.table import Table

skip = False
# skip = True
reason = "Temporary off!"


@pytest.mark.skipif(skip, reason=reason)
def test_dps() -> None:
    """docker ps"""
    logger.debug(222)
    # log.debug(222)
    column_delimiter = "~~~"
    dps = sh.bash(
        "-c",
        f"docker ps --format 'table {{{{.Names}}}}{column_delimiter}{{{{.Status}}}}{column_delimiter}{{{{.Networks}}}}{column_delimiter}{{{{.Ports}}}}'",
    )
    print(dir(dps))
    print()
    # print(len(dps))
    # iter_length = len(list(uu))
    # print(iter_length)
    dps_list = list(dps)
    amount_rows = len(dps_list)
    table = Table(title="Star Wars Movies")

    table.add_column("Names", justify="right", style="cyan", no_wrap=True)
    table.add_column("Status", style="magenta")
    table.add_column("Networks", justify="right", style="green")
    table.add_column("Ports", justify="right", style="yellow")

    for key, val in enumerate(dps_list):
        # print(type(val))
        # print(val)
        cells = val.split(column_delimiter)
        # table.add_row(*cells)
        # table.add_row(*cells[:-1])
        # for cell in cells:
        #     rprint(cell, end="")
        # table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
        # ii = val.splitlines(amount_rows)
        # ii = val.splitlines(' ')
        # rprint(ii)
        # rprint(len(ii[0]))
        # rprint(val, end="")
        if key == 0:
            ...
            # table.add_row("Names", "Status", "Networks", "Ports")
        #     print("=" * 50)
        else:
            table.add_row(*cells[:-1], cells[-1][:-1])
        #     print("-" * 50)
    console = Console()
    # table.add_row("Cat", "Dog", "Guinea Pig")
    # table.add_row("Cat", "Dog", "Guinea Pig")
    # table.add_row("Cat", "Dog", "Guinea Pig")
    console.print(table)
    # console.print(table, end="\t")
