# Generators in Python

`Google` • `Meta` • `Stripe` • `Accenture` • `TCS` • `Infosys` • `Wipro` • `Cognizant` • `IBM`

## Question

What are generators in Python? How do we use them?

<br><br>

## Answer

### What is a Generator

- A generator is a **special function that produces values one at a time**, instead of building and returning them all at once.
- It is written like a normal function, but it uses the `yield` keyword instead of `return`.
- Calling a generator function does **not** run the body. It immediately returns a **generator object** (which is an iterator).
- The body runs only when you ask for the next value (via `next()` or a `for` loop).
- Each `yield` **pauses** the function, hands the value back to the caller, and **remembers the entire local state** (variables, instruction pointer).
- On the next request, execution **resumes right after the `yield`**, not from the top.

<mark>A generator is lazy (it computes on demand) and stateful (it remembers where it paused).</mark>

<br><br>

### Why Generators Exist

The core problem they solve is **memory**.

- A normal function that returns a list of 10 million items must hold all 10 million in RAM.
- A generator holds only the **current item plus a few local variables**, so memory is O(1) instead of O(n).
- They also allow **infinite sequences**, which a list can never represent.
- They give you **faster time to first result**, since you do not wait for the whole collection to be built.

<br><br>

### How to Create Them

**1. Generator function (using `yield`)**

```python
def squares(n):
    for i in range(n):
        yield i ** 2

gen = squares(5)          # nothing has executed yet
print(next(gen))          # 0
print(next(gen))          # 1

for value in squares(5):  # 0 1 4 9 16
    print(value)
```

**2. Generator expression (lightweight, inline)**

```python
squares_gen = (i ** 2 for i in range(5))   # generator, lazy, parentheses
squares_list = [i ** 2 for i in range(5)]  # list, eager, square brackets

print(sum(i ** 2 for i in range(1000000)))  # no intermediate list is built
```

**3. Infinite generator**

```python
def fibonacci():
    a, b = 0, 1
    while True:          # safe, because values are produced on demand
        yield a
        a, b = b, a + b

fib = fibonacci()
print([next(fib) for _ in range(8)])   # [0, 1, 1, 2, 3, 5, 8, 13]
```

<br><br>

### How Execution Actually Flows

```ini
def counter():
    print("start")
    yield 1
    print("middle")
    yield 2
    print("end")

c = counter()        -> function body does NOT run, generator object created
next(c)              -> prints "start",  pauses at yield 1, returns 1
next(c)              -> prints "middle", pauses at yield 2, returns 2
next(c)              -> prints "end",    body finishes, raises StopIteration
```

- The `for` loop catches `StopIteration` internally, which is why you never see it in normal usage.

<br><br>

### Generator vs Normal Function

- **Return keyword:** normal function uses `return`, generator uses `yield`.
- **Execution:** normal function runs fully on call, generator runs only on demand.
- **State:** normal function loses its local state on return, generator preserves it between yields.
- **Output:** normal function gives one final value, generator gives a stream of values.
- **Memory:** normal function may hold the whole result set, generator holds one item at a time.

<br><br>

### Generator vs List Comprehension

- **Memory:** generator is lazy (O(1) space), list comprehension is eager (O(n) space).
- **Reusability:** a list can be iterated many times, a **generator is single use** and is exhausted after one pass.
- **Indexing:** a list supports `lst[3]` and `len(lst)`, a generator supports **neither**.
- **Speed:** the generator wins when you only need part of the data, or when you are chaining pipelines.

<mark>Once a generator is exhausted, it stays exhausted. Re-iterating it silently yields nothing, and this is a very common interview trap.</mark>

<br><br>

### Advanced Tools You Should Mention

**`yield from` (delegating to a sub generator)**

```python
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)   # cleaner than looping and re-yielding
        else:
            yield item

print(list(flatten([1, [2, [3, 4]], 5])))   # [1, 2, 3, 4, 5]
```

**`send()`, `close()`, `throw()`**

- `gen.send(value)` resumes the generator and **pushes a value back into it** (the `yield` expression evaluates to that value).
- `gen.close()` stops the generator and triggers cleanup in a `finally` block.
- `gen.throw(Exc)` raises an exception at the paused point.
- These make generators the foundation of **coroutines**, which is what `async` and `await` were built on top of.

<br><br>

### Real World Use Cases

- **Reading huge files line by line** without loading the file into memory.
- **Streaming ETL and data pipelines**, where each stage yields into the next.
- **Paginated API calls**, yielding records page by page.
- **Infinite or unbounded sequences** (IDs, timestamps, sensor readings).
- **Chained transformations**, where filtering and mapping stay lazy end to end.

```python
def read_large_file(path):
    with open(path) as f:
        for line in f:              # file objects are already lazy
            yield line.strip()

errors = (line for line in read_large_file("app.log") if "ERROR" in line)

for err in errors:                  # only one line in memory at any moment
    print(err)
```

<br><br>

### Key Gotchas

- Calling the generator function does **not** execute it. Forgetting this is a classic bug.
- A generator **cannot be rewound**. To iterate twice, call the generator function again.
- `len()` does not work on a generator. Use `sum(1 for _ in gen)` if you truly need a count (this also consumes it).
- Mixing `return` inside a generator does not return a value to the loop. It just raises `StopIteration`.
- Every generator is an iterator, but **not every iterator is a generator**. An iterator is any object implementing `__iter__` and `__next__`, while a generator gets both for free.

<br><br>

## Related Questions

- What is the difference between an iterable, an iterator, and a generator?
- How do `__iter__` and `__next__` work, and how would you build a custom iterator class?
- What is the difference between `yield` and `return`?
- What does `yield from` do and when would you use it?
- How would you read a 50 GB file in Python without running out of memory?
- What are decorators, and how do they compare to generators as a language feature?
- How do generators relate to coroutines, `async`, and `await`?
- What are the memory and performance trade offs between a list comprehension and a generator expression?
- What happens if you call `next()` on an exhausted generator?
- What is the `itertools` module and which functions do you use most (`islice`, `chain`, `count`, `groupby`)?