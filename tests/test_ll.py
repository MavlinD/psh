import pytest
from logrich.logger_ import log
import subprocess

from scripts.ll import ll

skip = False
# skip = True
reason = "Temporary off!"


@pytest.mark.skipif(skip, reason=reason)
def test_ll() -> None:
    """test shell ls"""
    log.debug(f"test of {ll.__doc__}")
    print("-")

    subprocess.run(["python3", "scripts/ll.py", "-la"])
