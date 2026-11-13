# Count the Number of Digits in a Given Number

## Problem Statement

Given an integer number, count the total number of digits it contains.

## Example

**Input:**

```
num = 43215
```

**Output:**

```
5
```

## Solution Approaches

### Approach 1: Using Count Logic (Modulo Division)

We repeatedly divide the number by 10 and increment the counter until the number becomes 0.

```python
def count_digits_modulo(num: int) -> int:
    num = abs(num)  # handle negative numbers
    if num == 0:
        return 1
    count = 0
    while num > 0:
        num //= 10
        count += 1
    return count

# Example usage
print(count_digits_modulo(43215))  # Output: 5
```

### Approach 2: Using log10 (Mathematical Approach)

We can use the logarithmic property:

```
Number of digits in N = ⌊log10(N)⌋ + 1
```

This avoids iteration and is efficient for large numbers.

```python
import math

def count_digits_log(num: int) -> int:
    if num == 0:
        return 1
    return int(math.log10(abs(num))) + 1

# Example usage
print(count_digits_log(43215))  # Output: 5
```

## Notes

* Both approaches handle positive and negative numbers.
* For zero, both approaches return 1 since 0 has one digit.
* The log10 approach requires an explicit check for 0, as `log10(0)` is undefined.
