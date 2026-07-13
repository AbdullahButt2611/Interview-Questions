# Exception Groups in Python

`TCS` • `Wipro` • `Infosys` • `IBM`

## Question

What are exception groups in Python, what problem do they solve, and how are they used?

<br><br>

## Answer

### The Core Idea

- Normally, Python can raise only **one** exception at a time.
- Exception groups (added in Python 3.11) let you bundle **multiple** exceptions together and raise them as a single object.
- Think of it as a box. Instead of handing over one error, you hand over a box that holds several errors, so none of them get lost.

<br><br>

### Why They Were Added

- Some situations produce many independent failures at the same time (for example, running several tasks in parallel).
- With normal exceptions, only the first failure surfaces and the rest disappear silently.
- Exception groups fix this by carrying every failure up together.

<br><br>

### How to Create One

You pass a message and a list of exceptions:

```python
raise ExceptionGroup(
    "some things failed",
    [ValueError("wrong value"), TypeError("wrong type")]
)
```

- The first argument is a description label for the group.
- The second argument is the list of actual exceptions stored inside it.

<br><br>

### How to Catch One (except*)

Use the new `except*` syntax (with a star) to look inside the group:

```python
try:
    raise ExceptionGroup("failed", [ValueError("v"), TypeError("t")])
except* ValueError:
    print("caught the value error")
except* TypeError:
    print("caught the type error")
```

- With a normal `except`, only the **first** matching block runs.
- With `except*`, **each** matching block runs, one per error type.
- Any errors that no block matches keep propagating as a leftover group.

<br><br>

### ExceptionGroup vs BaseExceptionGroup

- `ExceptionGroup` is used when every error inside is a normal `Exception`.
- `BaseExceptionGroup` is used automatically when the group contains system-level exceptions (like `KeyboardInterrupt` or `SystemExit`).

<br><br>

### Useful Attributes and Methods

- `.exceptions` gives the tuple of errors held inside the group.
- `.message` gives the group's description text.
- `.subgroup(...)` returns only the errors matching a condition (or None if none match).
- `.split(...)` returns a pair of groups (matching group, non-matching group).

<br><br>

### Where You Meet Them in Real Code

- Mostly with `asyncio.TaskGroup`, where many tasks run together and more than one can fail at once.
- Also useful for batch validation (collecting all errors together) and parsing input that has multiple issues.

<br><br>

## Different Ways to Ask This Question

- What are exception groups and why were they added to Python?
- What problem do exception groups solve?
- What is the difference between `except` and `except*`?
- Why can a normal `except` block not catch an exception that sits inside a group?
- How does `asyncio.TaskGroup` report failures when several tasks fail at once?
- You have 10 concurrent API calls and 3 of them fail. How do you surface all 3 errors?
- When do you get `BaseExceptionGroup` instead of `ExceptionGroup`?
- What do `.split()` and `.subgroup()` do on an exception group?
- Can exception groups be nested, and how does `except*` handle the nesting?