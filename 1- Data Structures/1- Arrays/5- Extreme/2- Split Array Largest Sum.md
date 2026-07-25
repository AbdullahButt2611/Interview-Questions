# Split Array Largest Sum

`Amazon` • `Google` • `Apple` • `Meta`

## Problem Statement

Given an integer array `nums` and an integer `k`, split `nums` into `k` non-empty subarrays such that the largest sum of any subarray is minimized.

Return the minimized largest sum of the split.

A subarray is a contiguous part of the array.

## Examples

**Example 1:**

```ini
Input: nums = [7,2,5,10,8], k = 2
Output: 18
Explanation: There are four ways to split nums into two subarrays.
The best way is to split it into [7,2,5] and [10,8], where the largest sum among the two subarrays is only 18.
```

**Example 2:**

```ini
Input: nums = [1,2,3,4,5], k = 2
Output: 9
Explanation: There are four ways to split nums into two subarrays.
The best way is to split it into [1,2,3] and [4,5], where the largest sum among the two subarrays is only 9.
```

## Constraints

* `1 <= nums.length <= 1000`
* `0 <= nums[i] <= 10^6`
* `1 <= k <= min(50, nums.length)`

<br><br>

## Approach

**Think of it like packing boxes.**

Imagine the numbers are items on a conveyor belt in a fixed order, and you have to pack them into exactly `k` boxes. Items must go in order (you cannot rearrange them), and each box holds a run of items sitting next to each other. Every box has the same weight limit. The question is really asking: what is the smallest weight limit that still lets everything fit into `k` boxes?

So instead of trying every possible way to split the array, we simply guess the box limit and check if it works.

**Step 1: Guess a box limit.**

Rather than guessing randomly, notice the guess can only fall in a fixed range:

* It can never be smaller than the biggest single item, because that one item has to fit into some box by itself at minimum. So the lowest guess is `max(nums)`.
* It can never be bigger than the total of all items, because that is the case where everything goes into one single box. So the highest guess is `sum(nums)`.

The best limit sits somewhere between `max(nums)` and `sum(nums)`, so we binary search on that range and repeatedly test the middle value `mid`.

**Step 2: Check if a guessed limit works.**

For a given limit `mid`, we just walk through the items once and greedily fill the current box:

* Keep dropping items into the current box while the running weight stays at or below `mid`.
* If the next item would push the box over `mid`, close that box, open a fresh one, and put the item there. That is one more box used.
* When we reach the end, we know how many boxes this limit needed.

For example, with items `[7, 2, 5, 10, 8]` and a limit of `18`: we fill `7 + 2 + 5 = 14` (still fine), adding `10` would make `24` (too heavy, so start box two), then `10 + 8 = 18` (exactly fits). That used `2` boxes.

**Step 3: Adjust the guess.**

* If the number of boxes used is `k` or fewer, the limit is comfortable. It works, so we save it as a possible answer and then try an even tighter limit to see if we can do better (move `high` down to `mid - 1`).
* If it used more than `k` boxes, the limit was too tight. We need to loosen it (move `low` up to `mid + 1`).

We keep narrowing the range until `low` passes `high`, and the last limit that worked is our answer.

<mark>Key intuition: a bigger limit means fewer boxes, and a smaller limit means more boxes. This steady one-directional pattern is exactly what lets binary search zero in on the answer.</mark>

<br><br>

## Code

```python
class Solution:
    def calculateSplits(self, nums, hold_value):
        splits = 1
        curr_hold = nums[0]

        for i in range(1, len(nums)):
            if curr_hold + nums[i] > hold_value:
                splits += 1
                curr_hold = nums[i]
            else:
                curr_hold += nums[i]
        
        return splits

    def splitArray(self, nums: List[int], k: int) -> int:
        low = max(nums)
        high = sum(nums)
        ans = float('inf')

        while low <= high:
            mid = (low + high) // 2
            splits = self.calculateSplits(nums, mid)

            if splits <= k:
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        
        return ans
```

<br><br>

## Dry Run

```ini
nums = [7, 2, 5, 10, 8]   k = 2

Initial search space:
low  = max(nums) = 10
high = sum(nums) = 7 + 2 + 5 + 10 + 8 = 32
ans  = infinity


Iteration 1:
low = 10, high = 32
mid = (10 + 32) // 2 = 21

  Count splits with max allowed sum = 21:
  splits = 1, curr_hold = 7            (start with first element)
  i=1 -> 7 + 2 = 9    <= 21  -> keep, curr_hold = 9
  i=2 -> 9 + 5 = 14   <= 21  -> keep, curr_hold = 14
  i=3 -> 14 + 10 = 24 >  21  -> cut,  splits = 2, curr_hold = 10
  i=4 -> 10 + 8 = 18  <= 21  -> keep, curr_hold = 18
  splits = 2

  splits (2) <= k (2)  ->  21 works
  Record ans = 21, shrink from the right: high = mid - 1 = 20


Iteration 2:
low = 10, high = 20
mid = (10 + 20) // 2 = 15

  Count splits with max allowed sum = 15:
  splits = 1, curr_hold = 7
  i=1 -> 7 + 2 = 9    <= 15  -> keep, curr_hold = 9
  i=2 -> 9 + 5 = 14   <= 15  -> keep, curr_hold = 14
  i=3 -> 14 + 10 = 24 >  15  -> cut,  splits = 2, curr_hold = 10
  i=4 -> 10 + 8 = 18  >  15  -> cut,  splits = 3, curr_hold = 8
  splits = 3

  splits (3) > k (2)  ->  15 is too small
  Need a bigger sum: low = mid + 1 = 16


Iteration 3:
low = 16, high = 20
mid = (16 + 20) // 2 = 18

  Count splits with max allowed sum = 18:
  splits = 1, curr_hold = 7
  i=1 -> 7 + 2 = 9    <= 18  -> keep, curr_hold = 9
  i=2 -> 9 + 5 = 14   <= 18  -> keep, curr_hold = 14
  i=3 -> 14 + 10 = 24 >  18  -> cut,  splits = 2, curr_hold = 10
  i=4 -> 10 + 8 = 18  <= 18  -> keep, curr_hold = 18
  splits = 2

  splits (2) <= k (2)  ->  18 works
  Record ans = 18, shrink from the right: high = mid - 1 = 17


Iteration 4:
low = 16, high = 17
mid = (16 + 17) // 2 = 16

  Count splits with max allowed sum = 16:
  splits = 1, curr_hold = 7
  i=1 -> 7 + 2 = 9    <= 16  -> keep, curr_hold = 9
  i=2 -> 9 + 5 = 14   <= 16  -> keep, curr_hold = 14
  i=3 -> 14 + 10 = 24 >  16  -> cut,  splits = 2, curr_hold = 10
  i=4 -> 10 + 8 = 18  >  16  -> cut,  splits = 3, curr_hold = 8
  splits = 3

  splits (3) > k (2)  ->  16 is too small
  Need a bigger sum: low = mid + 1 = 17


Iteration 5:
low = 17, high = 17
mid = (17 + 17) // 2 = 17

  Count splits with max allowed sum = 17:
  splits = 1, curr_hold = 7
  i=1 -> 7 + 2 = 9    <= 17  -> keep, curr_hold = 9
  i=2 -> 9 + 5 = 14   <= 17  -> keep, curr_hold = 14
  i=3 -> 14 + 10 = 24 >  17  -> cut,  splits = 2, curr_hold = 10
  i=4 -> 10 + 8 = 18  >  17  -> cut,  splits = 3, curr_hold = 8
  splits = 3

  splits (3) > k (2)  ->  17 is too small
  Need a bigger sum: low = mid + 1 = 18


Loop ends:
low = 18, high = 17  ->  low > high, stop.

Final Answer = ans = 18
```

<br><br>

## Complexity

* **Time:** `O(n * log(sum(nums) - max(nums)))`. For every value we guess in the binary search range, we do one full pass over the array of `n` elements.
* **Space:** `O(1)`. We only use a few counters and pointers, no extra data structures.

<br><br>

## Related Problems

* [Book Allocation Problem](https://github.com/AbdullahButt2611/Interview-Questions/blob/main/1-%20Data%20Structures/1-%20Arrays/5-%20Extreme/1-%20Book%20Allocation%20Problem.md)