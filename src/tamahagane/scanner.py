"""
tamahagene scanner implementation
"""

import pkgutil
import sys
from collections import defaultdict
from collections.abc import Callable
from types import ModuleType
from typing import Any, ClassVar, Generic, TypeVar

from tamahagane.resolver import resolve_maybe_relative

T = TypeVar("T")
KeyOfRegistry = str
CallbackHook = Callable[[T], None]


class Scanner(Generic[T]):
    """
    Scan python modules, collect hooks, then callback.
    """

    collected_hooks: ClassVar[dict[str, set[Any]]] = defaultdict(set)
    registry: T
    loaded_mods: ClassVar[set[ModuleType]] = set()

    def __init__(self, registry: T):
        self.registry = registry
        self.categories = {cat for cat in dir(registry) if not cat.startswith("_")}

    @classmethod
    def load_modules(cls, *modules: ModuleType | str, depth: int) -> None:
        for mod in modules:
            if isinstance(mod, str):
                mod = resolve_maybe_relative(mod, depth)
            if mod in cls.loaded_mods:
                continue
            cls.loaded_mods.add(mod)

            if hasattr(mod, "__path__"):  # if it's a package, recursive call
                for _, submodname, _ in pkgutil.iter_modules(mod.__path__):
                    fullname = f"{mod.__name__}.{submodname}"
                    cls.load_modules(fullname, depth=depth + 1)  # Recursive call

    def scan(self, *modules: ModuleType | str, stack_depth: int = 1) -> None:
        """
        Scan modules from the given parameter.


        :param modules: modules are absolute or relative if the starts with a dot.
        :param stack_depth: in case of relative package, speficy from what the package
            is relative too.
            If you expose a scan method in a framework, the depth of the stack frame
            must be updated in order to get it relative to the appropriate caller.
        """
        self.load_modules(*modules, depth=stack_depth)
        for category in self.categories:
            for hook in self.collected_hooks[category]:
                hook(self.registry)

    @classmethod
    def attach(cls, callback: CallbackHook[T], category: KeyOfRegistry) -> None:
        """
        Attach method from the scanner.

        This is a more verbose way to attach a callback, with better typing support.
        """
        cls.collected_hooks[category].add(callback)

    @classmethod
    def clear_cache(cls) -> None:
        """
        Clear the scanning cache.

        This method allows to clear the loading cache, for testing purpose.
        """
        for mod in cls.loaded_mods:
            if mod.__name__ in sys.modules:
                del sys.modules[mod.__name__]
        cls.loaded_mods.clear()
        # for funcs in cls.collected_hooks.values():
        #     for func in funcs:
        #         if func.__module__ in sys.modules:
        #             del sys.modules[func.__module__]
        cls.collected_hooks.clear()


def attach(callback: CallbackHook[Any], category: KeyOfRegistry) -> None:
    """
    Attach a callback to a category while loading a module.

    This function preload the callback, arranged by their category.

    :param callback: the callback to call when the scan is called.
    :param category: an attribute of the registry, if the registry does not have
        an attribute that matche the category, the category will callback
        will never be loaded.
    """
    Scanner[Any].attach(callback, category)
