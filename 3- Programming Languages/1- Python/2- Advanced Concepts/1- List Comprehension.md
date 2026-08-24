# List Comprehension

`Infosys` • `TCS` • `Wipro` • `HCL` • `Cognizant` • `Accenture`

## Question

What is list comprehension in Python?

- Give a simple example.
- How do you use `if-else` inside it?

<br><br>

## Answer

### What It Is

List comprehension is a short, one-line way to build a new list. Instead of writing a `for` loop with `.append()`, you describe the list you want in a single compact line.

<br><br>

### Basic Syntax

```python
new_list = [expression for item in iterable]
```

Read it left to right: for each `item` in the `iterable`, work out `expression`, and collect the results into a new list.

<br><br>

### A Simple Example

Say you want the squares of the numbers 0 to 4.

The long way (normal loop):

```python
squares = []
for n in range(5):
    squares.append(n * n)
# [0, 1, 4, 9, 16]
```

The same thing as a list comprehension:

```python
squares = [n * n for n in range(5)]
# [0, 1, 4, 9, 16]
```

Both give the same result. The second one is just shorter and easier to read once the pattern is familiar.

<br><br>

### Adding a Filter (if only)

You can add a plain `if` at the **end** to keep only some items:

```python
evens = [n for n in range(10) if n % 2 == 0]
# [0, 2, 4, 6, 8]
```

Only the numbers where `n % 2 == 0` (the even ones) make it into the list. The rest are dropped.

<br><br>

### Using if-else

An `if-else` goes in a different spot. It sits at the **front**, before the `for`. It does not drop anything. It only picks which value to use for each item.

```python
labels = ["even" if n % 2 == 0 else "odd" for n in range(6)]
# ['even', 'odd', 'even', 'odd', 'even', 'odd']
```

Nothing is removed here. Every number stays, but each one becomes either `"even"` or `"odd"`.

Why the different position? Because `"even" if n % 2 == 0 else "odd"` is just a normal value-producing expression, and the value always goes at the front of a comprehension.

<mark>A plain if goes at the end and filters items out. An if-else goes at the front and picks a value for every item.</mark>

<br><br>

### Quick Way to Remember

- `[expr for item in iterable if cond]` → keep or skip (filter).
- `[a if cond else b for item in iterable]` → always keep, pick `a` or `b`.

<br><br>

### Combining Both

You can do both at once: filter at the end and choose a value at the front.

```python
result = ["big" if n > 2 else "small" for n in range(6) if n % 2 == 0]
# n runs through 0, 2, 4 (odds filtered out), then each one is labeled
# ['small', 'small', 'big']
```

Here the trailing `if n % 2 == 0` keeps only the even numbers, and the front `if-else` labels each survivor.

<br><br>

## Related Questions

- What is the difference between a list comprehension and a normal for loop?
- What are dictionary and set comprehensions?
- What is a generator expression, and how is it different from a list comprehension?
- How do nested list comprehensions work (for example, flattening a 2D list)?
- When should you avoid list comprehensions for the sake of readability?
- How do `map()` and `filter()` compare with list comprehensions?