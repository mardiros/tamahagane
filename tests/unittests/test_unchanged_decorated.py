from tests.dummyapp.commands.hello_world import hello_world


def test_decorator_unalter():
    assert hello_world("hello-world") == "Hello World"
    assert hello_world.__name__ == "hello_world"
    assert hello_world.__qualname__ == "hello_world"
    assert hello_world.__module__ == "tests.dummyapp.commands.hello_world"
