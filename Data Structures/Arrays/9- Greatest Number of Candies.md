# 1431. Kids With the Greatest Number of Candies
`LeetCode 75`

## Problem Statement

There are `n` kids with candies. You are given an integer array `candies`, where each `candies[i]` represents the number of candies the `i`th kid has, and an integer `extraCandies`, denoting the number of extra candies that you have.

Return a boolean array `result` of length `n`, where `result[i]` is `true` if, after giving the `i`th kid all the `extraCandies`, they will have the greatest number of candies among all the kids, or `false` otherwise.



## My Solutions

Here are the three approaches I used to solve this problem. Each step shows an improvement in terms of readability and optimization.

### **Solution 1: My Initial Approach**

```python
class Solution(object):
    def kidsWithCandies(self, candies, extraCandies):
        """
        :type candies: List[int]
        :type extraCandies: int
        :rtype: List[bool]
        """

        max_value = max(candies)
        length_of_array = len(candies)
        result = [False] * length_of_array

        for i in range(0, length_of_array):
            if candies[i] + extraCandies >= max_value:
                result[i] = True
        
        return result
```

* Here, I first find the maximum number of candies any kid has.
* Then, I loop through each kid and check if their candies + `extraCandies` is greater or equal to the max.
* Complexity: **O(n)**


### **Solution 2: Optimized with Max Lookup**

```python
class Solution(object):
    def kidsWithCandies(self, candies, extraCandies):
        max_value = max(candies)
        n = len(candies)
        result = []

        for i in range(n):
            result.append(candies[i] + extraCandies >= max_value)
        
        return result
```

* Instead of pre-creating a result array of `False`, I directly append the boolean result.
* Slightly cleaner while still maintaining clarity.
* Complexity: **O(n)**


### **Solution 3: Even Cleaner Pythonic Way**

```python
class Solution(object):
    def kidsWithCandies(self, candies, extraCandies):
        max_value = max(candies)
        return [candy + extraCandies >= max_value for candy in candies]
```

* This version uses **list comprehension**.
* Very concise and still easy to read.
* Complexity: **O(n)**



## Takeaway

* **Brute force** approach (not included here) would compare each kid with all others → `O(n^2)`.
* With preprocessing (using `max()`), we reduced it to **O(n)**.
* Finally, with Python’s **list comprehension**, we made it more concise without losing efficiency.

This problem is a great example of how:

1. Preprocessing (finding `max`) can save redundant work.
2. Writing clean, concise solutions improves readability while keeping the same performance.
