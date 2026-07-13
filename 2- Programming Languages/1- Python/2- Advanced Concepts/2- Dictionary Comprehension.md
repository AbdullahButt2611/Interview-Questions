# Dictionary Comprehension

`TCS` • `Infosys` • `Wipro` • `Cognizant` • `IBM` • `Accenture`

## Question

What is dictionary comprehension in Python?

- Give a simple example.
- Show how to build a dict from two lists using `zip()`.

<br><br>

## Answer

### What It Is

Dictionary comprehension is the same idea as list comprehension, but it builds a **dictionary** (key-value pairs) instead of a list. You describe the dict you want in one compact line instead of writing a loop that fills it in.

<br><br>

### Basic Syntax

```python
new_dict = {key: value for item in iterable}
```

The only visual change from a list comprehension is the curly braces `{}` and the `key: value` pair before the `for`.

<mark>The colon between key and value is what tells Python this is a dictionary, not a list or a set.</mark>

<br><br>

### A Simple Example

Say you want each number mapped to its square.

The long way (normal loop):

```python
squares = {}
for n in range(5):
    squares[n] = n * n
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

The same thing as a dictionary comprehension:

```python
squares = {n: n * n for n in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

Here `n` becomes the key and `n * n` becomes the value.

<br><br>

### Adding a Filter

Just like with lists, a trailing `if` keeps only some pairs:

```python
even_squares = {n: n * n for n in range(10) if n % 2 == 0}
# {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}
```

Only the even numbers make it in. The rest are skipped.

<br><br>

### Turning Two Lists into a Dict (zip)

This is one of the most common real uses. Pair up a list of keys with a list of values using `zip()`:

```python
keys = ["name", "age", "city"]
values = ["Sara", 30, "Dubai"]

person = {k: v for k, v in zip(keys, values)}
# {'name': 'Sara', 'age': 30, 'city': 'Dubai'}
```

`zip` walks both lists together and hands you one `k` and one `v` at a time, and each pair becomes one key-value entry.

<br><br>

### Quick Mental Model

- List comprehension → `[expr for item in iterable]` → gives a list.
- Dict comprehension → `{key: value for item in iterable}` → gives a dict.

The same `if` filter and `if-else` rules apply. The only real change is the braces and the `key: value` colon.

<br><br>

## Related Questions

- What is the difference between a list comprehension and a dictionary comprehension?
- What is a set comprehension, and how does it differ from a dict comprehension?
- How does `zip()` work, and what happens if the two lists have different lengths?
- Can you use `if-else` inside a dictionary comprehension?
- How would you swap the keys and values of an existing dictionary?
- Why is there no tuple comprehension in Python?