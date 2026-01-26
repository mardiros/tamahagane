# Tamahagane


[![Documentation](https://github.com/mardiros/tamahagane/actions/workflows/publish-doc.yml/badge.svg)](https://mardiros.github.io/tamahagane/)
[![Continuous Integration](https://github.com/mardiros/tamahagane/actions/workflows/tests.yml/badge.svg)](https://github.com/mardiros/tamahagane/actions/workflows/tests.yml)
[![Coverage Report](https://codecov.io/gh/mardiros/tamahagane/graph/badge.svg?token=DTpi73d7mf)](https://codecov.io/gh/mardiros/tamahagane)


Forge your application registries.

Tamahagane is a library designed for constructing application registries,
the essential foundation for building decoupled software architectures
and enabling unit testing on application handlers.

## Motivation

Tamahagane essentially serves as a modern alternative to Venusian,
fulfilling the same core functionality.

The decision to create a new library stems from Venusian's limitations:
it was originally built for Python 2, relies heavily on dynamic behavior,
and lacks type support.

Tamahagane reuse the same vocabular, a Scanner and an attach function,
but the API is not fully compatible, in order to get a simpler version.

## Usage

To use Tamahagane you need to create a registries class that hold
all registries your app may load. The definition of the registry
is free and depends of the usage.

```python
from dataclasses import dataclass

@dataclass
class Registries:
    app_registry: ...
```

After what, the registries is filled out using the scan of the application code.

```python
import tamahagane as th

scanner = th.Scanner[Registries](Registries(app_registry=...))
scanner.scan("app.service_handlers")
```

At this time, the `app.service_handlers` is a module, or a package containing
submodules, that will be recursibely loaded. It contains decorated function,
where the decorator has been created in the application code to create the
callback.

```python
from collections.abc import Callable
from typing import Any

import tamahagane as th


CommandHandler = Callable[..., Any]

def command_handler(wrapped: CommandHandler) -> CommandHandler:

    def callback(registries: Registries) -> None:
        registries.app_registry.do_something_with(wrapped, ...)

    th.attach(wrapped, callback, category="app_registry")
    return wrapped

```

Now, you have a command_handler decorator that can be used an be filled out an
application registry with the decorated method.

```python
@command_handler
def handle_stuff(...):
    ...
```

handle_stuff is **unmodified** by its decorator and is purely unit testable.
No overhead.

## Difference from Venusian

* Tamahagane does not have a onerror on the scan, it raises.
* Tamahagane only support list of string, or tuple of string on the `onignore`.
* Tamahagane does not have a category on the scan method, the categories are the
  attributes of the registry, nothing less, nothing more.
* Tamahagane does not support class decoration.

## Installation

Tamahagane is available on [PyPI](https://pypi.org/project/tamahagane/)

So you can installing using your favorite packaging tool, mine is uv:

```bash
uv add tamahagane
```

## See also

- Documentation - https://mardiros.github.io/tamahagane/
- Venusian - https://docs.pylonsproject.org/projects/venusian/en/
