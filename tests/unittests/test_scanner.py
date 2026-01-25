import tamahagane as th
from tests.lazyapp import Cli, Registries


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
