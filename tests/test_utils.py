import re

import pytest

from tests.conftest import test_pair
from text_obfuscator.utils import Utils

to_test_get_arg_keys = [
    test_pair(input="", expected=[]),
    test_pair(input="no variables", expected=[]),
    test_pair(input="{a} {b} {c}", expected=["a", "b", "c"]),
    test_pair(input="{a}{b}", expected=["a", "b"]),
]


@pytest.mark.parametrize("test", to_test_get_arg_keys)
def test_get_arg_keys(test: test_pair):
    """Test function `get_arg_keys`."""
    output = Utils.get_arg_keys(test.input)
    assert output == test.expected


to_test_extra_args = [
    test_pair(
        input=(re.compile(r"(\{.*?})"), "the question is {answer}"),
        expected=(
            "the question is         ",
            [
                ("{answer}", (16, 24)),
            ],
        ),
    ),
    test_pair(
        input=(re.compile(r"(\{.*?})"), "The answer to {everything} is {key}"),
        expected=(
            "The answer to              is      ",
            [
                ("{everything}", (14, 26)),
                ("{key}", (30, 35)),
            ],
        ),
    ),
]


@pytest.mark.parametrize("test", to_test_extra_args)
def test_extra_args(test: test_pair):
    """Test function `extra_args`."""
    output = Utils.extra_args(*test.input)
    assert output == test.expected


to_test_put_back_key_args = [
    test_pair(
        input=(
            "Today is          ",
            [
                ("{holiday}", (9, 19)),
            ],
        ),
        expected="Today is {holiday}",
    ),
    test_pair(
        input=(
            "The answer to              is      ",
            [
                ("{everything}", (14, 26)),
                ("{key}", (30, 35)),
            ],
        ),
        expected="The answer to {everything} is {key}",
    ),
]


@pytest.mark.parametrize("test", to_test_put_back_key_args)
def test_put_back_key_args(test: test_pair):
    """Test function `put_back_key_args`."""
    output = Utils.put_back_key_args(*test.input)
    assert output == test.expected
