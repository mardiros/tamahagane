import inspect
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, get_args

import tamahagane as th

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

    def callback(registry: Registries) -> None:
        argsspec = inspect.getfullargspec(wrapped)
        msg_type_literal = argsspec.annotations[argsspec.args[0]]
        msg_type = get_args(msg_type_literal)[0]
        registry.cli.add_listener(msg_type, wrapped)

    th.Scanner[Registries].attach(callback, category="cli")
    return wrapped
