import inspect
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal, get_args

import tamahagane as th

Categories = Literal["cli"]

Listener = Callable[..., Any]


class Cli:
    commands: dict[str, Listener]

    def __init__(self) -> None:
        self.commands = {}

    def add_listener(self, msg_type: str, hook: Listener):
        self.commands[msg_type] = hook


@dataclass
class Registries:
    cli: Cli


def command_handler(wrapped: Listener) -> Listener:
    """
    Decorator to listen for a command or an event.
    """

    def callback(scanner: th.Scanner[Registries]) -> None:
        argsspec = inspect.getfullargspec(wrapped)
        msg_type_literal = argsspec.annotations[argsspec.args[0]]
        msg_type = get_args(msg_type_literal)[0]
        scanner.registry.cli.add_listener(msg_type, wrapped)

    th.attach(callback, category="cli")
    return wrapped
