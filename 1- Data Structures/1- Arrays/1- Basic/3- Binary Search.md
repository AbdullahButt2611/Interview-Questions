# Binary Search

`Google` • `Amazon` • `Meta` • `Microsoft` • `Apple` • `Bloomberg`

## Problem Statement

Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, then return its index. Otherwise, return `-1`.

You must write an algorithm with `O(log n)` runtime complexity.

## Examples

**Example 1:**

```
Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4
```

**Example 2:**

```
Input: nums = [-1,0,3,5,9,12], target = 2
Output: -1
Explanation: 2 does not exist in nums so return -1
```

## Constraints

- `1 <= nums.length <= 10^4`
- `-10^4 < nums[i], target < 10^4`
- All the integers in `nums` are unique.
- `nums` is sorted in ascending order.

<br><br>

## Approach 1: Recursive Binary Search

### Idea

- The array is sorted, so we do not need to check every element.
- Look at the middle element of the current search range.
- Three cases are possible:
  - Middle element equals the target, so return its index.
  - Middle element is smaller than the target, so the target can only be on the right side.
  - Middle element is larger than the target, so the target can only be on the left side.
- Recursively repeat the same logic on the half that can contain the target.
- If the range becomes empty, the target is not present, so return `-1`.

### Solution

```python3
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        def binarySearch(low: int, high: int) -> int:
            # Base case: search space is empty
            if low > high:
                return -1

            mid = low + (high - low) // 2

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                return binarySearch(mid + 1, high)   # go right
            else:
                return binarySearch(low, mid - 1)    # go left

        return binarySearch(0, len(nums) - 1)
```

### Explanation

- `low` and `high` mark the current search range (both inclusive).
- `mid = low + (high - low) // 2` finds the middle index.
  - This form avoids integer overflow in languages like Java and C++.
  - In Python it is not required, but it is the standard interview-safe way to write it.
- If `nums[mid]` matches the target, we are done.
- If `nums[mid] < target`, every element from `low` to `mid` is too small, so we recurse on `(mid + 1, high)`.
- If `nums[mid] > target`, every element from `mid` to `high` is too big, so we recurse on `(low, mid - 1)`.
- The base case `low > high` means the search space is empty, so the target does not exist.

### Dry Run

```
nums = [-1, 0, 3, 5, 9, 12], target = 9

Call 1: low = 0, high = 5 -> mid = 2, nums[2] = 3
        3 < 9, search right half

Call 2: low = 3, high = 5 -> mid = 4, nums[4] = 9
        9 == 9, return 4

Answer: 4
```

### Complexity

- **Time:** `O(log n)`, the search space is halved on every call.
- **Space:** `O(log n)`, each recursive call adds a frame to the call stack.

### What is the problem with this approach?

- The logic is optimal, but the recursion itself costs extra memory.
- Every recursive call stays on the call stack until the answer is returned, so we use `O(log n)` auxiliary space.
- Recursion also adds function call overhead and carries a (theoretical) risk of stack overflow for very deep recursions.
- The same halving idea can be written with a simple loop, which removes the stack usage completely.

<br><br>

## Approach 2: Iterative Binary Search (Optimal)

### Idea

- Keep the exact same halving logic, but replace recursion with a `while` loop.
- Maintain two pointers, `low` and `high`, that shrink toward each other.
- Loop while the search range is valid (`low <= high`):
  - If the middle element equals the target, return the index.
  - If it is smaller, move `low` to `mid + 1`.
  - If it is larger, move `high` to `mid - 1`.
- If the loop ends, the target is not in the array, so return `-1`.

### Solution

```python3
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        low, high = 0, len(nums) - 1

        while low <= high:
            mid = low + (high - low) // 2

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                low = mid + 1    # go right
            else:
                high = mid - 1   # go left

        return -1
```

### Explanation

- Instead of new function calls, we just update `low` and `high` in place.
- The loop condition `low <= high` is important:
  - `<=` (not `<`) ensures a range of size 1 is still checked.
- Each iteration removes half of the remaining elements, exactly like the recursive version.
- When `low` crosses `high`, the search space is empty and we return `-1`.

### Dry Run

```
nums = [-1, 0, 3, 5, 9, 12], target = 2

Iter 1: low = 0, high = 5 -> mid = 2, nums[2] = 3
        3 > 2, high = 1

Iter 2: low = 0, high = 1 -> mid = 0, nums[0] = -1
        -1 < 2, low = 1

Iter 3: low = 1, high = 1 -> mid = 1, nums[1] = 0
        0 < 2, low = 2

Now low (2) > high (1), loop ends.

Answer: -1
```

### Complexity

- **Time:** `O(log n)`, the search space is halved on every iteration.
- **Space:** `O(1)`, only three integer variables are used, no call stack.

### Why is this the best approach?

- Same optimal `O(log n)` time as the recursive version.
- Constant `O(1)` extra space, since there is no recursion stack.
- No function call overhead and no risk of stack overflow.
- This is the standard version expected in interviews.

<br><br>

## Related Problems

- Search Insert Position (LeetCode 35)
- First Bad Version (LeetCode 278)
- Search in Rotated Sorted Array (LeetCode 33)
- Find First and Last Position of Element in Sorted Array (LeetCode 34)
- Find Minimum in Rotated Sorted Array (LeetCode 153)
- Guess Number Higher or Lower (LeetCode 374)
- Sqrt(x) (LeetCode 69)