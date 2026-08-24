# Strategies to Optimize Memory Usage in Python

`Amazon` • `Google` • `Meta` • `Microsoft` • `Netflix` • `Uber` • `JPMorgan Chase` • `Infosys` • `TCS`

## Question

What strategies can be employed to optimize memory usage in Python?

<br><br>

## Answer

### 1. Use Generators Instead of Lists

- A list builds every item and holds all of them in memory at once
- A generator produces one item at a time and forgets it after use
- Memory stays almost flat no matter how big the data is

```python
squares = [x * x for x in range(10_000_000)]   # heavy, all in memory
squares = (x * x for x in range(10_000_000))   # light, one at a time
```

<br><br>

### 2. Read Large Files in Chunks

- Never call `file.read()` or `readlines()` on a large file, it loads the whole thing
- Loop over the file object instead, which reads line by line
- For CSVs, pandas supports a `chunksize` argument to process the file in pieces

```python
with open("big.log") as f:
    for line in f:          # one line in memory at a time
        process(line)
```

<br><br>

### 3. Use `__slots__` in Classes

- By default every object carries a `__dict__` to store its attributes, which is costly
- `__slots__` fixes the attribute list in advance and removes that dictionary
- Saves a large amount of memory when you create millions of small objects

```python
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y
```

<br><br>

### 4. Pick the Right Data Structure

- Use a **tuple** instead of a list when the data never changes, it is smaller
- Use a **set** or **dict** for lookups instead of scanning a big list
- Use `array.array` or **NumPy** arrays for large numeric data instead of Python lists
- Use `collections.deque` when you only add and remove from the ends

<mark>A Python list of one million integers stores one million full objects. A NumPy array stores raw numbers, so it can use several times less memory.</mark>

<br><br>

### 5. Avoid Making Unnecessary Copies

- Slicing a list or a string creates a brand new copy
- Prefer in place operations and views over building new objects
- `itertools.islice` gives you a slice without copying anything

<br><br>

### 6. Release What You No Longer Need

- Use `del` on large objects once you are done with them
- Keep big objects inside functions so they are freed when the function returns
- Avoid parking large data in global variables or long living lists, they never get released

<br><br>

### 7. Put a Limit on Your Caches

- An unbounded cache is just a slow memory leak
- Use `functools.lru_cache(maxsize=1000)` instead of `maxsize=None`
- Use `weakref` based caches when entries should disappear once nobody uses them

<br><br>

### 8. Shrink Data Types in Pandas and NumPy

- Downcast `int64` to `int32` or `int8` when the values are small
- Convert repeated text columns to the `category` dtype
- Load only the columns you actually need with `usecols`

<br><br>

### 9. Watch for Circular References and Leaks

- Python frees objects mainly through reference counting
- Two objects pointing at each other keep each other alive, so the counter never reaches zero
- The cyclic garbage collector cleans these up later, and `gc.collect()` can force it
- Better fix: avoid the cycle, or use `weakref` for the back pointer

<br><br>

### 10. Measure Before You Optimize

- `sys.getsizeof(obj)` gives the size of a single object
- `tracemalloc` shows which lines allocated the most memory
- `memory_profiler` reports memory usage line by line
- Optimize only what the numbers point at, guessing usually wastes effort
