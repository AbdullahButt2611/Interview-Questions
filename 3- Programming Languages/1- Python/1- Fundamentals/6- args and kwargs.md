# `*args` and `**kwargs` in Python

`TCS` • `Accenture` • `Infosys` • `Cognizant` • `Capgemini`

## Question

What are `*args` and `**kwargs` in Python, and when would you use them?

<br><br>

## Answer

### The Core Idea

- Both let you write functions that accept a **flexible** number of arguments instead of a fixed list.
- The names `args` and `kwargs` are only a convention. What actually matters is the `*` (one star) and `**` (two stars).
- You could write `*things` and `**stuff` and it would behave exactly the same.

<br><br>

### `*args` (One Star): Extra Positional Arguments

Collects any leftover positional arguments into a **tuple**.

```python
def add_all(*args):
    print(args)          # a tuple
    return sum(args)

add_all(1, 2, 3)         # args is (1, 2, 3), returns 6
add_all(1, 2, 3, 4, 5)   # args is (1, 2, 3, 4, 5), returns 15
```

You call the function with as many values as you like, and they all land inside `args`.

<br><br>

### `**kwargs` (Two Stars): Extra Keyword Arguments

Collects any leftover keyword (named) arguments into a **dictionary**.

```python
def show_info(**kwargs):
    print(kwargs)        # a dict

show_info(name="Sara", age=30)
# {'name': 'Sara', 'age': 30}
```

Each `key=value` you pass becomes a key-value pair inside `kwargs`.

<br><br>

### Using Both Together

You can mix them, but the order in the function definition is fixed: normal parameters first, then `*args`, then `**kwargs`.

```python
def profile(role, *args, **kwargs):
    print("role:", role)
    print("args:", args)
    print("kwargs:", kwargs)

profile("admin", 1, 2, active=True, level=5)
# role: admin
# args: (1, 2)
# kwargs: {'active': True, 'level': 5}
```

<br><br>

### The Other Direction: Unpacking

The same stars also work when **calling** a function, where they do the reverse. They unpack a collection into separate arguments.

```python
def greet(a, b, c):
    print(a, b, c)

nums = [1, 2, 3]
greet(*nums)             # same as greet(1, 2, 3)

info = {"a": 1, "b": 2, "c": 3}
greet(**info)            # same as greet(a=1, b=2, c=3)
```

- `*` unpacks a list or tuple into positional arguments.
- `**` unpacks a dict into keyword arguments.

<br><br>

### Where You Actually Use Them

- Writing flexible functions when you do not know in advance how many inputs you will receive.
- Wrapper functions and decorators that accept anything and pass it straight through, usually with `func(*args, **kwargs)`.
- Extending or overriding a method while forwarding all arguments to the parent.

<br><br>

### Quick Summary

- `*args` gives extra positional arguments, arriving as a **tuple**.
- `**kwargs` gives extra keyword arguments, arriving as a **dict**.
- In a definition they **collect**. In a call they **unpack**.
- The stars are what matter, not the names.

<br><br>

## Different Ways to Ask This Question

- What are `*args` and `**kwargs` in Python?
- What is the difference between `*args` and `**kwargs`?
- Why are the names `args` and `kwargs` not actually required?
- What is the correct order of parameters when a function uses both?
- How do you use `*` and `**` to unpack a list or dictionary into function arguments?
- How are `*args` and `**kwargs` used in decorators or wrapper functions?
- Can you pass both positional and keyword arguments to the same function, and how?