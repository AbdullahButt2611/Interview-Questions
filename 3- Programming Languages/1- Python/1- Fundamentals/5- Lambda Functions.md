# Lambda Functions in Python

`TCS` • `Infosys` • `Wipro` • `Amazon` • `Arbisoft`

## Question

What is a lambda function in Python, and when should you use one?

<br><br>

## Answer

### What It Is

- A lambda is a small, anonymous function defined in a single line using the `lambda` keyword instead of `def`.
- "Anonymous" means it does not need a name. You write it inline, right where you need it.
- It is handy for short, throwaway operations where writing a full named function would be overkill.

<br><br>

### Syntax

```python
lambda arguments: expression
```

- After `lambda` come the arguments, just like a normal function's parameters.
- After the colon comes a single expression, whose result is returned automatically.

<br><br>

### Lambda vs a Regular Function

These two definitions do exactly the same thing:

```python
# Regular function
def add(x, y):
    return x + y

# Lambda version
add = lambda x, y: x + y

print(add(2, 3))   # 5
```

<br><br>

### Key Characteristics

- Can take any number of arguments, but holds only **one** expression.
- There is no `return` keyword. The expression's value is returned automatically.
- It is usually not given a name. You use it on the spot and then discard it.

<br><br>

### Common Use Cases

Lambdas shine when you need a quick throwaway function to pass into another function. The most common cases are with `sorted()`, `map()`, and `filter()`:

```python
# Sort a list of tuples by the second item
pairs = [(1, "b"), (2, "a"), (3, "c")]
pairs.sort(key=lambda p: p[1])   # sorts by the letter

# Square every number
squares = list(map(lambda x: x**2, [1, 2, 3]))   # [1, 4, 9]

# Keep only even numbers
evens = list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4]))   # [2, 4]
```

<br><br>

### Lambda vs def (When to Use Which)

- Use a **lambda** for a short, simple, one-off operation, especially as an argument to another function.
- Use a regular **def** when the logic is longer, needs multiple statements, or when a clear name makes the code easier to read.
- If you find yourself assigning a lambda to a variable just to reuse it, a normal `def` is usually the better choice.

<br><br>

## Different Ways to Ask This Question

- What is a lambda function in Python?
- What is the difference between a lambda function and a function defined with `def`?
- When would you use a lambda instead of a normal function?
- Can a lambda function contain multiple expressions or statements?
- How are lambda functions used with `map()`, `filter()`, and `sorted()`?
- Why are lambda functions called anonymous functions?
- What are the limitations of lambda functions?