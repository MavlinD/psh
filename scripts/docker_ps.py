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
        # dps_ = dps_list.split("\n")
        dps_ = (dps_list.split("\n"))[:-1]
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

    table.add_column("Names", justify="left", style="red")
    table.add_column("Status", justify="left", style="green")
    table.add_column("Networks", justify="left", style="magenta")
    table.add_column("Ports", justify="left", style="yellow")

    for key, val in enumerate(dps_):
        cells = val.split(column_delimiter)
        if key != 0:
            table.add_row(
                # сначала все клетки кроме последней
                *cells[:-1],
                # последняя клетка может содержать или не содержать символ новой строки
                (lambda cell: cells[-1][:-1] if cells[-1][-1:] == '\n' else cells[-1])(cells),
                style=(lambda key_: "on #18181C" if key_ % 2 else "on black")(key)
            )
    console = Console()
    console.print(table)
    # console.print(table, end="\t")
