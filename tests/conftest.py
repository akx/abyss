# -*- coding: utf-8 -*-

import logging
import os

import pytest

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def output_dir():
    return os.path.join(os.path.dirname(__file__), "output") + os.sep
