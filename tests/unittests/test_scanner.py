from collections.abc import Iterator

import pytest

import tamahagane as th
from tests.lazyapp import Cli, Registries


@pytest.fixture(autouse=True)
def clean() -> Iterator[None]:
    yield
    th.Scanner[Registries].clear_cache()


def test_scanner():
    cli = Cli()
    scanner = th.Scanner[Registries](Registries(cli=cli))
    scanner.scan("tests.lazyapp.commands")
    assert set(cli.commands.keys()) == {"hello-sub", "hello-world"}
    assert cli.commands["hello-world"]("hello") == "Hello World"


def test_scan_twice():
    cli = Cli()
    scanner = th.Scanner[Registries](Registries(cli=cli))
    scanner.scan("tests.lazyapp.commands")
    scanner.scan("tests.lazyapp.commands")
    assert set(cli.commands.keys()) == {"hello-sub", "hello-world"}
