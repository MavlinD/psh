### Shell command in python

```shell
# docker ps
python3 scripts/docker_ps.py
# sort by first column
python3 scripts/docker_ps.py 1
# sort by second column
python3 scripts/docker_ps.py 2
# shell ls
python3 scripts/ll.py --help
```

```shell
# copy docker_ps.py to host
# check current python version
python -V
# install necessary dependencies
pip3 rich sh click
```

### Requirements

see [tool.poetry.dependencies](pyproject.toml)


### Tests

```shell
# create env
poetry shell
# setup deps
poetry install
# run tests
pytest
# run tests monitor
ptw 
```
