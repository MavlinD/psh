from typing import Union

import sh
from sh import RunningCommand
from rich.console import Console
from rich.table import Table
from rich.style import Style


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

    table_header_style = Style(color="#3385BF", bold=False)

    table = Table(
        highlight=True,
        header_style=table_header_style,
        padding=(0, 2),
        collapse_padding=True,
        show_edge=True,
        box=None,
    )

    table.add_column("Names", justify="left", style="red", max_width=20)
    table.add_column("Status", justify="left", style="green", max_width=20)
    table.add_column("Networks", justify="left", style="magenta", max_width=20)
    table.add_column("Ports", justify="left", style="yellow")

    for key, val in enumerate(dps_):
        cells = val.split(column_delimiter)
        if key != 0:
            table.add_row(
                cells[0],
                cells[1],
                # сети слеплены без пробела
                ', '.join(cells[2].split(',')),
                # последняя клетка может содержать или не содержать символ новой строки
                (lambda cell: cells[-1][:-1] if cells[-1][-1:] == '\n' else cells[-1])(cells),
                style=(lambda key_: "on #18181C" if key_ % 2 else "on black")(key)
            )
    console = Console()
    console.print(table)
    # console.print(table, end="\t")


if __name__ == '__main__':
    dps()
