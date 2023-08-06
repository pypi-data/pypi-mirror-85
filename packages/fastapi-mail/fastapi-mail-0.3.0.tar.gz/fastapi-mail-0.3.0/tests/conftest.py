import pytest


@pytest.fixture
def temp_data():
    temp = [
        'str',
        'string',
        'int',
        'integer',
        'biginteger',
        'float',
        'datetime',
        'date',
        'timestamp',
        'varchar']
    return temp