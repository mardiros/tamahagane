from collections.abc import Sequence

import pytest

import tamahagane as th
from tests.lazyapp import Cli, Registries


@pytest.mark.parametrize(
    "scanmod,ignore,expected",
    [
        pytest.param(
            ["tests.lazyapp.commands"],
            ["tests.lazyapp.commands.ignoreme"],
            {"hello-sub", "hello-world"},
            id="regular package / exclude packge",
        ),
        pytest.param(
            ["tests.lazyapp.commands"],
            ["tests.lazyapp.commands.ignoreme.wanted"],
            {"hello-sub", "hello-world"},
            id="regular package / exclude module",
        ),
        pytest.param(
            ["tests.lazyapp.commands"],
            "tests.lazyapp.commands.ignoreme.wanted",
            {"hello-sub", "hello-world"},
            id="ignore one string",
        ),
        pytest.param(
            ["tests.lazyapp.commands"],
            ["tests.lazyapp.commands"],
            set[str](),
            id="ignore all",
        ),
        pytest.param(
            ["tests.lazyapp.commands"],
            [".ignoreme"],
            {"hello-sub", "hello-world"},
            id="ignore relative",
        ),
        pytest.param(
            ["tests.lazyapp.commands"],
            [],
            {"hello-sub", "hello-world", "hello-wanted"},
            id="all",
        ),
    ],
)
def test_scanner_ignore(scanmod: list[str], ignore: Sequence[str], expected: set[str]):
    cli = Cli()
    scanner = th.Scanner[Registries](Registries(cli=cli))
    scanner.scan(*scanmod, ignore=ignore)
    assert set(cli.commands.keys()) == expected


def test_scan_twice():
    cli = Cli()
    scanner = th.Scanner[Registries](Registries(cli=cli))
    scanner.scan("tests.lazyapp.commands", ignore=["tests.lazyapp.commands.ignoreme"])
    assert set(cli.commands.keys()) == {"hello-sub", "hello-world"}
    scanner.scan("tests.lazyapp.commands")
    assert set(cli.commands.keys()) == {"hello-sub", "hello-world", "hello-wanted"}
