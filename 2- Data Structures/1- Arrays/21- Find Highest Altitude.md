# Find the Highest Altitude
`LeetCode 75`

## Problem Statement

A biker is going on a road trip that consists of **n + 1** points at different altitudes. The biker starts his trip at point `0` with an altitude equal to `0`.

You are given an integer array `gain` of length `n`, where `gain[i]` represents the **net gain in altitude** between points `i` and `i + 1` for all `(0 <= i < n)`.

Your task is to return the **highest altitude** of any point during the trip.

### Example 1

**Input:**

```python
gain = [-5, 1, 5, 0, -7]
```

**Output:**

```python
1
```

**Explanation:**
The altitudes during the trip are `[0, -5, -4, 1, 1, -6]`. The highest altitude is `1`.

### Example 2

**Input:**

```python
gain = [-4, -3, -2, -1, 4, 3, 2]
```

**Output:**

```python
0
```

**Explanation:**
The altitudes during the trip are `[0, -4, -7, -9, -10, -6, -3, -1]`. The highest altitude is `0`.

### Constraints

* `n == gain.length`
* `1 <= n <= 100`
* `-100 <= gain[i] <= 100`

<br><br>

## Approach 1: Prefix Sum Simulation (Iterative)

### Idea

The biker starts at altitude `0`. For each value in `gain`, we add it to a running sum to simulate the altitude change. While doing this, we keep track of the **maximum altitude** reached.

### Steps

1. Start from `altitude = 0`.
2. For each `gain[i]`, add it to a `prefix_sum` (which represents current altitude).
3. Keep updating the `highest_altitude` whenever the `prefix_sum` is greater than the current maximum.

### Code

```python
class Solution:
    def largestAltitude(self, gain: List[int]) -> int:
        highest_altitude = 0
        prefix_sum = 0

        for value in gain:
            prefix_sum += value
            if prefix_sum > highest_altitude:
                highest_altitude = prefix_sum
        
        return highest_altitude
```

### Explanation

* We initialize both `prefix_sum` and `highest_altitude` as `0` because the biker starts at ground level.
* As we move through the list, we add each gain to `prefix_sum`.
* Each time we check if `prefix_sum` exceeds `highest_altitude` and update it.

### Time Complexity

* **O(n)**:  We traverse the list once.

### Space Complexity

* **O(1)**: Only a few variables are used.

<br><br>

## Approach 2: Using Prefix Sum Array

### Idea

Instead of tracking prefix sum in a single variable, we can explicitly build the altitude list (prefix sum array) and return the maximum value.

### Code

```python
class Solution:
    def largestAltitude(self, gain: List[int]) -> int:
        altitudes = [0]  # Starting altitude
        
        for value in gain:
            altitudes.append(altitudes[-1] + value)
        
        return max(altitudes)
```

### Explanation

* We build a list `altitudes` that stores the altitude after each gain.
* At the end, we simply take the `max` value from it.

### Time Complexity

* **O(n)**: Iteration through the list once.

### Space Complexity

* **O(n)**: We store all intermediate altitude values.

### Discussion

While this approach is simple to understand, it uses extra space to store all intermediate altitudes. The **first approach** is more memory efficient since it only keeps track of the current and highest altitudes.

<br><br>

## Final Thoughts

Both solutions solve the problem correctly. The **iterative approach (Approach 1)** is preferred in interviews because:

* It uses **constant space**.
* It is straightforward and efficient.
