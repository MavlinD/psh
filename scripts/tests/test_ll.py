import sys

import pytest
from logrich.logger_ import log
import subprocess

from scripts.assets.tools import timer
from scripts.ll import ll
from rich import print as pr

skip = False
# skip = True
reason = "Temporary off!"


@pytest.mark.skipif(skip, reason=reason)
@timer
def test_ll() -> None:
    """test shell ls"""
    log.debug(f"test of {ll.__doc__}")
    print("-")
    # log.debug('', o=sys.path)

    subprocess.run(["python3", "scripts/ll.py", ".", "-l", "--sv=1"])
    # subprocess.run(["python3", "scripts/ll.py", ".", "-la", "--sv=1"])
    # subprocess.run(["python3", "scripts/ll.py"])
    # subprocess.run(["python3", "scripts/ll.py", ".."])
    # subprocess.run(["python3", "scripts/ll.py", ".", "-la"])
    # r = subprocess.run(["python3", "scripts/ll.py", ".", "-l"])
    # pr(r)
    # subprocess.run(["python3", "scripts/ll.py", "..", "-la"])
