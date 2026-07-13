# Find Out How Many Times the Array Is Rotated

`Amazon` • `Microsoft` • `Meta` • `Bloomberg` • `Goldman Sachs` • `Oracle`

## Problem Statement

Given an integer array `nums` of size `n`, sorted in ascending order with **distinct values**. The array has been **right rotated** an unknown number of times, between `0` and `n - 1` (both inclusive).

Determine the number of rotations performed on the array.

<mark>The number of rotations is exactly the index of the minimum element in the rotated array.</mark>

## Examples

**Example 1**

```ini
Input : nums = [4, 5, 6, 7, 0, 1, 2, 3]
Output: 4
Explanation: The original array should be [0, 1, 2, 3, 4, 5, 6, 7].
             The minimum element 0 sits at index 4, so the array has been rotated 4 times.
```

**Example 2**

```ini
Input : nums = [3, 4, 5, 1, 2]
Output: 3
Explanation: The original array should be [1, 2, 3, 4, 5].
             The minimum element 1 sits at index 3, so the array has been rotated 3 times.
```

**Example 3**

```ini
Input : nums = [1, 2, 3, 4, 5]
Output: 0
Explanation: The array is not rotated at all, so the minimum sits at index 0.
```

## Constraints

- `1 <= n <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
- All values in `nums` are **distinct**
- The array is sorted in ascending order and then right rotated `k` times, where `0 <= k <= n - 1`

<br><br>

## Intuition

- A rotated sorted array is made of **two sorted halves**.
- The **minimum element** is the only point where the ascending order breaks (the pivot).
- Everything before the minimum belongs to the "bigger" half, everything from the minimum onwards belongs to the "smaller" half.
- So the answer reduces to: **find the index of the minimum element**, and that index is the rotation count.
- A linear scan would take `O(n)`. Since the array is (piecewise) sorted, we can do better with **binary search** in `O(log n)`.

<br><br>

## Approach (Binary Search)

At every step, we split the array at `mid`. At least one of the two halves is guaranteed to be **fully sorted**.

**Step 1: Identify the sorted half**

- If `nums[low] <= nums[mid]` → the **left half is sorted**.
- Otherwise → the **right half is sorted**.

**Step 2: Take the candidate minimum from the sorted half**

- If the left half is sorted, its smallest element is `nums[low]`. Compare it with the running minimum and update `rotation = low` if it is smaller. Then discard the left half by moving `low = mid + 1`.
- If the right half is sorted, its smallest element is `nums[mid]`. Compare it with the running minimum and update `rotation = mid` if it is smaller. Then discard the right half by moving `high = mid - 1`.

**Step 3: Repeat until `low > high`**

The running `rotation` variable then holds the index of the global minimum, which is the answer.

<mark>Key idea: we never search inside the sorted half. We only pick its smallest element as a candidate and then throw that half away.</mark>

<br><br>

## Code

```python
class Solution:
    def findKRotation(self, nums):
        low = 0
        high = len(nums) - 1

        mini_element = float('inf')
        rotation = 0

        while low <= high:
            mid = (low + high) // 2

            # Left half is sorted
            if nums[low] <= nums[mid]:
                if nums[low] <= mini_element:
                    mini_element = nums[low]
                    rotation = low
                low = mid + 1

            # Right half is sorted
            else:
                if nums[mid] <= mini_element:
                    mini_element = nums[mid]
                    rotation = mid
                high = mid - 1

        return rotation
```

<br><br>

## Dry Run

Input: `nums = [4, 5, 6, 7, 0, 1, 2, 3]`

```ini
Initial : low = 0, high = 7, mini_element = inf, rotation = 0

Step 1  : mid = (0 + 7) // 2 = 3
          nums[low] = 4, nums[mid] = 7  ->  4 <= 7, left half is sorted
          4 <= inf  ->  mini_element = 4, rotation = 0
          low = mid + 1 = 4

Step 2  : low = 4, high = 7, mid = (4 + 7) // 2 = 5
          nums[low] = 0, nums[mid] = 1  ->  0 <= 1, left half is sorted
          0 <= 4  ->  mini_element = 0, rotation = 4
          low = mid + 1 = 6

Step 3  : low = 6, high = 7, mid = (6 + 7) // 2 = 6
          nums[low] = 2, nums[mid] = 2  ->  2 <= 2, left half is sorted
          2 <= 0 is False  ->  no update
          low = mid + 1 = 7

Step 4  : low = 7, high = 7, mid = 7
          nums[low] = 3, nums[mid] = 3  ->  3 <= 3, left half is sorted
          3 <= 0 is False  ->  no update
          low = mid + 1 = 8

Loop ends (low = 8 > high = 7)

Answer  : rotation = 4
```

<br><br>

## Complexity Analysis

- **Time Complexity:** `O(log n)` because the search space is halved on every iteration.
- **Space Complexity:** `O(1)` since only a few pointers and variables are used.

<br><br>

## Edge Cases to Remember

- **Array not rotated at all** (`[1, 2, 3, 4, 5]`): the left half stays sorted throughout and `rotation` correctly stays at `0`.
- **Single element array** (`[7]`): the loop runs once and returns `0`.
- **Rotated by `n - 1`** (`[2, 3, 4, 5, 1]`): the minimum is the last element and gets picked up in the final iterations.
- <mark>Duplicates are not allowed here. If duplicates were present, the check nums[low] <= nums[mid] could no longer identify the sorted half reliably, and we would need the extra shrinking step used in Find Minimum in Rotated Sorted Array II.</mark>

<br><br>

## Optimisation Note

If at any point `nums[low] <= nums[high]`, the entire current search window is already sorted. You can immediately compare `nums[low]` with the running minimum, record `low` as the rotation index, and break out of the loop. This does not change the worst case complexity but speeds up many practical cases.

<br><br>

## Related Problems

- [Find Minimum in Rotated Sorted Array (LeetCode 153)](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)
- [Find Minimum in Rotated Sorted Array II (LeetCode 154)](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/)
- [Search in Rotated Sorted Array (LeetCode 33)](https://leetcode.com/problems/search-in-rotated-sorted-array/)
- [Search in Rotated Sorted Array II (LeetCode 81)](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/)
- [Check if Array Is Sorted and Rotated (LeetCode 1752)](https://leetcode.com/problems/check-if-array-is-sorted-and-rotated/)
- [Rotate Array (LeetCode 189)](https://leetcode.com/problems/rotate-array/)
- [Find Peak Element (LeetCode 162)](https://leetcode.com/problems/find-peak-element/)
- [Peak Index in a Mountain Array (LeetCode 852)](https://leetcode.com/problems/peak-index-in-a-mountain-array/)
- [Single Element in a Sorted Array (LeetCode 540)](https://leetcode.com/problems/single-element-in-a-sorted-array/)