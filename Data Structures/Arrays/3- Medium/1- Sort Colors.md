# Sort Colors ⭐

`Microsoft` • `Google` • `Facebook` • `Amazon` • `LinkedIn` • `Apple` • `Bloomberg` • `Uber` • `Adobe`
<br>

**Also Known As:** Sort an array of 0's, 1's and 2's \
**Topic:** Dutch National Flag Problem

## Problem Statement

Given an array `nums` with `n` objects colored red, white, or blue, sort them [in-place](https://en.wikipedia.org/wiki/In-place_algorithm) so that objects of the same color are adjacent, with the colors in the order red, white, and blue.

We will use the integers `0`, `1`, and `2` to represent the color red, white, and blue, respectively.

You must solve this problem **without** using the library's sort function.

## Examples

**Example 1:**
```
Input:  nums = [2, 0, 2, 1, 1, 0]
Output: [0, 0, 1, 1, 2, 2]
```

**Example 2:**
```
Input:  nums = [2, 0, 1]
Output: [0, 1, 2]
```

**Constraints:**
- `n == nums.length`
- `1 <= n <= 300`
- `nums[i]` is either `0`, `1`, or `2`

<br><br>

## Approach 1: Counting Sort (Two-Pass)

### Intuition

Since we only have three distinct values (`0`, `1`, `2`), we can simply count how many times each appears, then overwrite the entire array in sorted order. This is the most straightforward approach you can think of before optimizing.

**Steps:**
1. Traverse `nums` once and count the frequency of `0`s, `1`s, and `2`s.
2. Overwrite `nums` in a second pass: first fill `count[0]` positions with `0`, then `count[1]` positions with `1`, then `count[2]` positions with `2`.

### Solution

```python3
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        count = [0, 0, 0]

        for num in nums:
            count[num] += 1

        idx = 0
        for color in range(3):
            for _ in range(count[color]):
                nums[idx] = color
                idx += 1
```

### Explanation

We use a `count` array of size 3 where `count[i]` holds the frequency of color `i`. In the first loop we tally every element. In the second loop we write back exactly `count[0]` zeros, then `count[1]` ones, then `count[2]` twos, overwriting the original array in place.

### Complexity

| | |
|---|---|
| **Time** | O(n), two separate linear passes |
| **Space** | O(1), only a fixed-size count array of length 3 |


### What's the Problem?

This solution works correctly and is already O(n) in time and O(1) in space. However, it **requires two passes** over the array: one to count, one to rewrite. Interviewers will almost always follow up asking:

> *"Can you do this in a **single pass**?"*

The follow-up is the real test. Two-pass counting sort is the expected "better than naive" answer, but the one-pass Dutch National Flag algorithm is what actually demonstrates mastery of the problem. Moving on...

<br><br>

## Approach 2: Dutch National Flag Algorithm (One-Pass, Optimal)

### Intuition

This is the classic **Dutch National Flag** problem, introduced by computer scientist Edsger W. Dijkstra. The idea is to maintain three pointers that define three regions of the array simultaneously:

```
[0 ... low-1]   -> all 0s (confirmed red zone)
[low ... mid-1] -> all 1s (confirmed white zone)
[mid ... high]  -> unknown / unprocessed
[high+1 ... n-1]-> all 2s (confirmed blue zone)
```

We process elements at `mid` one by one and extend the appropriate boundary, sorting the array in a single left-to-right pass with no extra space.

**Pointer roles:**
- `low`: the boundary of the 0-region. Everything before `low` is a confirmed `0`.
- `mid`: the current element under inspection.
- `high`: the boundary of the 2-region. Everything after `high` is a confirmed `2`.

**Rules at each step (while `mid <= high`):**
- `nums[mid] == 0`: swap `nums[low]` and `nums[mid]`, advance both `low` and `mid`.
- `nums[mid] == 1`: it is already in the right region, just advance `mid`.
- `nums[mid] == 2`: swap `nums[mid]` and `nums[high]`, shrink `high`. Do **not** advance `mid` because the swapped-in element from `high` is unknown and must be inspected next.

### Solution

```python3
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        low = 0
        mid = 0
        high = len(nums) - 1

        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:  # nums[mid] == 2
                nums[high], nums[mid] = nums[mid], nums[high]
                high -= 1
                # mid is NOT incremented here
```

### Explanation (Dry Run)

Let's trace through `nums = [2, 0, 2, 1, 1, 0]`:

```
Initial:  low=0, mid=0, high=5
          [2, 0, 2, 1, 1, 0]

Step 1:   nums[mid]=2 → swap(mid=0, high=5) → [0, 0, 2, 1, 1, 2], high=4
          low=0, mid=0, high=4

Step 2:   nums[mid]=0 → swap(low=0, mid=0) → [0, 0, 2, 1, 1, 2], low=1, mid=1
          low=1, mid=1, high=4

Step 3:   nums[mid]=0 → swap(low=1, mid=1) → [0, 0, 2, 1, 1, 2], low=2, mid=2
          low=2, mid=2, high=4

Step 4:   nums[mid]=2 → swap(mid=2, high=4) → [0, 0, 1, 1, 2, 2], high=3
          low=2, mid=2, high=3

Step 5:   nums[mid]=1 → mid=3
          low=2, mid=3, high=3

Step 6:   nums[mid]=1 → mid=4
          low=2, mid=4, high=3

mid > high → STOP

Result:   [0, 0, 1, 1, 2, 2] ✓
```

**Why not increment `mid` when swapping with `high`?**
When we swap `nums[mid]` with `nums[high]`, the element that lands at `mid` came from the unprocessed right side. Its value is unknown, so we must evaluate it again in the next iteration before advancing `mid`. When we swap with `low`, however, we know `low` holds a `1` (since `mid` has already passed it), so after the swap the element at `mid` is guaranteed to be `1` and we can safely move both pointers forward.

### Complexity

| | |
|---|---|
| **Time** | O(n), single pass through the array |
| **Space** | O(1), only three integer pointers |

<br><br>

## Summary

| Approach | Time | Space | Passes |
|---|---|---|---|
| Counting Sort (Two-Pass) | O(n) | O(1) | 2 |
| Dutch National Flag (One-Pass) | O(n) | O(1) | 1 |

Both approaches are O(n) time and O(1) space. The Dutch National Flag algorithm is the **preferred answer in interviews** because it solves the problem in a single pass, demonstrating a deeper understanding of in-place partitioning. The counting sort approach is a solid stepping-stone answer to show your reasoning before optimizing.

<br><br>

## About the Dutch National Flag Problem

The **Dutch National Flag Problem** is a classic computer science problem formulated by Edsger W. Dijkstra. The name comes from the flag of the Netherlands, which consists of three horizontal bands of color: red, white, and blue, in that order from top to bottom.

Dijkstra used this as an abstract model for a common real-world challenge: given a sequence of elements that each belong to one of three categories, arrange them so all elements of the same category are grouped together, in a fixed predefined order, using only in-place swaps and a single pass.

The core insight of the algorithm is to maintain three pointers (`low`, `mid`, `high`) that together divide the array into four regions at any given moment: a confirmed "low" region on the left, a confirmed "high" region on the right, a growing "middle" region just behind the current pointer, and an unexplored region in between. As `mid` advances, each element is immediately placed into its correct region via a swap, until the unexplored region is exhausted.

Beyond this specific problem, the Dutch National Flag algorithm is a foundational technique that generalizes to any 3-way partitioning scenario, and it also serves as the backbone of 3-way QuickSort, which performs significantly better than standard QuickSort on inputs with many duplicate keys.