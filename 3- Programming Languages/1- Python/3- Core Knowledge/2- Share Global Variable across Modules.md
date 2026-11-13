# Share Global Variables Across Modules

## Question

Explain how to share global variables across multiple modules in a single Python program.

- What mechanism makes this possible?
- What is the common mistake that quietly breaks it?

<br><br>

## Answer

### The Config Module Pattern

The standard approach is to keep shared state in its own module and have every other module import that module.

- Put the shared state in a dedicated module (commonly `config.py`, `settings.py`, or `globals.py`).
- Every module that needs the state runs `import config`.
- All reads and writes go through the module name (for example, `config.counter`).

```python
# config.py
counter = 0
settings = {}
```

```python
# writer.py
import config

def bump():
    config.counter += 1
    config.settings["ready"] = True
```

```python
# main.py
import config
import writer

writer.bump()
print(config.counter)    # 1
print(config.settings)   # {'ready': True}
```

Everyone touches the same `config` object, so the values stay in sync.

<br><br>

### Why This Works

- Python creates only one object per imported module and caches it in `sys.modules`.
- The first `import config` runs the file once and saves the result.
- Every later `import config` (from any file) gets that same cached object.
- So there is only one `config` in memory, shared by all files.

<mark>Any attribute you set on the shared module is visible everywhere that module is imported.</mark>

<br><br>

### The Common Pitfall

This does not share state the way you might expect:

```python
from config import counter   # copies the current value into a new local name
counter += 1                 # rebinds the LOCAL name only, config.counter is unchanged
```

- `from config import counter` binds a brand new name pointing at whatever value existed at import time.
- Rebinding that local name does not touch `config.counter`.
- If someone else updates `config.counter`, your local `counter` still points at the old value.

The rule of thumb: always `import config` and go through `config.x`, never `from config import x`.

<br><br>

### Mutable Objects (A Partial Exception)

- With `from config import settings`, mutating the object (`settings["x"] = 1`) does work, because you are changing the shared object rather than rebinding the name.
- Rebinding it (`settings = {}`) still will not propagate to other modules.
- Accessing through the module (`config.settings`) stays consistent in every case, so it is the safer habit.

<br><br>

### Other Approaches

- A class holding class attributes.
- A single shared object (a singleton instance).
- Passing a shared dict or object explicitly as a function argument.

The dedicated config module remains the most common Pythonic choice for most situations.