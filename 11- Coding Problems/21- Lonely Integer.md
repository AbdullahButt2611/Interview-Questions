# Given an array of integers, where all elements but one occur twice, find the unique element.

`HackerRank`
<br><br>

## Brute Force Solution

- Building the frequency dictionary takes 𝑂(𝑛).
- Searching for the unique element also takes 𝑂(𝑛).

Thus, the total time complexity is: O(n) + O(n) = O(n)

```python
def lonelyinteger(a):
    count_int = {}
    
    for element in a:
        if element in count_int:
            count_int[element] += 1
        else:
            count_int[element] = 1
    
    key = next(key for key, value in count_int.items() if value == 1)
    return key
```
<br><br>


## Optimized Solution
Time Complexity: O(n)

```python
def lonelyinteger(a):
    unique = 0
    for num in arr:
        unique ^= num
    return unique
```
<br><br>

### Example
```
arr = [2, 3, 5, 3, 2]
print(find_unique(arr))  # Output: 5
```
<br><br>

### Step-by-Step XOR Breakdown

| Iteration | Element | Binary Element | XOR Result (unique in binary) | Decimal Result (unique) |
|-----------|---------|----------------|-------------------------------|-------------------------|
| 1         | 2       | `0010`         | `0000 ⊕ 0010 = 0010`          | 2                       |
| 2         | 3       | `0011`         | `0010 ⊕ 0011 = 0001`          | 1                       |
| 3         | 5       | `0101`         | `0001 ⊕ 0101 = 0100`          | 4                       |
| 4         | 3       | `0011`         | `0100 ⊕ 0011 = 0111`          | 7                       |
| 5         | 2       | `0010`         | `0111 ⊕ 0010 = 0101`          | 5                       |

