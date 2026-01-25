## 0.4.0 - Released on 2026-01-25
* APIBreak: Add the wrapped method as first parameter of tamahagane.attach method.
* Bugfix: A tamahagane.Scanner.scan() call will not load previously cached hook
  outside of the given module.
* Feature: tamahagane.Scanner.scan() support, module, absolute name and relative names.

## 0.3.0 - Released on 2026-01-25
* APIBreak: stop exposing the scanner in the callback, only the registry. 

## 0.2.0 - Released on 2026-01-25
* APIBreak: drop scan module directly, module name required.
* Add support of relative package.
* Add caching to avoid side effects on re-import.

## 0.1.1 - Released on 2026-01-25
* Initial Release

