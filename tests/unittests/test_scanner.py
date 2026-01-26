import tamahagane as th
from tests.lazyapp import Cli, Registries


def test_scanner_ignore_package():
    cli = Cli()
    scanner = th.Scanner[Registries](Registries(cli=cli))
    scanner.scan("tests.lazyapp.commands", ignore=["tests.lazyapp.commands.ignoreme"])
    assert set(cli.commands.keys()) == {"hello-sub", "hello-world"}


def test_scanner_ignore_module():
    cli = Cli()
    scanner = th.Scanner[Registries](Registries(cli=cli))
    scanner.scan(
        "tests.lazyapp.commands", ignore=["tests.lazyapp.commands.ignoreme.wanted"]
    )
    assert set(cli.commands.keys()) == {"hello-sub", "hello-world"}


def test_scanner_ignore_all():
    cli = Cli()
    scanner = th.Scanner[Registries](Registries(cli=cli))
    scanner.scan("tests.lazyapp.commands", ignore=["tests.lazyapp.commands"])
    assert set(cli.commands.keys()) == set()


def test_scanner_ignore_relative():
    cli = Cli()
    scanner = th.Scanner[Registries](Registries(cli=cli))
    scanner.scan("tests.lazyapp.commands", ignore=[".ignoreme"])
    assert set(cli.commands.keys()) == {"hello-sub", "hello-world"}


def test_scan_twice():
    cli = Cli()
    scanner = th.Scanner[Registries](Registries(cli=cli))
    scanner.scan("tests.lazyapp.commands", ignore=["tests.lazyapp.commands.ignoreme"])
    assert set(cli.commands.keys()) == {"hello-sub", "hello-world"}
    scanner.scan("tests.lazyapp.commands")
    assert set(cli.commands.keys()) == {"hello-sub", "hello-world", "hello-wanted"}


def test_scanner_all():
    cli = Cli()
    scanner = th.Scanner[Registries](Registries(cli=cli))
    scanner.scan("tests.lazyapp.commands")
    assert set(cli.commands.keys()) == {"hello-sub", "hello-world", "hello-wanted"}
    assert cli.commands["hello-world"]("hello") == "Hello World"
    assert cli.commands["hello-sub"]("hello") == "Hello Sub"
    assert cli.commands["hello-wanted"]("hello") == "Hello Wanted"
