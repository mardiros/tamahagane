"""
tamahagene scanner implementation
"""
import importlib
import pkgutil
from collections import defaultdict
from collections.abc import Callable
from types import ModuleType
from typing import Any, ClassVar, Generic, TypeVar

T = TypeVar("T")


class Scanner(Generic[T]):
    """
    Scan python modules, collect hooks, then callback.
    """
    collected_hooks: ClassVar[dict[str, set[Any]]] = defaultdict(set)
    registry: T

    def __init__(self, registry: T):
        self.registry = registry
        self.categories = {cat for cat in dir(registry) if not cat.startswith("_")}

    @classmethod
    def load_modules(cls, *modules: str | ModuleType) -> None:
        for mod in modules:
            if isinstance(mod, str):
                mod = importlib.import_module(mod)

            if hasattr(mod, "__path__"):  # if it's a package, recursive call
                for _, submodname, _ in pkgutil.iter_modules(mod.__path__):
                    fullname = f"{mod.__name__}.{submodname}"
                    submod = importlib.import_module(fullname)
                    cls.load_modules(submod)  # Recursive call

    def scan(self, *modules: str | ModuleType) -> None:
        self.load_modules(*modules)
        for category in self.categories:
            for hook in self.collected_hooks[category]:
                hook(self)

    @classmethod
    def attach(cls, callback: "CallbackHook", category: "KeyOfRegistry") -> None:
        cls.collected_hooks[category].add(callback)


KeyOfRegistry = str
CallbackHook = Callable[[Scanner[Any]], None]


def attach(callback: CallbackHook, category: KeyOfRegistry) -> None:
    """
    Attach a callback to a category while loading a module.

    This function preload the callback, arranged by their category.
    """
    Scanner.attach(callback, category)
