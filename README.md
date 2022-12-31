### Shell command in python

```shell
# copy docker_ps.py to host
# check current python version
python -V
# install necessary dependencies
pip3 rich sh  
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
