# Metaprogramming in Python

`Amazon` • `Google` • `Microsoft`

## Question

What is metaprogramming in Python, and how does a framework like Django use it?

<br><br>

## Answer

### Simple Definition

- Metaprogramming means writing code that works on **other code**, instead of working on normal data like numbers and text.
- In one line: it is code that reads, changes, or builds other code while the program is running.

<br><br>

### The Key Idea in Python

- In Python, almost everything is an object, including functions and classes.
- Because a function is just an object, you can pass it into another function, change it, and return a new version of it.
- This "you can treat code like data" ability is what makes metaprogramming possible.

<br><br>

### The Most Common Example: Decorators

- A decorator is a function that takes another function and returns a **new function that wraps it**.
- The wrapper adds some behavior before or after the original function runs, without changing the original code.
- This is metaprogramming because the decorator works on a function, not on plain data.

<br><br>

### How Django Uses It: @login_required

Django protects pages using a decorator called `@login_required`. It checks whether a user is logged in before letting them see a page.

Here is a simple version of how it works:

```python
def login_required(view_func):
    def wrapper(request):
        if request.user.is_authenticated:   # is the user logged in?
            return view_func(request)        # yes: show the page
        return redirect_to_login()           # no:  send to the login page
    return wrapper
```

You use it on a view like this:

```python
@login_required
def dashboard(request):
    return "secret page"
```

What happens, step by step:

- Django runs `wrapper` first, not your `dashboard` function.
- `wrapper` checks if the user is logged in.
- If yes, it calls your real `dashboard` function.
- If no, it sends the user to the login page.

<br><br>

### Why This Counts as Metaprogramming

- `login_required` takes your `dashboard` function as input.
- It hands back a brand new function (`wrapper`) with extra behavior added.
- So it is a program adjusting another program, which is the heart of metaprogramming.
- (Note: `is_authenticated` is not the decorator. It is just the True or False check that the decorator uses.)

<br><br>

### Other Places You See It

- `@property`, `@staticmethod`, and `@classmethod` are all decorators.
- Django models and tools like Pydantic look at your classes and set up behavior for you automatically.
- `@dataclass` writes methods like `__init__` for you, based on the fields you define.

<br><br>

### Quick Summary

- Metaprogramming is code that works on other code.
- The everyday form is the decorator: a function that wraps another function.
- Django's `@login_required` is a real example. It wraps a view to add a login check.
- You use metaprogramming far more often than you actually write it.

<br><br>

## Different Ways to Ask This Question

- What is metaprogramming in Python?
- How does a decorator work, and why is it a form of metaprogramming?
- Explain how Django's `@login_required` decorator works under the hood.
- What does it mean to say functions in Python are first-class objects?
- Can you give a real-world example of metaprogramming in a framework?
- What is the difference between a decorator and a metaclass?