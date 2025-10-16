# Product of Array Except Self
`LeetCode 75`

### Problem Statement

Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the **product of all the elements** of `nums` **except** `nums[i]`.

The product of any prefix or suffix of `nums` is guaranteed to fit in a **32-bit integer**.

You must write an algorithm that runs in **O(n)** time and **without using the division operation**.


### 💡 Example

**Input:**
`nums = [1, 2, 3, 4]`

**Output:**
`[24, 12, 8, 6]`

**Explanation:**

* For index `0`: 2 × 3 × 4 = 24
* For index `1`: 1 × 3 × 4 = 12
* For index `2`: 1 × 2 × 4 = 8
* For index `3`: 1 × 2 × 3 = 6

<br><br>

## Approach 1: Brute Force

### Idea

For each element in the array, calculate the product of all elements **except** itself using a nested loop.

This is the most direct solution, easy to understand, but **inefficient** for large arrays.

### Code

```python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = []

        # For every element, compute product of all except itself
        for i in range(n):
            product = 1
            for j in range(n):
                if i != j:
                    product *= nums[j]
            result.append(product)

        return result
```

### Complexity Analysis

* **Time Complexity:** O(n²) — because of the nested loops.
* **Space Complexity:** O(1) — ignoring the output array.

### Problem with this approach

* This approach becomes **too slow** for large arrays.
* We need a way to compute results in **O(n)** without nested loops.

<br>

## Approach 2: Optimized (Prefix and Suffix Products)

### Idea

Instead of recomputing the entire product for every index, we can precompute:

* **Prefix products:** Product of all elements **before** each index.
* **Suffix products:** Product of all elements **after** each index.

Then, for each index `i`:

```
answer[i] = prefix[i] * suffix[i]
```

This allows us to calculate the result in **O(n)** time.

### Code

```python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        prefix = [1] * n
        suffix = [1] * n
        result = [0] * n

        # Compute prefix products
        for i in range(1, n):
            prefix[i] = prefix[i - 1] * nums[i - 1]

        # Compute suffix products
        for i in range(n - 2, -1, -1):
            suffix[i] = suffix[i + 1] * nums[i + 1]

        # Multiply prefix and suffix to get the result
        for i in range(n):
            result[i] = prefix[i] * suffix[i]

        return result
```

### Example Walkthrough

For `nums = [1, 2, 3, 4]`:

| Index | nums[i] | prefix[i] | suffix[i] | result[i] = prefix × suffix |
| :---: | :-----: | :-------: | :-------: | :-------------------------: |
|   0   |    1    |     1     |     24    |              24             |
|   1   |    2    |     1     |     12    |              12             |
|   2   |    3    |     2     |     8     |              8              |
|   3   |    4    |     6     |     1     |              6              |

### Complexity Analysis

* **Time Complexity:** O(n) — three linear passes (prefix, suffix, result).
* **Space Complexity:** O(n) — due to prefix and suffix arrays.
* **No division used.**

### Why this is better

* This reduces the time complexity from **O(n²)** → **O(n)**.
* Still very readable and conceptually simple.

<br>

## Summary of Approaches

| Approach            | Description                          | Time  | Space | Division Used |
| ------------------- | ------------------------------------ | ----- | ----- | ------------- |
|  Brute Force     | Nested loops for each index          | O(n²) | O(1)  | ❌             |
| Prefix + Suffix | Use prefix and suffix precomputation | O(n)  | O(n)  | ❌             |


