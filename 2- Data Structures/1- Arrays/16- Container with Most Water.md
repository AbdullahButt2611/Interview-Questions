# Container With Most Water
`LeetCode 75` `Educative`

## Problem Statement

You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the *i*th line are `(i, 0)` and `(i, height[i])`.

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return *the maximum amount of water a container can store*.

You **may not slant** the container.

![alt text](Problem16.png)

### Example 1

**Input:** `height = [1,8,6,2,5,4,8,3,7]`
**Output:** `49`
**Explanation:** The maximum area of water the container can contain is 49.

### Example 2

**Input:** `height = [1,1]`
**Output:** `1`

<br><br>

## Approach 1: Brute Force

### Idea

Check **every pair of lines**, calculate the area formed by them, and keep track of the **maximum**.

For two lines at indices `i` and `j`:

```
Area = min(height[i], height[j]) * (j - i)
```

### Code

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:
        n = len(height)
        max_water = 0

        for i in range(n):
            for j in range(i + 1, n):
                area = min(height[i], height[j]) * (j - i)
                max_water = max(max_water, area)

        return max_water
```

### Complexity

* **Time:** O(n²)
* **Space:** O(1)

### Problem with this approach

This solution checks every possible pair of lines. For large arrays, it becomes very slow because the time grows quickly as `n` increases.

We can do much better by using a smarter technique.

<br>

## Approach 2: Two Pointer Method (Optimal)

### Idea

Start with two pointers:

* One at the **start** (`left = 0`)
* One at the **end** (`right = len(height) - 1`)

We calculate the area between them and then **move the pointer at the shorter line inward**, because the height of the container is limited by the shorter line.

By moving the shorter one, there’s a chance to find a taller line that increases the area.

### Steps

1. Set `left = 0` and `right = n - 1`
2. While `left < right`:

   * Calculate the current area
   * Update `max_water` if needed
   * Move the pointer pointing to the **shorter** line
3. Return `max_water`

### Code

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:
        if not height or len(height) == 1:
            return 0

        left = 0
        right = len(height) - 1
        max_water = 0

        while left < right:
            area = min(height[left], height[right]) * (right - left)
            max_water = max(max_water, area)

            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return max_water
```

### Complexity

* **Time:** O(n) — Each element is checked at most once.
* **Space:** O(1)

### Explanation

The key insight is that moving the **taller** line never increases the area. The smaller height limits the water level, so to potentially get more area, we must move past the smaller height and hope for a taller line.

<br>

## Final Thoughts

* Brute force is good for understanding how the area is calculated.
* The two-pointer approach is the optimized version and is the standard solution used in interviews.
* This is a common pattern — **move two pointers from opposite ends** and adjust based on which side limits the result.

<br>

**Tags:** `Two Pointers` `Array` `Greedy` `Math`

