import pytest
import saltext.tidx1.states.tidx1_mod as tidx1_module


@pytest.fixture
def configure_loader_modules():
    module_globals = {"__salt__": {"this_does_not_exist.please_replace_it": lambda: True}}
    return {tidx1_module: module_globals}


def test_replace_this_this_with_something_meaningful():
    assert "this_does_not_exist.please_replace_it" in tidx1_module.__salt__
    assert tidx1_module.__salt__["this_does_not_exist.please_replace_it"]() is True
