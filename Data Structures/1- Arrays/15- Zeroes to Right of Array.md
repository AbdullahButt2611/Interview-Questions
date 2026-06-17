# Move Zeroes to End of Array
`Pentaloop` `LeetCode 75`

## Problem Statement

Given an integer array `nums`, move all 0's to the end of it while maintaining the relative order of the non-zero elements.

You must do this **in-place** without making a copy of the array.

### Example 1

```python
Input: nums = [0, 1, 0, 3, 12]
Output: [1, 3, 12, 0, 0]
```

### Example 2

```python
Input: nums = [0]
Output: [0]
```

### Constraints

```
1 <= nums.length <= 10^4
-2^31 <= nums[i] <= 2^31 - 1
```

<br><br>

## Approach 1: In-Place Swapping with Two Pointers

### Idea

Use two pointers:

* One pointer (`locating_pointer`) scans through the list.
* The other pointer (`insert_pos`) keeps track of the index where the next non-zero element should go.

When we find a non-zero element, we swap it with the element at `insert_pos` and move `insert_pos` forward.

This keeps all non-zero elements in the same order, while zeroes naturally move to the end.

### Code

```python
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        insert_pos = 0
        locating_pointer = 0

        while locating_pointer < len(nums):
            if nums[locating_pointer] != 0:
                nums[insert_pos], nums[locating_pointer] = nums[locating_pointer], nums[insert_pos]
                insert_pos += 1
            locating_pointer += 1
```

### Step-by-Step Example

For `nums = [0, 1, 0, 3, 12]`:

| Step | locating_pointer | insert_pos | Action                      | Array            |
| ---- | ---------------- | ---------- | --------------------------- | ---------------- |
| 1    | 0                | 0          | Found 0, do nothing         | [0, 1, 0, 3, 12] |
| 2    | 1                | 0          | Found 1, swap with nums[0]  | [1, 0, 0, 3, 12] |
| 3    | 2                | 1          | Found 0, do nothing         | [1, 0, 0, 3, 12] |
| 4    | 3                | 1          | Found 3, swap with nums[1]  | [1, 3, 0, 0, 12] |
| 5    | 4                | 2          | Found 12, swap with nums[2] | [1, 3, 12, 0, 0] |

Final Output: `[1, 3, 12, 0, 0]`

### Explanation

* The non-zero elements are swapped forward as soon as they are found.
* `insert_pos` always marks the boundary between the processed (non-zero) and unprocessed part.

### Why This Works

* The relative order of non-zero elements stays the same.
* All operations are in-place.

Time Complexity: **O(n)**
Space Complexity: **O(1)**

<br>

## Approach 2: Optimized In-Place

### Idea

We can simplify the code slightly by using only one loop variable for scanning.

### Code

```python
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        insert_pos = 0
        for i in range(len(nums)):
            if nums[i] != 0:
                nums[insert_pos], nums[i] = nums[i], nums[insert_pos]
                insert_pos += 1
```

### Explanation

* This is functionally the same as Approach 2.
* Cleaner and easier to read since we don’t need a second variable explicitly.

### Performance

Time Complexity: **O(n)**
Space Complexity: **O(1)**

This is the **optimal and most elegant** in-place approach for this problem.

<br>

## Final Thoughts

* The two-pointer technique is one of the most common and powerful tools for array manipulation.
* Problems similar to this include:

  * Removing elements from an array
  * Partitioning based on a condition
  * Rearranging elements based on parity or sign

<br>

**Key Takeaway:**
The main idea is to use a pointer to track the position where the next valid (non-zero) element should go, rather than searching multiple times.
