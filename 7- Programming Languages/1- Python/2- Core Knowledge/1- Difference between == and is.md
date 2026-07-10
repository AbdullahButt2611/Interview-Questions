# Difference Between == and is in Python

`Accenture` • `TCS` • `Infosys` • `Wipro` • `Cognizant`

## Question

What is the difference between the `==` and `is` operators in Python, and when should each be used?

<br><br>

## Answer

### Quick Summary

- `==` checks **value equality**. Do the two objects hold the same data?
- `is` checks **identity**. Are the two variables the exact same object in memory?

<br><br>

### == (Value Equality)

- Compares the **contents** of two objects.
- Works by calling the `__eq__` method under the hood.
- Two completely separate objects can still be equal with `==` as long as their values match.

<br><br>

### is (Identity)

- Compares whether two variables point to the **same object** in memory.
- Every object has a unique identifier (its memory address), which you can inspect with the `id()` function.
- `a is b` is True only when `id(a) == id(b)`.

<br><br>

### Code Example

```python
# Initialize two lists with identical values
list_a = [1, 2, 3]
list_b = [1, 2, 3]
list_c = list_a

print(list_a == list_b)  # True:  the values are the same
print(list_a is list_b)  # False: they are different objects in memory
print(list_a is list_c)  # True:  both names point to the same object
```

- `list_a` and `list_b` hold equal data, so `==` is True.
- They were built separately, so they live at different addresses and `is` is False.
- `list_c` was assigned from `list_a`, so both names refer to one single object.

<br><br>

### Best Practices

- Use `==` for normal value comparisons (numbers, strings, lists, and other data structures where the content matters).
- Use `is` only for identity checks against singletons, most commonly `None`.
- Prefer `if val is None:` over `if val == None:`.
- Avoid `is` for comparing integers or strings, since that relies on interning and can give inconsistent results.

<br><br>

### Why None Uses is

- `None` is a singleton, meaning there is exactly one `None` object in the entire program.
- Checking identity against it is fast and unambiguous.
- It is also safer, because a class could override `__eq__` in a surprising way, but it cannot change object identity.

<br><br>

## Different Ways to Ask This Question

- What is the difference between `==` and `is` in Python?
- When should you use `is` instead of `==`?
- Why is `if x is None` preferred over `if x == None`?
- What does the `id()` function tell you, and how does `is` rely on it?
- Which method does the `==` operator call internally?
- Can two objects be equal with `==` but not identical with `is`? Give an example.