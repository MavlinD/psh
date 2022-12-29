import sh
from rich.console import Console
from rich.table import Table
from rich.style import Style


def dps(dps_list: str=None, column_delimiter:str = "~~~") -> None:
    """docker ps"""

    if type(dps_list) is str:
        # удаляем последний перенос
        dps_ = (dps_list.split("\n"))[:-1]
    else:
        dps_ = sh.bash(
            "-c",
            f"docker ps --format 'table {{{{.Names}}}}{column_delimiter}{{{{.Status}}}}{column_delimiter}{{{{.Networks}}}}{column_delimiter}{{{{.Ports}}}}'",
        )
        dps_ = list(dps_)

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


if __name__ == '__main__':
    dps()
