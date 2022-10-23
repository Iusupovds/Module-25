import pytest
import uuid

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    rep = outcome.get_result()
    setattr(item, 'rep_' + rep.when, rep)
    return rep

@pytest.fixture
def Chrome(request, driver):

    browser = driver
    browser.set_window_size(1400, 1000)

    yield browser
    
