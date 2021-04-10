import pytest
from clsp import SelectionPrompt


@pytest.fixture
def sp():

    return SelectionPrompt([1, 2, 3, 23, 11, 5])
