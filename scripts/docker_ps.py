from typing import Union

import sh
from sh import RunningCommand
from rich.console import Console
from rich.table import Table


def dps(dps_list: Union[str, RunningCommand]=None, column_delimiter:str = "~~~") -> None:
    """docker ps"""

    if type(dps_list) is RunningCommand:
        dps_ = list(dps_list)
    elif type(dps_list) is str:
        dps_ = dps_list.split("\n")
    else:
        dps_ = sh.bash(
            "-c",
            f"docker ps --format 'table {{{{.Names}}}}{column_delimiter}{{{{.Status}}}}{column_delimiter}{{{{.Networks}}}}{column_delimiter}{{{{.Ports}}}}'",
        )

    # amount_rows = len(dps_)
    table = Table(
        highlight=True,
        # show_header=False,
        padding=(0, 2),
        collapse_padding=True,
        show_edge=True,
        # show_lines=False,
        show_footer=False,
        # expand=True,
        box=None,
    )

    table.add_column("Names", justify="center", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center", style="magenta")
    table.add_column("Networks", justify="left", style="green")
    table.add_column("Ports", justify="center", style="yellow")

    for key, val in enumerate(dps_):
        cells = val.split(column_delimiter)
        if key == 0:
            ...
        else:
            table.add_row(
                *cells[:-1],
                cells[-1][:-1],
                style=(lambda key: "on black" if key % 2 else "on #18181C")(key)
            )
        #     print("-" * 50)
    console = Console()
    console.print(table)
    # console.print(table, end="\t")
