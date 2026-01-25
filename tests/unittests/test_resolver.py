import sys
from types import ModuleType

import pytest

import tests.dummyapp.commands
import tests.dummyapp.commands.hello_world
from tamahagane import resolver


@pytest.mark.parametrize(
    "input,expected",
    [
        pytest.param(
            tests.dummyapp.commands, tests.dummyapp.commands, id="regular package"
        ),
        pytest.param(
            tests.dummyapp.commands.hello_world,
            tests.dummyapp.commands,
            id="module",
        ),
        pytest.param(sys, sys, id="compiled package"),
    ],
)
def test_resolve_package(input: ModuleType, expected: ModuleType):
    assert resolver.resolve_package(input) is expected


@pytest.mark.parametrize(
    "input,expected",
    [
        pytest.param("tests.dummyapp", "tests.dummyapp", id="absolute"),
        pytest.param(".test_scanner", "tests.unittests.test_scanner", id="sibling"),
        pytest.param(".", "tests.unittests", id="parent"),
        pytest.param("..", "tests", id="ancestor"),
        pytest.param("..dummyapp", "tests.dummyapp", id="uncle"),
    ],
)
def test_resolve_maybe_relative(input: str, expected: str):
    mod = resolver.resolve_maybe_relative(input)
    assert mod.__name__ == expected
