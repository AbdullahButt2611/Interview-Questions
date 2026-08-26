# Squares of a Sorted Array

`Google` • `Amazon` • `Adobe` • `Natwest Group` • `Educative`

## Problem Statement
Given an integer array `nums` sorted in non-decreasing order, return an array of the squares of each number, also sorted in non-decreasing order.

## Examples

```ini
Input: nums = [-4,-1,0,3,10]
Output: [0,1,9,16,100]
Explanation: After squaring, the array becomes [16,1,0,9,100].
After sorting, it becomes [0,1,9,16,100].

Input: nums = [-7,-3,2,3,11]
Output: [4,9,9,49,121]
```

## Constraints

* `1 <= nums.length <= 10^4`
* `-10^4 <= nums[i] <= 10^4`
* `nums` is sorted in non-decreasing order.

<br><br>

## Approach 1: Square and Sort (O(n log n))

The most obvious idea that comes to mind:

* Go through the array and square every number.
* Once every number is squared, just sort the whole array.
* Return the sorted result.

This works perfectly and gives the correct answer.

<br>

**So why is this not the best?**

The catch is in the sorting step. Squaring each number takes `O(n)` time, which is fast. But sorting the array afterwards takes `O(n log n)` time, and that becomes the slowest part of our solution.

Here is the important thing we are ignoring: the input array is **already sorted**. When someone hands us a sorted array and we still sort again from scratch, we are throwing away a gift that was given to us for free. A good solution should use that existing order instead of wasting it.

<mark>Whenever the input is already sorted, ask yourself if sorting again is really needed. Most of the time, it is not.</mark>

<br><br>

## Approach 2: Two Pointers (O(n))

Let us think about where the **biggest** squares come from.

* The array is sorted, so the most negative numbers sit on the **left**, and the most positive numbers sit on the **right**.
* A big negative number like `-4` becomes `16` when squared. A big positive number like `10` becomes `100`.
* This means the largest square is always sitting at one of the two ends of the array, never in the middle.

That single observation is the whole trick. If the largest square is always at one end, we can just keep picking the bigger of the two ends and place it in our answer.

<br>

**How we do it in raw form:**

* Create a `result` array of the same size, filled with zeros.
* Put one pointer `left` at the very start of the array and another pointer `right` at the very end.
* We will fill the `result` array from the **back to the front**, because we are finding the biggest values first.
* At each step, compare the absolute values of `nums[left]` and `nums[right]`.
* Whichever one is bigger, square it, place it at the current back position of `result`, and move that pointer inward.
* Keep doing this until both pointers meet and the whole `result` array is filled.

Since we only walk through the array one time and never sort, this runs in clean `O(n)` time.

<br><br>

## Dry Run

Let us trace `nums = [-4,-1,0,3,10]` step by step so you can see exactly what happens.

```ini
nums   = [-4, -1, 0, 3, 10]
result = [0, 0, 0, 0, 0]
left  -> index 0 (value -4)
right -> index 4 (value 10)
We fill result from index 4 down to index 0.

Iteration 1 (i = 4):
  abs(nums[left]) = abs(-4) = 4
  abs(nums[right]) = abs(10) = 10
  10 > 4, so right side wins
  result[4] = 10 * 10 = 100
  move right: right -> index 3
  result = [0, 0, 0, 0, 100]

Iteration 2 (i = 3):
  abs(nums[left]) = abs(-4) = 4
  abs(nums[right]) = abs(3) = 3
  4 > 3, so left side wins
  result[3] = (-4) * (-4) = 16
  move left: left -> index 1
  result = [0, 0, 0, 16, 100]

Iteration 3 (i = 2):
  abs(nums[left]) = abs(-1) = 1
  abs(nums[right]) = abs(3) = 3
  3 > 1, so right side wins
  result[2] = 3 * 3 = 9
  move right: right -> index 2
  result = [0, 0, 9, 16, 100]

Iteration 4 (i = 1):
  abs(nums[left]) = abs(-1) = 1
  abs(nums[right]) = abs(0) = 0
  1 > 0, so left side wins
  result[1] = (-1) * (-1) = 1
  move left: left -> index 2
  result = [0, 1, 9, 16, 100]

Iteration 5 (i = 0):
  left and right both point to index 2 (value 0)
  abs(nums[left]) = 0, abs(nums[right]) = 0
  right side wins (equal case goes to else branch)
  result[0] = 0 * 0 = 0
  move right: right -> index 1
  result = [0, 1, 9, 16, 100]

Final result = [0, 1, 9, 16, 100]
```

<br><br>

## Code

```python
class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        input_size = len(nums)

        result = [0] * input_size
        left = 0
        right = input_size - 1

        for i in range(input_size - 1, -1, -1):
            if abs(nums[left]) > abs(nums[right]):
                result[i] = nums[left] ** 2
                left += 1
            else:
                result[i] = nums[right] ** 2
                right -= 1

        return result
```

<br><br>

## Related Problems

* [Merge Sorted Array (88)](https://leetcode.com/problems/merge-sorted-array/)
* [Two Sum II - Input Array Is Sorted (167)](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
* [Sort Colors (75)](https://leetcode.com/problems/sort-colors/)
* [Remove Duplicates from Sorted Array (26)](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)