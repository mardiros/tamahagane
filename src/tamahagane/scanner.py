"""
tamahagene scanner implementation
"""

import importlib
import pkgutil
from collections import defaultdict
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from types import ModuleType
from typing import Any, ClassVar, Generic, TypeVar

from tamahagane.resolver import resolve_maybe_relative

__all__ = [
    "T",
    "KeyOfRegistry",
    "CallbackHook",
    "RegisteredFn",
    "CallbackInfo",
    "Scanner",
    "attach",
]


T = TypeVar("T")
"""Represent the final registry to forge."""

KeyOfRegistry = str
"""Represent a valid attribute of the registry T."""

CallbackHook = Callable[[T], None]
"""Callback hook."""

RegisteredFn = Callable[..., Any]
"""Represent the decorated method that will be hooked in the registry after a scan."""


@dataclass
class CallbackInfo:
    """Store information at import time to fillout registries during the scan."""
    fn: RegisteredFn
    """The decorated method."""
    callback: CallbackHook[Any]
    """Its inner callback method."""


class Scanner(Generic[T]):
    """
    Scan python modules, collect hooks, then callback.
    """

    collected_hooks: ClassVar[dict[str, list[CallbackInfo]]] = defaultdict(list)
    registry: T
    loaded_mods: ClassVar[set[ModuleType]] = set()

    def __init__(self, registry: T):
        """
        Initialize the scanner for the given registry.

        :param registry: application registry contains attributes of registry to scan.
            The attributes act as the category to filters at scanning.
        """
        self.registry = registry
        self.categories = {cat for cat in dir(registry) if not cat.startswith("_")}

    @classmethod
    def load_modules(cls, *modules: ModuleType, ignore: Sequence[str] = ()) -> None:
        for mod in modules:
            if mod.__name__ in ignore:
                continue
            if mod in cls.loaded_mods:
                continue
            cls.loaded_mods.add(mod)

            if hasattr(mod, "__path__"):  # if it's a package, recursive call
                for _, submodname, _ in pkgutil.iter_modules(mod.__path__):
                    fullname = f"{mod.__name__}.{submodname}"
                    # take care, we still preload modules that may be excluded
                    # as hook here because we cache loaded modules to avoid
                    # recursive call to be done many times.
                    submod = importlib.import_module(fullname)
                    cls.load_modules(submod)  # Recursive call

    def scan(
        self,
        *modules: ModuleType | str,
        stack_depth: int = 1,
        ignore: Sequence[str] = (),
    ) -> None:
        """
        Scan modules from the given parameter.


        :param modules: modules are absolute or relative if the starts with a dot.
        :param stack_depth: in case of relative package, speficy from what the package
            is relative too.
            If you expose a scan method in a framework, the depth of the stack frame
            must be updated in order to get it relative to the appropriate caller.
        """
        mods = [
            resolve_maybe_relative(mod, stack_depth) if isinstance(mod, str) else mod
            for mod in modules
        ]
        mod_names = [mod.__name__ for mod in mods]
        if isinstance(ignore, str):
            ignore = [ignore]
        absolute_ignore: list[str] = []
        for ign in ignore:
            if ign.startswith("."):
                absolute_ignore.extend([f"{mod}{ign}" for mod in mod_names])
            else:
                absolute_ignore.append(ign)

        # we don't load the module ignored in the cache
        self.load_modules(*mods, ignore=absolute_ignore)

        def match_(hook: CallbackInfo) -> bool:
            for excl in absolute_ignore:
                if hook.fn.__module__ == excl:
                    return False
                if hook.fn.__module__.startswith(f"{excl}."):
                    return False
            for mod in mod_names:
                if hook.fn.__module__.startswith(mod):
                    return True
            return False

        for category in self.categories:
            for hook in self.collected_hooks[category]:
                if match_(hook):
                    hook.callback(self.registry)

    @classmethod
    def attach(
        cls, wrapped: RegisteredFn, callback: CallbackHook[T], category: KeyOfRegistry
    ) -> None:
        """
        Attach method from the scanner.

        This is a more verbose way to attach a callback, with better typing support.
        """
        cls.collected_hooks[category].append(CallbackInfo(wrapped, callback))


def attach(
    wrapped: RegisteredFn, callback: CallbackHook[Any], category: KeyOfRegistry
) -> None:
    """
    Attach a callback to a category while loading a module.

    This function preload the callback, arranged by their category.

    :param callback: the callback to call when the scan is called.
    :param category: an attribute of the registry, if the registry does not have
        an attribute that matche the category, the category will callback
        will never be loaded.
    """
    Scanner[Any].attach(wrapped, callback, category)
