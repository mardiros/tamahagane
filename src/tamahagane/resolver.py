import importlib
import inspect
from pathlib import Path
from types import ModuleType


def _strip_left_dots(s: str) -> tuple[str, int]:
    stripped_string = s.lstrip(".")
    num_stripped_dots = len(s) - len(stripped_string)
    return stripped_string, num_stripped_dots - 1


def _get_parent(pkg: str, num_parents: int) -> str:
    if num_parents == 0:
        return pkg
    segments = pkg.split(".")
    return ".".join(segments[:-num_parents])


def resolve_package(mod: ModuleType) -> ModuleType:
    """
    Return the
    [regular package](https://docs.python.org/3/glossary.html#term-regular-package)
    of a module or itself if it is the ini file of a package.

    """

    # Compiled package has no __file__ attribute, ModuleType declare it as NoneType
    if not hasattr(mod, "__file__") or mod.__file__ is None:
        return mod

    module_path = Path(mod.__file__)
    if module_path.name == "__init__.py":
        return mod

    parent_module_name = mod.__name__.rsplit(".", 1)[0]
    parent_module = importlib.import_module(parent_module_name)
    return parent_module


def resolve_maybe_relative(mod: str, stack_depth: int = 1) -> ModuleType:
    """
    Resolve a module, maybe relative to the stack frame and import it.

    :param mod: the module to import. starts with a dot if it is relative.
    :param stack_depth: relative to which module in the stack.
        used to do an api that call it instead of resolve the module directly.
    :return: the imported module
    """
    if mod.startswith("."):
        caller_module = inspect.getmodule(inspect.stack()[stack_depth][0])

        # we could do an assert here but caller_module could really be none ?
        parent_module = resolve_package(caller_module)  # type: ignore
        package = parent_module.__name__
        mod, count = _strip_left_dots(mod)
        package = _get_parent(package, count)
        mod = f"{package}.{mod}".rstrip(".")

    module = importlib.import_module(mod)
    return module
