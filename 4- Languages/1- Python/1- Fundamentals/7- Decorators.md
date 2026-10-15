# Decorators in Python

`TCS` • `Accenture` • `Cognizant` • `Infosys` • `Wipro`

## Question

What are decorators in Python, and how do they work?

<br><br>

## Answer

### Simple Definition

- A decorator is a function that takes another function and returns a **new function that adds behavior around it**.
- It does this without changing the original function's own code.

<br><br>

### The Key Idea

- In Python, functions are just objects. You can pass a function into another function, and you can return a function.
- A decorator uses both of these ideas: it accepts a function and hands back a wrapped version of it.

<br><br>

### A Basic Decorator

```python
def my_decorator(func):
    def wrapper():
        print("before the function runs")
        func()                       # call the original
        print("after the function runs")
    return wrapper
```

- `my_decorator` takes a function as input.
- It wraps that function inside `wrapper`, which adds a print before and after.
- It returns the `wrapper`.

<br><br>

### Using It

You could apply it by hand:

```python
def say_hello():
    print("Hello!")

say_hello = my_decorator(say_hello)
say_hello()
```

Python gives you the `@` symbol as a shortcut that does exactly the same thing:

```python
@my_decorator
def say_hello():
    print("Hello!")

say_hello()
```

Output:

```
before the function runs
Hello!
after the function runs
```

So `@my_decorator` above a function just means "replace this function with `my_decorator(function)`."

<br><br>

### Making It Work for Any Function

The basic wrapper only works for functions that take no arguments. To handle **any** function, the wrapper accepts and forwards arguments using `*args` and `**kwargs`:

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)                     # keep the original name and info
    def wrapper(*args, **kwargs):
        print("before")
        result = func(*args, **kwargs)
        print("after")
        return result                # pass the real return value back
    return wrapper
```

- `return result` makes sure the original function's return value is not thrown away.
- `@wraps(func)` copies the original function's name and docstring onto the wrapper, so debugging tools do not just see "wrapper" everywhere.

<br><br>

### Where Decorators Are Used

- Authentication and permission checks, like `@login_required`.
- Logging, or timing how long a function takes.
- Caching results, like `@functools.lru_cache`.
- Registering routes in web frameworks, like `@app.route("/")` in Flask.
- Built-ins like `@property`, `@staticmethod`, and `@classmethod`.

<br><br>

### Quick Summary

- A decorator wraps a function to add behavior before, after, or around it.
- `@decorator` is just a clean shortcut for "replace this function with a wrapped version."
- The wrapper usually uses `*args` and `**kwargs` so it works on any function.

<br><br>

## Different Ways to Ask This Question

- What are decorators in Python?
- How does a decorator work under the hood?
- What does the `@` symbol actually do?
- Why do decorators use `*args` and `**kwargs` in the wrapper?
- What is the purpose of `functools.wraps` in a decorator?
- Can you write a decorator that logs or times a function?
- What is the difference between a decorator and a metaclass?