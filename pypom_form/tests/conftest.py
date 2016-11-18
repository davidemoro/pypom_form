import pytest


@pytest.fixture
def browser():
    import mock
    browser = mock.MagicMock()

    from zope.interface import alsoProvides
    from pypom.splinter_driver import ISplinter
    alsoProvides(browser, ISplinter)
    return browser
