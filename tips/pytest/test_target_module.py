
import pytest


@pytest.fixture(scope='function')
def input_values():
    return {
        "a" : 1,
        "b" : 2,
    }
