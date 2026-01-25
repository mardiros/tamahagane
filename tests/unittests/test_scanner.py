import tamahagane as th
from tests.dummyapp import Cli, Registries
from tests.dummyapp.commands.hello_world import hello_world


def test_unmodified_handler():
    assert hello_world("hello") == "Hello World"


def test_scanner():
    cli = Cli()
    scanner = th.Scanner[Registries](Registries(cli=cli))
    scanner.scan("tests.dummyapp.commands")
    assert set(cli.commands.keys()) == {"hello-world"}
    assert cli.commands["hello-world"]("hello") == "Hello World"


def test_scan_twice():
    cli = Cli()
    scanner = th.Scanner[Registries](Registries(cli=cli))
    scanner.scan("tests.dummyapp.commands")
    scanner.scan("tests.dummyapp.commands")
    assert set(cli.commands.keys()) == {"hello-world"}
