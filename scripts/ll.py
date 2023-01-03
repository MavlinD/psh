from datetime import datetime
import re

import click
import sh
from rich.console import Console

# from logrich.logger_ import log  # noqa

from rich.filesize import decimal
from rich.table import Table
from rich import print as pr

# from assets.tools import timer


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("path", default=".")
@click.argument("arg", default="-la")
# @timer
def ll(path: str = ".", arg: str = "-al") -> Table:
    """shell; ls - дополнительные аргументы ls"""
    # log.trace(path)
    # log.debug(arg)
    column_delimiter: str = "~~~"
    dps_ = sh.bash(
        "-c",
        f'ls {path} {arg} --time-style="+%Y-%m-%d %T" |  sed -r s"/\s+/{column_delimiter}/g"',
    )
    # log.debug("", o=dps_)

    table = Table(
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
    table.add_column("SizeD", justify="left", style="cyan", max_width=10)
    table.add_column("Time", justify="left", style="green", max_width=27)
    table.add_column("I", justify="left", style="magenta", max_width=23)
    table.add_column("Content", justify="left", style="yellow")

    # @timer
    def print_ls(table: Table, rows: int) -> Table:
        """принтит как пейджер, если высота консоли меньше кол-ва строк в выводе"""
        console = Console(force_terminal=True)
        if rows > console.size.height:
            with console.pager(styles=True):
                console.print(table)
        else:
            pr(table)
        # pr(console.size.height)
        return table

    # @timer
    def get_size(arg_: str) -> tuple:
        """вывод размеров контента"""
        size = decimal(int(arg_))
        size_, dim = str(size).split(" ")
        if dim =='bytes':
            dim_=f"[dim cyan]B[/]"
        elif dim == 'kB':
            dim_=f"[#A0D3D3]{dim}[/]"
        else:
            dim_=f"[#11EBEB]{dim}[/]"
        return f"[#9A4CF5]{size_}[/]", dim_

    # @timer
    def get_perm(arg_: str) -> str:
        """формирует вывод разрешений"""
        # удаляем признак папки - d
        arg__ = arg_[1:]
        resp = re.sub("r", "[#27C864]r[/]", arg__)
        resp = re.sub("x", "[#E13200]x[/]", resp)
        resp = re.sub("w", "[#BAE100]w[/]", resp)
        resp = re.sub("-", "[#798721]-[/]", resp)
        return resp

    # @timer
    def get_time(date: str, time_: str) -> str:
        """формирует время"""
        format_in = "%Y-%m-%d %H:%M:%S"
        format_out = "%Y-%b-%d %T"
        datetime_created = datetime.strptime(f"{date} {time_}", format_in)
        diff_hours = (datetime.now() - datetime_created).total_seconds() / 3600
        timestamp = datetime_created.strftime(format_out)
        if diff_hours < 1:
            return f"[not b #68FE00]{timestamp}[/]"
        if diff_hours < 12:
            return f"[not b #38FF86]{timestamp}[/]"
        return f"[not b #65A57D]{timestamp}[/]"

    # @timer
    def get_content(arg_: list) -> str:
        """определяет содержимое колонки контент"""
        item = arg_[7].strip()
        if arg_[0][:1] == "d":
            return f"{' '.join(arg_[7:]).strip()}/"
        # если в имени ресурса есть пробелы
        if len(arg_) > 8:
            # log.debug(arg_)
            return " ".join(arg_[7:]).strip()
        return item

    # @timer
    def get_icon(arg_: list) -> tuple:
        """get icon from ext content"""
        content = get_content(arg_)
        ext = arg_[7:][-1:][0].split(".")[-1].strip().lower()
        if ext == "ini":
            return "[yellow][/]", f"[#DAF7A6]{content}[/]"
        if ext == "pdf":
            return "[yellow][/]", f"[#D98880]{content}[/]"
        if ext == "db":
            return "[yellow][/]", f"[#14E864]{content}[/]"
        if ext == "mp4":
            return "[yellow][/]", f"[#93C6E9]{content}[/]"
        if ext == "xml":
            return "[yellow][/]", f"[#14E864]{content}[/]"
        if ext == "html":
            return "[yellow][/]", f"[#9B59B6]{content}[/]"
        if ext == "apk":
            return "[yellow][/]", f"[yellow]{content}[/]"
        if ext == "md":
            return "[yellow][/]", f"[#D98880]{content}[/]"
        if ext == "lock":
            return "[yellow][/]", f"[#14E864]{content}[/]"
        if ext in [
            "mp3",
            "flack",
        ]:
            return "[yellow][/]", f"[#30FCF3]{content}[/]"
        if ext in [
            "jpeg",
            "jpg",
            "bmp",
            "png",
            "ico",
            "webp",
            "gif",
        ]:
            return "[yellow][/]", f"[#BF1FD8]{content}[/]"
        if ext in [
            "xls",
            "xlsx",
            "csv",
        ]:
            return "[yellow][/]", f"[#14E864]{content}[/]"
        if ext in [
            "doc",
            "docx",
        ]:
            return "[yellow][/]", f"[#D87C1F]{content}[/]"
        if ext in [
            "gz",
            "zip",
            "rar",
        ]:
            return "[yellow][/]", f"[#A50079]{content}[/]"
        if ext in [
            "sh",
        ]:
            return "[green][/]", f"[#14E864]{content}[/]"
        if ext in ["appimage"]:
            return "[b green][/]", f"[#14E864]{content}[/]"
        if ext == "json":
            return "[yellow][/]", f"[#76C200]{content}[/]"
        if ext == "env":
            return "[green][/]", f"[#DAF7A6]{content}[/]"
        if ext == "txt":
            return "[green][/]", f"[#D87C1F]{content}[/]"
        if ext == "vscode":
            return "[green][/]", f"[#14E864]{content}[/]"
        if ext == "log":
            return "[green][/]", f"[#D87C1F]{content}[/]"
        if ext == "js":
            return "[green][/]", f"[#FF5733]{content}[/]"
        if ext == "git":
            return "[green][/]", f"[#14E864]{content}[/]"
        if ext == "bin":
            return "[green][/]", f"[#14E864]{content}[/]"

        if arg_[0][:1] == "d":
            return "[blue][/]", f"[b #30BBFC]{content}[/]"

        return "[yellow][/]", f"[yellow]{content}[/]"

    rows=0
    for key, val in enumerate(dps_):
        cells = val.split(column_delimiter)
        # print(cells)
        if key != 0:
            # exclude total info
            table.add_row(
                get_perm(cells[0]),  # 1 sec
                cells[1],
                cells[2],
                cells[3],
                *get_size(cells[4]),  # 0.7 sec
                get_time(cells[5], cells[6]),  # 0.8 sec
                *get_icon(cells),  # 0.6 sec
                style=(lambda key_: "on #18181C" if key_ % 2 else "on black")(key),
            )
        rows=key
    return print_ls(table=table, rows=rows)


if __name__ == "__main__":
    ll()
