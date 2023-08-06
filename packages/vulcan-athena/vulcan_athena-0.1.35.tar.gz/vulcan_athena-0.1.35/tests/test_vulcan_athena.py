#!/usr/bin/env python

"""Tests for `vulcan_athena` package."""

import pytest

from vulcan_athena.vulcan_athena import sqrt_function, say_hello


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_sqrt_with_param():
    assert sqrt_function(25) == 5


def test_helloworld_no_params():
    assert say_hello() == 'Welcome to Athena...'


def test_helloworld_with_param():
    assert say_hello("Everyone") == "Welcome to Athena, Everyone!"
