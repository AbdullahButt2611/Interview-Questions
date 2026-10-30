# Container With Most Water

`Amazon` • `Google` • `Meta` • `Microsoft` • `Apple` • `Bloomberg` • `Adobe` • `Goldman Sachs` • `Uber` • `Educative`

## Problem Statement

You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the *i*th line are `(i, 0)` and `(i, height[i])`.

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return _the maximum amount of water a container can store_.

You **may not slant** the container.

![alt text](Problem16.png)

## Examples

### Example 1

**Input:** `height = [1,8,6,2,5,4,8,3,7]`

**Output:** `49`

**Explanation:** The lines at index `1` (height 8) and index `8` (height 7) form the best container. Width is `8 - 1 = 7`, height is `min(8, 7) = 7`, so the area is `7 * 7 = 49`.

### Example 2

**Input:** `height = [1,1]`

**Output:** `1`

**Explanation:** There are only two lines. Width is `1`, height is `1`, so the area is `1`.

## Constraints

- `n == height.length`
- `2 <= n <= 10^5`
- `0 <= height[i] <= 10^4`

<br><br>

## Understanding the Container

Think of any two lines as the two walls of a fish tank.

- **Width** = distance between the two walls = `right index - left index`
- **Height** = the **shorter** wall (water spills over the short side)
- **Water** = width multiplied by height

```ini
Area = min(height[left], height[right]) * (right - left)
```

<mark>The shorter wall always decides how much water you can hold.</mark>

<br><br>

## Approach 1: Brute Force

### Idea

- Try **every pair** of walls, calculate the water, and keep the biggest.

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

- **Time:** `O(n²)`, every pair is checked.
- **Space:** `O(1)`

### Problem with this approach

- With `n = 10^5`, that is about **5 billion** pairs, which will time out.

<br><br>

## Approach 2: Two Pointers (Optimal)

### The Big Idea (remember this one line)

<mark>Start with the widest container, then always move the shorter wall inward.</mark>

### Why does this work?

- We start with the walls at the two ends, so the **width is as big as it can ever be**.
- From here, every move makes the width **smaller by 1**.
- To get more water with less width, we **need a taller wall**.
- The **shorter wall** is the one holding us back.
- If we move the **taller** wall instead:
  - Width goes down.
  - Height is still stuck at the short wall (or lower).
  - So the water **can never increase**. That move is useless.
- If we move the **shorter** wall:
  - Width goes down.
  - But we might find a taller wall, which could raise the water level.
  - This is the **only move that has a chance** of doing better.

### Simple real life picture

- Imagine two friends holding the ends of a rope to make a fence.
- The fence is only as tall as the **shorter friend**.
- Asking the **taller** friend to step closer only makes the fence narrower, never taller.
- So you swap out the **shorter** friend, hoping for someone taller.

### Steps

1. Put `left` at the first wall (`0`) and `right` at the last wall (`n - 1`).
2. Set `max_water = 0`.
3. While `left < right`:
   - Width = `right - left`.
   - Height = the shorter of `height[left]` and `height[right]`.
   - Area = width multiplied by height.
   - Update `max_water` if this area is bigger.
   - If the left wall is shorter, move `left` one step right.
   - Otherwise, move `right` one step left.
4. When the two pointers meet, return `max_water`.

### Code

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        max_water = 0

        while left < right:
            width = right - left
            h = min(height[left], height[right])
            area = width * h
            max_water = max(max_water, area)

            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return max_water
```

### Dry Run

```ini
Input: height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
Index:           0  1  2  3  4  5  6  7  8

Start: left = 0, right = 8, max_water = 0

Iteration 1:
  left = 0 (height 1), right = 8 (height 7)
  width  = 8 - 0 = 8
  height = min(1, 7) = 1
  area   = 1 * 8 = 8
  max_water = max(0, 8) = 8
  Compare: 1 < 7, left wall is shorter
  Move left: left = 1

Iteration 2:
  left = 1 (height 8), right = 8 (height 7)
  width  = 8 - 1 = 7
  height = min(8, 7) = 7
  area   = 7 * 7 = 49
  max_water = max(8, 49) = 49
  Compare: 8 < 7 is false, right wall is shorter
  Move right: right = 7

Iteration 3:
  left = 1 (height 8), right = 7 (height 3)
  width  = 7 - 1 = 6
  height = min(8, 3) = 3
  area   = 3 * 6 = 18
  max_water = max(49, 18) = 49
  Compare: 8 < 3 is false, right wall is shorter
  Move right: right = 6

Iteration 4:
  left = 1 (height 8), right = 6 (height 8)
  width  = 6 - 1 = 5
  height = min(8, 8) = 8
  area   = 8 * 5 = 40
  max_water = max(49, 40) = 49
  Compare: 8 < 8 is false, walls are equal, move right
  Move right: right = 5

Iteration 5:
  left = 1 (height 8), right = 5 (height 4)
  width  = 5 - 1 = 4
  height = min(8, 4) = 4
  area   = 4 * 4 = 16
  max_water = max(49, 16) = 49
  Compare: 8 < 4 is false, right wall is shorter
  Move right: right = 4

Iteration 6:
  left = 1 (height 8), right = 4 (height 5)
  width  = 4 - 1 = 3
  height = min(8, 5) = 5
  area   = 5 * 3 = 15
  max_water = max(49, 15) = 49
  Compare: 8 < 5 is false, right wall is shorter
  Move right: right = 3

Iteration 7:
  left = 1 (height 8), right = 3 (height 2)
  width  = 3 - 1 = 2
  height = min(8, 2) = 2
  area   = 2 * 2 = 4
  max_water = max(49, 4) = 49
  Compare: 8 < 2 is false, right wall is shorter
  Move right: right = 2

Iteration 8:
  left = 1 (height 8), right = 2 (height 6)
  width  = 2 - 1 = 1
  height = min(8, 6) = 6
  area   = 6 * 1 = 6
  max_water = max(49, 6) = 49
  Compare: 8 < 6 is false, right wall is shorter
  Move right: right = 1

Stop: left = 1, right = 1, so left < right is false.

Final Answer: 49 (walls at index 1 and index 8)
```

### Complexity

- **Time:** `O(n)`, because each step moves one pointer, and the pointers meet after at most `n - 1` steps.
- **Space:** `O(1)`, because only a few variables are used.

<br><br>

## Key Takeaways

- Water level is always set by the **shorter wall**.
- Brute force checks all pairs, which is easy to understand but too slow (`O(n²)`).
- Two pointers starts **wide** and smartly shrinks, giving `O(n)`.
- When both walls are equal, moving either one is fine.
- This is a classic pattern: <mark>two pointers from opposite ends, move the side that limits the answer.</mark>

<br><br>

## Related Problems

- [Trapping Rain Water (42)](https://leetcode.com/problems/trapping-rain-water/)
- [3Sum (15)](https://leetcode.com/problems/3sum/)
- [3Sum Closest (16)](https://leetcode.com/problems/3sum-closest/)
- [Two Sum II - Input Array Is Sorted (167)](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
- [Largest Rectangle in Histogram (84)](https://leetcode.com/problems/largest-rectangle-in-histogram/)
- [Boats to Save People (881)](https://leetcode.com/problems/boats-to-save-people/)
- [Maximize Distance to Closest Person (849)](https://leetcode.com/problems/maximize-distance-to-closest-person/)
