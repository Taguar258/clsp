import pytest
from clsp import SelectionPrompt, select


@pytest.fixture
def sp():

    return SelectionPrompt([1, 2, 3, 23, 11, 5], rows=1, cutoff=0.15)


def basic_tests(sp):

    sp._navigate_menu(1)
    sp._refresh_currently_shown()
    sp._return_selection()
    selected = sp._return_placeholder

    assert selected.value == "2"
    assert selected.index == 1
    assert sp._current == 1
    assert sp._current_position == [1, 1]


def test_search(sp):

    print("Please search and select number '23'.")

    sp._search = "23"
    sp._refresh_currently_shown()
    sp._return_selection()
    selected = sp._return_placeholder

    assert selected.value == "23"
    assert selected.index == 3
    assert sp._current == 0
    assert sp._current_position == [0, 1]


if __name__ == "__main__":

    inp = [1, 2, 3, 23, 11, 5]

    out = select(inp)

    print(out, out.index)
