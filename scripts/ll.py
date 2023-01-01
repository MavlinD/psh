from datetime import datetime
import pathlib
import re

import click
import sh

# from logrich.logger_ import log  # noqa
from rich.console import Console
from rich.filesize import decimal
from rich.table import Table
from rich.style import Style


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("arg", default="-la")
def ll(arg: str = "-al") -> Table:
    """shell; ls - дополнительные аргументы ls"""
    # log.debug(arg)
    column_delimiter: str = "~~~"
    dps_ = sh.bash(
        "-c",
        f'ls {arg} --time-style="+%Y-%m-%d %T" |  sed -r s"/\s+/{column_delimiter}/g"',
    )
    # log.debug("", o=dps_)

    table_header_style = Style(color="#3385BF", bold=False)

    table = Table(
        header_style=table_header_style,
        padding=(0, 2),
        collapse_padding=True,
        show_edge=True,
        box=None,
        show_header=False,
    )

    table.add_column("Perms", justify="left", style="cyan", max_width=20)
    table.add_column("Chld", justify="right", style="green", max_width=27)
    table.add_column("User", justify="left", style="magenta", max_width=23)
    table.add_column("Group", justify="left", style="yellow")
    table.add_column("Size", justify="right", style="green", max_width=27)
    table.add_column("SizeD", justify="left", style="cyan")
    table.add_column("Time", justify="left", style="green", max_width=27)
    table.add_column("I", justify="left", style="magenta", max_width=23)
    table.add_column("Content", justify="left", style="yellow")

    def get_size(arg: str) -> list:
        """вывод размеров контента"""
        size = decimal(int(arg))
        size_, dim = str(size).split(" ")
        return [f"[b cyan]{size_}[/]", f"[cyan]{dim}[/]"]

    def get_perm(arg: str) -> str:
        """формирует вывод разрешений"""
        arg_ = arg[1:]
        resp = re.sub("r", "[#27C864]r[/]", arg_)
        resp = re.sub("x", "[#A6C827]x[/]", resp)
        resp = re.sub("w", "[#C87C27]w[/]", resp)
        resp = re.sub("-", "[#798721]-[/]", resp)
        return resp

    def get_content(arg: list) -> str:
        """определяет содержимое колонки контент"""
        item = arg[7][:-1]
        if arg[0][:1] == "d":
            return f"[#00B1FE]{' '.join(arg[7:])[:-1]}/[/]"
        ext = pathlib.Path(item).suffix
        if ext == ".sh":
            return f"[b #14E864]{arg[-1][:-1]}[/]"
        # если в имени ресурса есть пробелы
        if len(arg) > 8:
            # log.debug(arg)
            return " ".join(arg[7:])[:-1]
        return item

    def get_time(date: str, time_: str) -> str:
        format_ = "%Y-%m-%d %H:%M:%S"
        format_out = "%Y-%b-%d %T"
        datetime_created = datetime.strptime(f"{date} {time_}", format_)
        diff_hours = (datetime.now() - datetime_created).total_seconds() / 3600
        timestamp = datetime_created.strftime(format_out)
        if diff_hours < 1:
            return f"[not b #68FE00]{timestamp}[/]"
        if diff_hours < 12:
            return f"[not b #38FF86]{timestamp}[/]"
        return f"[not b #65A57D]{timestamp}[/]"

    def get_icon(arg: list) -> str:
        """get icon from ext content"""
        ext = arg[7:][-1:][0].split(".")[-1].strip().lower()
        if ext == "ini":
            return "[yellow][/]"
        if ext == "md":
            return "[yellow][/]"
        if ext == "lock":
            return "[yellow][/]"
        if ext in [
            "mp3",
            "flack",
        ]:
            return "[yellow][/]"
        if ext in [
            "jpeg",
            "jpg",
            "bmp",
            "ico",
            "webp",
        ]:
            return "[yellow][/]"
        if ext == "sh":
            return "[green][/]"
        if ext == "env":
            return "[green][/]"
        if ext == "txt":
            return "[green][/]"
        if ext == "vscode":
            return "[green][/]"
        if ext == "log":
            return "[green][/]"
        if ext == "js":
            return "[green][/]"
        if ext == "git":
            return "[green][/]"
        if ext == "bin":
            return "[green][/]"

        if arg[0][:1] == "d":
            return "[blue][/]"

        return "[yellow][/]"

    for key, val in enumerate(dps_):
        cells = val.split(column_delimiter)
        # print(cells)
        if key != 0:
            table.add_row(
                get_perm(cells[0]),
                cells[1],
                cells[2],
                cells[3],
                *get_size(cells[4]),
                get_time(cells[5], cells[6]),
                get_icon(cells),
                get_content(cells),
                style=(lambda key_: "on #18181C" if key_ % 2 else "on black")(key),
            )
    console = Console()
    console.print(table)
    return table


if __name__ == "__main__":
    ll()
