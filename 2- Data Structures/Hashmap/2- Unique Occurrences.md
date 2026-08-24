# Unique Number of Occurrences
`LeetCode 75`

## Problem

You are given an array of integers. You need to check if each number in the array appears a different number of times. If all counts are different, return true. If any two numbers appear the same number of times, return false.

### Examples

**Example 1**
Input: `[1,2,2,1,1,3]`
Output: `true`

**Example 2**
Input: `[1,2]`
Output: `false`

**Example 3**
Input: `[-3,0,1,-3,1,1,1,-3,10,0]`
Output: `true`

<br><br>

# Approach 1: Count and Set Check

First we count how many times each number shows up. After that we check if all these counts are different. If the size of the set of counts matches the number of items, then each count is unique.

## Code (Python)

```python
def uniqueOccurrences(arr):
    count = {}
    for num in arr:
        count[num] = count.get(num, 0) + 1

    seen = set()
    for c in count.values():
        if c in seen:
            return False
        seen.add(c)
    return True
```

## Short Note

This works fine and is simple to read. It uses a dictionary for counts and a set to check if any count repeats.
