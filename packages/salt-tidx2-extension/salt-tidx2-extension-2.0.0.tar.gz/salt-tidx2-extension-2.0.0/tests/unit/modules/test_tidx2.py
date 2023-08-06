import pytest
import saltext.tidx2.modules.tidx2_mod as tidx2_module


@pytest.fixture
def configure_loader_modules():
    module_globals = {"__salt__": {"this_does_not_exist.please_replace_it": lambda: True}}
    return {tidx2_module: module_globals}


def test_replace_this_this_with_something_meaningful():
    assert "this_does_not_exist.please_replace_it" in tidx2_module.__salt__
    assert tidx2_module.__salt__["this_does_not_exist.please_replace_it"]() is True
