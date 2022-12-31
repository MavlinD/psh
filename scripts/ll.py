import pathlib
import re
from typing import Union

import sh
from logrich.logger_ import log
from rich.console import Console
from rich.filesize import decimal
from rich.table import Table
from rich.style import Style
import argparse


def ll(dps_list: Union[None, str] = None, column_delimiter: str = "~~~", sort: int = 2) -> Table:
    """shell ls"""

    if type(dps_list) is str:
        # удаляем последний перенос
        dps_ = (dps_list.split("\n"))[:-1]
    else:
        dps_ = sh.bash(
            "-c",
            f'ls -al --time-style=long-iso |  sed -r s"/\s+/{column_delimiter}/g"',
            # f'find . -maxdepth 1 -printf "%M{column_delimiter}%n{column_delimiter}%u{column_delimiter}%g{column_delimiter}%s{column_delimiter}%P\n"',
        )
        # dps_ = list(dps_)
    # log.debug("", o=dps_)
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

    table.add_column("Perms", justify="left", style="cyan", max_width=20)
    table.add_column("Chld", justify="left", style="green", max_width=27)
    table.add_column("User", justify="left", style="magenta", max_width=23)
    table.add_column("Group", justify="left", style="yellow")
    table.add_column("Size", justify="left", style="green", max_width=27)
    table.add_column("Date", justify="left", style="green", max_width=27)
    table.add_column("Time", justify="left", style="green", max_width=27)
    table.add_column("Icons", justify="left", style="magenta", max_width=23)
    table.add_column("Content", justify="left", style="yellow", no_wrap=False)

    def get_size(arg: str) -> str:
        size = decimal(int(arg))
        return str(size)

    def get_perm(arg: str) -> str:
        arg_ = arg[1:]
        resp = re.sub("r", "[#27C864]r[/]", arg_)
        # resp = re.sub("d", "[#27A1C8]d[/]", resp)
        resp = re.sub("x", "[#A6C827]x[/]", resp)
        resp = re.sub("w", "[#C87C27]w[/]", resp)
        resp = re.sub("-", "[#798721]-[/]", resp)
        return resp

    def get_content(arg: list) -> str:
        """определяет содержимое колонки контент"""
        item = arg[7][:-1]
        # item = arg[-1][:-1]
        # log.debug(arg)
        if arg[0][:1] == "d":
            # dir = ' '.join(arg[7:][:-1])
            return f"[blue]{' '.join(arg[7:])[:-1]}/[/]"
        ext = pathlib.Path(item).suffix
        if ext == ".sh":
            return f"[b #14E864]{arg[-1][:-1]}[/]"
        # если в имени ресурса есть пробелы
        if len(arg) > 8:
            # log.debug(arg)
            return " ".join(arg[7:])[:-1]
        return item

    def get_time(arg: str) -> str:
        return f"[not b]{arg}[/]"

    # return
    for key, val in enumerate(dps_):
        cells = val.split(column_delimiter)
        # print(cells)
        if key != 0:
            table.add_row(
                get_perm(cells[0]),
                cells[1],
                cells[2],
                cells[3],
                get_size(cells[4]),
                cells[5],
                get_time(cells[6]),
                # *cells[:-1],
                "icon",
                # cells[7],
                get_content(cells),
                style=(lambda key_: "on #18181C" if key_ % 2 else "on black")(key),
            )
    console = Console()
    console.print(table)
    return table


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sort", default=1, type=int, help="номер колонки для сортировки")
    args = parser.parse_args()

    ll(sort=args.sort)
