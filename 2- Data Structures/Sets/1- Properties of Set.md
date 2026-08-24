# Properties of Sets

`Tajir`
<br><br>

In Python, sets are a collection data type that stores <mark> unordered, unique </mark> elements. They support mathematical set operations such as `union`, `intersection`, and `difference`. Below are the key properties of sets in Python:

<br>

## Unordered

A set does not maintain the order of elements. When elements are added, their order in the set is not guaranteed.
```python
my_set = {3, 1, 2}
print(my_set)  # Output: {1, 2, 3}
```

<br>

## Unique Elements
Sets do not allow duplicate elements. If a duplicate is added, it will be ignored.

```python
my_set = {1, 2, 2, 3}
print(my_set)  # Output: {1, 2, 3}
```

<br>

## Mutable
Sets themselves are mutable, meaning you can add or remove elements from a set after its creation.

```python
my_set = {1, 2, 3}
my_set.add(4)  # Adds 4 to the set
print(my_set)  # Output: {1, 2, 3, 4}
```

<br>

## Immutable Elements
The elements within a set must be immutable (e.g., integers, strings, tuples). You cannot have mutable elements like lists or dictionaries inside a set.

```python
my_set = {1, (2, 3)}
print(my_set)  # Valid set

my_set = {1, [2, 3]}  # Raises a TypeError because lists are mutable
```

<br>

## No Indexing or Slicing
Since sets are unordered, they do not support indexing, slicing, or any form of positional access to elements.

```python
my_set = {1, 2, 3}
print(my_set[0])  # Raises a TypeError
```

<br>

## Set Operations
Sets support several mathematical operations such as:

### Union (|):
Combines elements from two sets.

```python
set1 = {1, 2, 3}
set2 = {3, 4, 5}
print(set1 | set2)  # Output: {1, 2, 3, 4, 5}
```

### Intersection (&):
Returns elements common to both sets

```python
print(set1 & set2)  # Output: {3}
```

### Difference (-):
Returns elements in one set but not in another.

```python
print(set1 - set2)  # Output: {1, 2}
```

### Symmetric Difference (^):
Returns elements that are in either set but not in both.

```python
print(set1 ^ set2)  # Output: {1, 2, 4, 5}
```

<br>

## Membership Testing
Sets allow for fast membership testing using the in operator.

```python
my_set = {1, 2, 3}
print(2 in my_set)  # Output: True
print(4 in my_set)  # Output: False
```

<br>

## Frozensets (Immutable Sets)
Python also provides a special type called frozenset, which is an immutable version of a set. Once created, you cannot modify a frozenset.

```python
my_frozen_set = frozenset([1, 2, 3])
# my_frozen_set.add(4)  # Raises an AttributeError since frozenset is immutable
```