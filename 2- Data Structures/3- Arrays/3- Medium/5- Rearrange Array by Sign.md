# Rearrange Array Elements by Sign

`Amazon` • `Google` • `Microsoft` • `Apple` • `Adobe`

## Problem Statement

You are given a 0-indexed integer array `nums` of even length consisting of an equal number of positive and negative integers.

You should rearrange the elements of `nums` such that the modified array follows the given conditions:

1. Every consecutive pair of integers have opposite signs.
2. For all integers with the same sign, the order in which they were present in `nums` is preserved.
3. The rearranged array begins with a positive integer.

Return the modified array after rearranging the elements to satisfy the aforementioned conditions.

### Examples

**Example 1:**

```
Input: nums = [3,1,-2,-5,2,-4]
Output: [3,-2,1,-5,2,-4]
```

Explanation: The positive integers in `nums` are `[3,1,2]`. The negative integers are `[-2,-5,-4]`. The only possible way to rearrange them such that they satisfy all conditions is `[3,-2,1,-5,2,-4]`. Other arrangements such as `[1,-2,2,-5,3,-4]`, `[3,1,2,-2,-5,-4]`, or `[-2,3,-5,1,-4,2]` are incorrect because they violate one or more of the conditions.

**Example 2:**

```
Input: nums = [-1,1]
Output: [1,-1]
```

Explanation: 1 is the only positive integer and -1 is the only negative integer in `nums`, so `nums` is rearranged to `[1,-1]`.

### Constraints

- `2 <= nums.length <= 2 * 10^5`
- `nums.length` is even
- `1 <= |nums[i]| <= 10^5`
- `nums` consists of an equal number of positive and negative integers

<br><br>

## Approach 1: Separate Lists, Then Merge

### Intuition

The conditions essentially describe a "wave" pattern: positive, negative, positive, negative, and so on, starting with a positive number. Since the relative order within each sign group must be preserved, the most natural first idea is to physically split the array into two groups (one for positives, one for negatives) while walking through `nums` once. Each group keeps the original order of its elements automatically, since we visit elements left to right.

Once we have these two groups, we just need to weave them together: take one element from the positive group, then one from the negative group, then repeat. Since the array is guaranteed to have an equal number of positives and negatives, both groups will run out at exactly the same time.

### Code

```python
class Solution:
    def rearrangeArray(self, nums: List[int]) -> List[int]:
        pos = [num for num in nums if num > 0]
        neg = [num for num in nums if num < 0]

        result = []
        for i in range(len(pos)):
            result.append(pos[i])
            result.append(neg[i])

        return result
```

### Explanation

We make a single pass through `nums` to build two lists, `pos` and `neg`, which preserve the original relative order of positive and negative numbers respectively. Then, since `len(pos) == len(neg)` is guaranteed by the constraints, we iterate over both lists in lockstep, appending `pos[i]` followed by `neg[i]` to the `result` list. This guarantees the array starts with a positive number and alternates signs at every step.

**Time Complexity:** O(n), since we make a constant number of linear passes over the array (one to build `pos` and `neg`, and one to merge them).

**Space Complexity:** O(n), for the `pos`, `neg`, and `result` lists combined.

<br>

### What's the Problem Here?

This solution is correct and runs in linear time, but it isn't the most efficient version possible. We are allocating three separate containers (`pos`, `neg`, and `result`), each of size roughly `n / 2` or `n`. While this is still O(n) asymptotically, the constant factor is higher than necessary, and we are doing more bookkeeping (two list comprehensions plus a final merge loop) than the problem actually requires.

### Can We Do Better?

Yes. Notice that we already know exactly where every element belongs in the final array, the moment we see it:

- If a number is positive, it must go to the next available even index (0, 2, 4, ...), since positives are guaranteed to occupy all even positions in the final array.
- If a number is negative, it must go to the next available odd index (1, 3, 5, ...).

This means we can write directly into a single `result` array of size `n` using two simple counters, without ever building the intermediate `pos` and `neg` lists. This leads to a cleaner, single-pass approach.

<br><br>

## Approach 2: Two Pointers Into a Single Result Array (Optimal)

### Intuition

Since the final array always starts with a positive number and strictly alternates signs, the positions of positive numbers are fixed in advance: they occupy indices `0, 2, 4, ...`. Similarly, negative numbers occupy indices `1, 3, 5, ...`. This is true regardless of the actual values involved, it's purely a consequence of the alternating pattern.

So instead of grouping numbers first and merging afterward, we can place each number directly into its correct slot in a single output array as we encounter it, using two pointers (one for the next even index, one for the next odd index).

### Code

```python
class Solution:
    def rearrangeArray(self, nums: List[int]) -> List[int]:
        result = [0] * len(nums)

        pos_index = 0
        neg_index = 1

        for num in nums:
            if num < 0:
                result[neg_index] = num
                neg_index += 2
            else:
                result[pos_index] = num
                pos_index += 2

        return result
```

### Explanation

We initialize a `result` array of the same length as `nums`, filled with placeholder zeros. We then maintain two pointers:

- `pos_index`, starting at 0, marking the next available slot for a positive number.
- `neg_index`, starting at 1, marking the next available slot for a negative number.

As we iterate through `nums` once, every positive number is placed at `result[pos_index]` and `pos_index` is advanced by 2, while every negative number is placed at `result[neg_index]` and `neg_index` is advanced by 2. Because we process `nums` left to right and never revisit an index, the relative order within each sign group is automatically preserved, exactly as required by condition 2.

Since `result[0]` is always filled by the first positive number processed and `result[1]` is always filled by the first negative number processed, condition 3 (starting with a positive integer) is also automatically satisfied, and condition 1 (alternating signs) follows directly from the even/odd index split.

**Time Complexity:** O(n), as we make exactly one pass through `nums`.

**Space Complexity:** O(n), for the `result` array. This is effectively optimal, since we are required to return a new array of size `n`.

<br>

### Is There Anything Left to Improve?

In terms of time and space complexity, this solution is already optimal for the problem as stated: O(n) time with a single pass, and O(n) space, which is unavoidable since the output itself is an array of size `n`. There is no extra auxiliary data structure beyond the result array, and no wasted work.

<br><br>

## Follow-Up: What About O(1) Extra Space?

A natural interview follow-up question is whether this can be done in-place, using only O(1) extra space (modifying `nums` directly instead of returning a new array).

This is technically possible using a cyclic-replacement technique, where each out-of-place element is rotated into its correct position while shifting the affected elements along the way. However, this comes at a steep cost: because each rotation can touch a large portion of the array, the time complexity degrades to O(n^2) in the worst case.

In practice, this trade-off (O(1) space for O(n^2) time) is almost never worth it for an array that can have up to 2 * 10^5 elements, so the two-pointer, single-result-array approach (Approach 2) remains the recommended and accepted solution.s