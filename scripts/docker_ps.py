from typing import Union

import sh
from rich import print as pr
from rich.console import Console
from rich.table import Table
from rich.style import Style
import argparse


def dps(dps_list: Union[None, str] = None, column_delimiter: str = "~~~", sort: int = 2) -> Table:
    """docker ps, по умолчанию вывод не сортируется, точнее сортируется как docker ps выводит - по времени работы процессов"""

    if type(dps_list) is str:
        # удаляем последний перенос
        dps_ = (dps_list.split("\n"))[:-1]
    else:
        dps_ = sh.bash(
            "-c",
            f"docker ps --format 'table {{{{.Names}}}}{column_delimiter}{{{{.Status}}}}{column_delimiter}{{{{.Networks}}}}{column_delimiter}{{{{.Ports}}}}'",
        )
        dps_ = list(dps_)

    if sort == 1:
        # сортируем, сохраняем первую строку - заголовок
        first_row = dps_[:1]
        # сортируем по первой колонке
        dps_2 = dps_[1:]
        dps_2.sort()
        # собираем снова список
        dps_ = first_row + dps_2

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
    table.add_column("Status", justify="left", style="green", max_width=27)
    table.add_column("Networks", justify="left", style="magenta", max_width=23)
    table.add_column("Ports", justify="left", style="yellow")

    rows = 0
    for key, val in enumerate(dps_):
        cells = val.split(column_delimiter)
        if key != 0:
            table.add_row(
                cells[0],
                cells[1],
                # сети слеплены без пробела
                ", ".join(cells[2].split(",")),
                # последняя клетка может содержать или не содержать символ новой строки
                (lambda cell: cells[-1][:-1] if cells[-1][-1:] == "\n" else cells[-1])(cells),
                style=(lambda key_: "on #18181C" if key_ % 2 else "on black")(key),
            )
        rows = key

    def print_ps(table: Table, rows: int) -> Table:
        """принтит как пейджер, если высота консоли меньше кол-ва строк в выводе"""
        console = Console(force_terminal=True)
        if rows > console.size.height:
            with console.pager(styles=True):
                console.print(table)
        else:
            pr(table)
        # pr(console.size.height)
        return table

    return print_ps(table=table, rows=rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sort", default=1, type=int, help="номер колонки для сортировки")
    args = parser.parse_args()

    dps(sort=args.sort)
