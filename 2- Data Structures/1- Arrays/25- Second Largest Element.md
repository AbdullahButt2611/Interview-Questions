# Find the Second Largest Element in an Array

`Accolite` `Zoho` `Hike` `SAP Labs` `FactSet`

## Problem Statement

Given an array of integers `nums`, return the **second largest distinct element**.

If no such element exists, return `-1`.

### Example 1

**Input:** `nums = [12, 35, 1, 10, 34, 1]`  
**Output:** `34`

### Example 2

**Input:** `nums = [10, 5, 10]`  
**Output:** `5`  
**Explanation:** `10` is the largest. The next distinct value is `5`.

### Example 3

**Input:** `nums = [7, 7, 7]`  
**Output:** `-1`

### Constraints

- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

<br>

## Approach 1: Sorting

Sort in descending order, then return the first element that is not equal to the largest.

```python
class Solution:
    def secondLargest(self, nums):
        if len(nums) < 2:
            return -1

        nums.sort(reverse=True)
        for num in nums[1:]:
            if num != nums[0]:
                return num
        return -1
```

**Time:** O(n log n)  
**Space:** O(1)

### Problem with this approach

Sorting does extra work. We only need the top two values, not the full order.

<br>

## Approach 2: Single Pass (Optimal)

Track two variables while scanning:

- `largest`: max seen so far.
- `second`: max value seen so far that is strictly less than `largest`.

For each `num`:
1. If `num > largest`: old `largest` becomes `second`, `num` becomes `largest`.
2. Else if `num < largest` and `num > second`: update `second`.
3. If `num == largest`: skip (we want distinct).

```python
class Solution:
    def secondLargest(self, nums):
        if len(nums) < 2:
            return -1

        largest = float('-inf')
        second = float('-inf')

        for num in nums:
            if num > largest:
                second = largest
                largest = num
            elif num < largest and num > second:
                second = num

        return second if second != float('-inf') else -1
```

**Time:** O(n)  
**Space:** O(1)

<br>

## Dry Run

**Input:** `nums = [12, 35, 1, 10, 34, 1]`  

| num | largest | second |
|-----|---------|--------|
| 12  | 12      | -inf   |
| 35  | 35      | 12     |
| 1   | 35      | 12     |
| 10  | 35      | 12     |
| 34  | 35      | 34     |
| 1   | 35      | 34     |

**Output:** `34`

<br>

## Edge Cases

- Length 1: return `-1`.
- All elements equal: no distinct second largest, return `-1`.
- Negative numbers: handled by `float('-inf')` initial values.
- Largest repeated (e.g. `[10, 10, 5]`): skipped by `num < largest` check, answer is `5`.

<br>

**Tags:** `Array` `Linear Scan` `Easy`
