import pytest
from scripts.docker_ps import dps

skip = False
# skip = True
reason = "Temporary off!"


@pytest.mark.skipif(skip, reason=reason)
def test_dps() -> None:
    """test docker ps"""
    # logger.debug()
    print()

    with open("tests/dps_mock.txt") as fo:
        dps_mock = fo.read()
    # dps_mock=None

    if dps_mock:
        dps(dps_mock)
    else:
        dps()
