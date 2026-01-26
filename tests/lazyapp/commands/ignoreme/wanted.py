from typing import Literal

from tests.dummyapp import command_handler


@command_handler
def hello_wanted(cmd: Literal["hello-wanted"]) -> str:
    return "Hello Wanted"
