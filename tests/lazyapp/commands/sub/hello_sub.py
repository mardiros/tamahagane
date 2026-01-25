from typing import Literal

from tests.dummyapp import command_handler


@command_handler
def hello_sub(cmd: Literal["hello-sub"]) -> str:
    return "Hello Sub"
