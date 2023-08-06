import os
import sys

from assertpy import assert_that

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../rabbitmqbaselibrary')))

from __version__ import VERSION  # noqa: E402


def test_version() -> None:
    assert_that(VERSION).is_equal_to('0.8.9')
