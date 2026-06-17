# Next Permutation

`Adobe` • `Amazon` • `Apple` • `Bloomberg` • `ByteDance` • `eBay` • `Facebook` • `Google` • `Microsoft` • `Quora` • `Rubrik` • `Sumo Logic` • `Uber`
<br>
## Problem Statement

A permutation is just one possible way to arrange the numbers in an array.

For example, for `arr = [1,2,3]`, here are all the possible permutations: `[1,2,3]`, `[1,3,2]`, `[2,1,3]`, `[2,3,1]`, `[3,1,2]`, `[3,2,1]`.

Now imagine you line up all the permutations of an array in order, from smallest to largest (the way words are sorted in a dictionary). The "next permutation" is simply the one that comes right after the current arrangement in that ordered list.

If the current arrangement is already the biggest one possible, then there is nothing bigger to go to. In that case, we go back to the smallest arrangement, which is the array sorted in ascending order.

A few examples to make this clear:

- The next permutation of `[1,2,3]` is `[1,3,2]`.
- The next permutation of `[2,3,1]` is `[3,1,2]`.
- The next permutation of `[3,2,1]` is `[1,2,3]`, because `[3,2,1]` is already the largest arrangement, so we wrap around to the smallest one.

Given an array of integers `nums`, find its next permutation.

You must do this in place, meaning you should change `nums` directly and not use extra arrays to store the answer.

Example 1:
```
Input: nums = [1,2,3]
Output: [1,3,2]
```

Example 2:
```
Input: nums = [3,2,1]
Output: [1,2,3]
```

Example 3:
```
Input: nums = [1,1,5]
Output: [1,5,1]
```

Constraints:
- `1 <= nums.length <= 100`
- `0 <= nums[i] <= 100`

<br><br>

## Approach 1: Brute Force (Generate All Permutations)

### Intuition

The simplest way to think about this problem is to do exactly what it describes, step by step.

List out every possible arrangement of the array, put them in sorted order, find where our current array sits in that list, and then pick the one right after it. If our array is the last one in the list, we just pick the first one instead.

This is the easiest way to understand the problem, but it is not a good solution in practice. We will look at why after seeing the code.

### Steps

1. Create every possible arrangement of `nums`. If there are repeated numbers, make sure we do not count the same arrangement twice.
2. Sort all these arrangements from smallest to largest.
3. Find the position of our current array in this sorted list.
4. If our array is the last one in the list, the answer is the first (smallest) arrangement.
5. Otherwise, the answer is the arrangement that comes right after our current one.
6. Copy this answer back into `nums`.

### Code

```python3
from itertools import permutations
from typing import List

class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        all_perms = sorted(set(permutations(nums)))
        current = tuple(nums)

        index = all_perms.index(current)
        next_index = (index + 1) % len(all_perms)

        nums[:] = list(all_perms[next_index])
```

### Complexity

- Time complexity: `O(n! * n log(n!))`. There are `n!` possible arrangements, and sorting all of them takes a lot of extra time on top of that.
- Space complexity: `O(n! * n)`, because we are storing every single arrangement in memory.

### Why This Approach Is Not Good Enough

There are two big issues here.

The first issue is speed and memory. The number of arrangements grows extremely fast as the array gets bigger, so this approach becomes too slow and uses too much memory very quickly, even for arrays that are not that large.

The second issue is that the problem asks us to solve this using only constant extra memory. Storing a huge list of every possible arrangement breaks this rule completely, no matter how fast or slow it is.

So instead of generating every arrangement, we need a smarter way to jump directly to the next one by just looking at the array itself.

<br><br>

## Approach 2: Two Pointers (Optimal)

### Intuition

Here is a simple way to think about it. Imagine the array is a number, and we want to find the next bigger number using the same digits.

For example, if you have `129` and want the next bigger number using the digits `1`, `2`, `9`, you would look from the right side for the first digit that can be made bigger by swapping it with something to its right. Then you would arrange everything after that digit to be as small as possible.

We do the same thing here, but with array elements instead of digits.

Start from the right side of the array and look for the first position where the value is smaller than the value right after it. Call this position `i`. Everything to the right of `i` is currently arranged from largest to smallest, which means that part of the array is already at its biggest possible value and cannot be increased any further on its own.

To get the next permutation, we need to slightly increase the value at position `i`, and then make everything after it as small as possible.

If we cannot find any such position `i`, that means the whole array is arranged from largest to smallest, which is the biggest possible arrangement. In that case, there is no next permutation, so we simply flip the whole array around to get the smallest arrangement.

### Steps

1. Starting from the second to last position and moving left, find the first index `i` where `nums[i]` is smaller than `nums[i + 1]`.
2. If no such index exists, the array is already in its largest possible order. Reverse the whole array and we are done.
3. Otherwise, look from the right side of the array back toward `i`, and find the first value that is bigger than `nums[i]`. Since the part after `i` is arranged from largest to smallest, this will be the smallest value that is still bigger than `nums[i]`.
4. Swap `nums[i]` with this value. This gives us the smallest possible increase at position `i`.
5. Reverse everything after position `i`. Since that part was arranged from largest to smallest before the swap, flipping it makes it go from smallest to largest, which is exactly what we want for the next permutation.

### Code

```python3
from typing import List

class Solution:
    def reverse_array_inplace(self, arr, start, end):
        while start < end:
            arr[start], arr[end] = arr[end], arr[start]
            start += 1
            end -= 1
        return arr

    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        index = -1

        for i in range(len(nums) - 2, -1, -1):
            if nums[i] < nums[i + 1]:
                index = i
                break

        if index == -1:
            self.reverse_array_inplace(nums, 0, len(nums) - 1)
        else:
            for i in range(len(nums) - 1, -1, -1):
                if nums[i] > nums[index]:
                    nums[i], nums[index] = nums[index], nums[i]
                    break

            self.reverse_array_inplace(nums, index + 1, len(nums) - 1)
```

### Complexity

- Time complexity: `O(n)`. We go through the array a small number of times, one after another, never inside one another.
- Space complexity: `O(1)`. We only use a few extra variables, and we change the array directly without creating new ones.

### Walkthrough Example

Let's go through `nums = [1, 3, 5, 4, 2]` step by step.

We scan from the right side. `4 < 2` is false, `5 < 4` is false, but `3 < 5` is true. So `i = 1`, and `nums[1] = 3`.

The part after `i`, which is `[5, 4, 2]`, is arranged from largest to smallest, just as we expected.

Now we scan from the right again, looking for the first value bigger than `3`. That value is `4`, at index `3`.

We swap `nums[1]` and `nums[3]`. The array becomes `[1, 4, 5, 3, 2]`.

Finally, we reverse everything after index `1`, turning `[5, 3, 2]` into `[2, 3, 5]`.

The final result is `[1, 4, 2, 3, 5]`, which is the next permutation of `[1, 3, 5, 4, 2]`.

### Why This Approach Works

This approach checks every box. It runs in linear time, uses only a constant amount of extra memory, and correctly handles the case where the array is already the largest arrangement. It also works fine with repeated numbers, like `[1, 1, 5]`, since we only compare values using strict "smaller than" and "bigger than" checks. This makes it the best and accepted solution for this problem.