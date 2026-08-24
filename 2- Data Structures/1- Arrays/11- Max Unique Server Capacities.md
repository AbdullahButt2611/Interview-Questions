# Problem: Maximum Unique Server Capacities
`IBM` `HackerRank`

## Problem Statement

You are given an array, **capacities**, which represents the CPU capacities of **n** servers in a data center. Before starting a new workload, you need to select a subset of these servers such that each server in the subset has a unique CPU capacity.

Each server’s CPU capacity can be adjusted by at most **1 unit** in either direction (increased, decreased, or left unchanged), with the condition that the capacity must always remain **positive**.

Implement a function to select the largest group of servers with unique capacities.

### Function Signature

```python
def getMaxUniqueServer(capacities: list[int]) -> int:
    pass
```

## Input

* `capacities[n]`: List of integers representing CPU capacities of servers.

## Output

* Integer representing the size of the largest subset of servers with unique capacities.

## Constraints

* `1 ≤ n ≤ 2 * 10^5`
* `1 ≤ capacities[i] ≤ 10^9`

## Examples

### Example 1

**Input:**

```
capacities = [1, 1, 2, 1]
```

**Output:**

```
3
```

**Explanation:**
Adjusting capacities with +1, -1, or no change, a possible configuration is `[1, 2, 3, 1]`, achieving 3 unique capacities.

### Example 2

**Input:**

```
capacities = [3, 3, 5, 5, 3]
```

**Output:**

```
5
```

**Explanation:**
Adjusting capacities with +1, -1, or no change, a possible configuration is `[2, 3, 6, 5, 4]`, achieving 5 unique capacities.

### Example 3

**Input:**

```
capacities = [1, 1, 4, 4, 1, 4]
```

**Output:**

```
5
```

**Explanation:**
Adjusting capacities with +1, -1, or no change, a possible configuration is `[1, 2, 3, 5, 1, 4]`, achieving 5 unique capacities.

## Approach

### Greedy + Sorting

1. **Sort the array** of capacities.
2. **Iterate through the capacities** and for each capacity `cap`, try to assign it to the smallest available unique value among `{cap-1, cap, cap+1}`.

   * Always prioritize the smallest valid capacity (`cap-1 > 0`) to leave room for future capacities.
3. **Use a set** to keep track of assigned capacities.
4. **Return the size** of the set.

This greedy approach ensures that we maximize the number of unique capacities while adjusting each capacity by at most 1 unit.

### Complexity

* **Time Complexity:** `O(n log n)` for sorting + `O(n)` for iteration = `O(n log n)`
* **Space Complexity:** `O(n)` for the set storing used capacities

## Python Solution

```python
def getMaxUniqueServer(capacities):
    capacities.sort()
    used = set()
    
    for cap in capacities:
        # Try to use cap-1 if it's valid and available
        if cap - 1 > 0 and (cap - 1) not in used:
            used.add(cap - 1)
        # Otherwise try to use cap
        elif cap not in used:
            used.add(cap)
        # Otherwise try cap+1
        elif (cap + 1) not in used:
            used.add(cap + 1)
    
    return len(used)

if __name__ == "__main__":
    n = int(input().strip())
    capacities = [int(input().strip()) for _ in range(n)]
    print(getMaxUniqueServer(capacities))
```

### Notes

* The solution uses a greedy approach, always picking the smallest possible value to leave space for future capacities.
* Sorting ensures we handle smaller capacities first, which is crucial to maximize unique capacities.
* Works efficiently even for the maximum constraints (`n = 2 * 10^5`).
