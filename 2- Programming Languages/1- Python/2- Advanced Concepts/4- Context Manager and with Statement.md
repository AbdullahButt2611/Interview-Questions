# Context Manager and the `with` Statement in Python

`Amazon` • `Google` • `Microsoft` • `Flipkart` • `TCS` • `Infosys` • `Wipro` • `Cognizant` • `Accenture` • `Capgemini`

## Question

What is a context manager in Python and how does the `with` statement work internally? Explain with an example and show how you would write your own context manager.

<br><br>

## Answer

### The Idea in One Line

A context manager is an object that knows two things:

- What to do **before** your block of code runs (setup)
- What to do **after** your block of code finishes (cleanup)

The `with` statement is the syntax that runs both of these for you, automatically.

<mark>The cleanup runs even if your code crashes in the middle. That single guarantee is the whole reason context managers exist.</mark>

<br><br>

### A Real Life Way to Remember It

Think of staying in a hotel room:

- You check in and get the key, this is `__enter__`
- You use the room, this is your code inside the `with` block
- You check out and hand back the key, this is `__exit__`
- Even if you rush out because of a fire alarm (an exception), the checkout still happens

Without a context manager, you are the person who walks out with the key still in your pocket. The room stays blocked for everyone else, which is exactly what a leaked file handle or an unclosed database connection looks like.

<br><br>

### The Problem: Life Without `with`

```python
f = open("data.txt", "r")
data = f.read()
f.close()
```

- If `f.read()` throws an error, `f.close()` never runs
- The file stays open, holding an OS level resource
- Do this in a loop enough times and the program dies with "too many open files"

The manual fix works but is noisy, and you have to remember it every single time:

```python
f = open("data.txt", "r")
try:
    data = f.read()
finally:
    f.close()
```

<br><br>

### The Same Thing With `with`

```python
with open("data.txt", "r") as f:
    data = f.read()

# file is already closed here, error or no error
```

The `try` / `finally` logic did not disappear. It was written once inside the object, so you never repeat it.

<br><br>

### What Python Actually Does Behind the Scenes

For an object to work with `with`, it must implement two dunder methods:

- `__enter__(self)` runs when the block starts, and whatever it returns is assigned to the variable after `as`
- `__exit__(self, exc_type, exc_value, traceback)` runs when the block ends, normally or because of an exception

So this:

```python
with open("data.txt") as f:
    data = f.read()
```

Is roughly translated by Python into this:

```python
mgr = open("data.txt")
f = mgr.__enter__()
try:
    data = f.read()
finally:
    mgr.__exit__(exc_type, exc_value, traceback)
```

<mark>`with` is not magic. It is just `try` / `finally` with the boilerplate moved into the object.</mark>

<br><br>

### Writing Your Own Context Manager (Class Way)

```python
class DBConnection:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"Opening connection to {self.name}")
        self.conn = f"conn_object_{self.name}"
        return self.conn                # this value goes to the "as" variable

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"Closing connection to {self.name}")
        self.conn = None
        return False                    # False means: do not hide the error


with DBConnection("orders_db") as conn:
    print("Running query on", conn)
    raise ValueError("query failed")
```

Dry run:

```ini
Opening connection to orders_db
Running query on conn_object_orders_db
Closing connection to orders_db        <- cleanup STILL ran
ValueError: query failed               <- error still reaches the caller
```

This is the behaviour interviewers look for. Cleanup happened, and the error was not silently eaten.