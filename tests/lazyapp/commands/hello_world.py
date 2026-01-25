from typing import Literal

from tests.lazyapp import command_handler


@command_handler
def hello_world(cmd: Literal["hello-world"]) -> str:
    return "Hello World"
