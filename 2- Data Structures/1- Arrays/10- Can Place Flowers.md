# Can Place Flowers
`LeetCode 75`

## Problem Statement

You have a long flowerbed in which some of the plots are planted, and some are not. However, flowers cannot be planted in adjacent plots.

Given an integer array `flowerbed` containing `0`'s and `1`'s, where `0` means empty and `1` means not empty, and an integer `n`, return `true` if `n` new flowers can be planted in the flowerbed without violating the no-adjacent-flowers rule and `false` otherwise.

### Examples

**Example 1:**

```text
Input: flowerbed = [1,0,0,0,1], n = 1
Output: true
```

**Example 2:**

```text
Input: flowerbed = [1,0,0,0,1], n = 2
Output: false
```

## Approaches

We’ll explore the problem step by step: starting from the brute force solution, moving to a greedy simulation, and then finally an optimized mathematical greedy approach.

### 1. Brute Force Approach

**Idea:**

* Try to place flowers one by one in every possible location.
* After each attempt, check if the placement is valid (neighbors are empty).
* Continue until either we plant all `n` flowers or we run out of space.

```python
class Solution(object):
    def canPlaceFlowers(self, flowerbed, n):
        def can_place(i):
            if flowerbed[i] == 1:
                return False
            if i > 0 and flowerbed[i - 1] == 1:
                return False
            if i < len(flowerbed) - 1 and flowerbed[i + 1] == 1:
                return False
            return True

        for i in range(len(flowerbed)):
            if can_place(i):
                flowerbed[i] = 1
                n -= 1
                if n == 0:
                    return True
        return n <= 0
```

**Complexity:**

* Time: O(m²) in worst case.
* Space: O(1).

### 2. Greedy Simulation Approach

**Idea:**

* Traverse the array once.
* If a position and its neighbors are empty, plant a flower.
* Stop early if we’ve planted `n` flowers.

To handle edges cleanly, we pad the array with extra zeros at both ends.

```python
class Solution(object):
    def canPlaceFlowers(self, flowerbed, n):
        f = [0] + flowerbed + [0]

        for i in range(1, len(f) - 1):
            if f[i - 1] == 0 and f[i] == 0 and f[i + 1] == 0:
                f[i] = 1
                n -= 1
        
        return n <= 0
```

**Complexity:**

* Time: O(m)
* Space: O(m) due to padding (can be optimized to O(1) if handled inline).

### 3. Mathematical Greedy Approach (Optimal)

**Idea:**

* Count stretches of consecutive zeros between flowers.
* Calculate how many flowers can fit in each stretch.
* Use boundary padding logic implicitly by initializing counters.

```python
class Solution(object):
    def canPlaceFlowers(self, flowerbed, n):
        count = 0
        zeros = 1  # pretend there’s a zero before the first element

        for f in flowerbed:
            if f == 0:
                zeros += 1
            else:
                count += (zeros - 1) // 2
                zeros = 0
        
        zeros += 1  # pretend there’s a zero after the last element
        count += (zeros - 1) // 2

        return count >= n
```

**Complexity:**

* Time: O(m)
* Space: O(1).

## Summary

* **Brute Force:** Works but inefficient.
* **Greedy Simulation:** Simple, clean, and efficient.
* **Mathematical Greedy:** Most optimal (O(m), O(1)), avoids modifying the array.
