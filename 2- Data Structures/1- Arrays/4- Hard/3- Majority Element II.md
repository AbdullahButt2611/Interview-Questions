# Majority Element II

`Amazon` • `Apple` • `Bloomberg` • `Facebook` • `Google` • `Microsoft` • `Uber`<br>

## Problem Statement

Given an integer array of size `n`, find all elements that appear more than `⌊n / 3⌋` times.

**Examples**

```
Input: nums = [3,2,3]
Output: [3]

Input: nums = [1]
Output: [1]

Input: nums = [1,2]
Output: [1,2]
```

**Constraints**
- `1 <= nums.length <= 5 * 10^4`
- `-10^9 <= nums[i] <= 10^9`

**Follow-up:** Can you solve this in linear time and O(1) space?

<br><br>

## Intuition

Before jumping into solutions, ask yourself: how many elements can possibly appear more than `⌊n / 3⌋` times?

If even 3 elements each appeared more than `⌊n / 3⌋` times, their combined count would exceed `n`, which is impossible. So the answer is at most **2** elements, and the minimum is **0**.

This is the key observation that all approaches build on.

<br><br>

## Approach 1: Brute Force

**Intuition**

For every element in the array, count how many times it appears. If the count exceeds `⌊n / 3⌋`, add it to the result. Before counting, we check if `num` is already in `res`. If it is, we skip it entirely so we never do redundant work for the same value twice.

**Solution**

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = []

        for num in nums:
            if num in res:
                continue

            count = 0
            for x in nums:
                if x == num:
                    count += 1
            if count > n // 3:
                res.append(num)

        return res
```

**Complexity**
- Time: O(n^2), for each element we scan the entire array
- Space: O(1), only the result list with no extra data structures

**Problem with this approach**

We are doing a full scan of the array for each element, leading to O(n^2) time. For large inputs (n = 50,000), this becomes too slow. We can do better by counting everything in a single pass using a hash map.

<br><br>

## Approach 2: Hash Map (Two Passes)

**Intuition**

Count the frequency of every element in one pass using a hash map. Then, in a second pass over the map, collect all elements whose count exceeds `⌊n / 3⌋`.

**Solution**

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> List[int]:
        count = {}
        n = len(nums)

        for num in nums:
            count[num] = count.get(num, 0) + 1

        res = []
        for num, cnt in count.items():
            if cnt > n // 3:
                res.append(num)

        return res
```

**Complexity**
- Time: O(2n) = O(n), one pass to build the map and one pass over the map entries
- Space: O(n), the hash map can hold up to n distinct elements

**Problem with this approach**

This is already O(n) time, but it uses O(n) extra space for the hash map. The follow-up asks us to solve this in O(1) space. We need a smarter method that tracks candidates without storing every element.

<br><br>

## Approach 3: Hash Map (Single Pass)

**Intuition**

We can collapse the two passes into one. Build the frequency map and check the threshold in the same loop.

**Solution**

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> List[int]:
        count = {}
        n = len(nums)
        res = []

        for num in nums:
            count[num] = count.get(num, 0) + 1
            if count[num] == n // 3 + 1:
                res.append(num)

        return res
```

> We check `== n // 3 + 1` (exactly when the count first crosses the threshold) so each qualifying element is added only once, avoiding duplicates without needing a set.

**Complexity**
- Time: O(n), single pass
- Space: O(n), still using a hash map

**Problem with this approach**

Both hash map approaches are O(n) in space. Since we know at most 2 elements can qualify, there is no need to track every element. The Boyer-Moore Voting Algorithm achieves this with just two variables.

<br><br>

## Approach 4: Boyer-Moore Voting Algorithm (Optimal)

**Intuition**

Since at most 2 elements can appear more than `⌊n / 3⌋` times, we maintain two candidates with their respective vote counts. As we scan:

- If the current number matches a candidate, increment that candidate's count.
- If a candidate slot is empty (count = 0), assign this number to that slot.
- Otherwise, decrement both counts (a non-candidate element "cancels out" one occurrence from each candidate).

After the first pass, the two candidates are not guaranteed winners yet. They are just survivors of the cancellation process. A second pass verifies their actual counts.

**Solution**

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> List[int]:
        element1, count1 = None, 0
        element2, count2 = None, 0

        # First pass: find the two candidates
        for num in nums:
            if count1 == 0 and num != element2:
                element1, count1 = num, 1
            elif count2 == 0 and num != element1:
                element2, count2 = num, 1
            elif num == element1:
                count1 += 1
            elif num == element2:
                count2 += 1
            else:
                count1 -= 1
                count2 -= 1

        # Second pass: verify actual counts
        count1 = count2 = 0
        for num in nums:
            if num == element1:
                count1 += 1
            elif num == element2:
                count2 += 1

        res = []
        n_by_3 = len(nums) // 3

        if count1 > n_by_3:
            res.append(element1)
        if count2 > n_by_3:
            res.append(element2)

        return res
```

**Walkthrough on `[1, 1, 1, 3, 3, 2, 2, 2]`**

| num | element1 | count1 | element2 | count2 |
|-----|----------|--------|----------|--------|
| 1   | 1        | 1      | None     | 0      |
| 1   | 1        | 2      | None     | 0      |
| 1   | 1        | 3      | None     | 0      |
| 3   | 1        | 3      | 3        | 1      |
| 3   | 1        | 3      | 3        | 2      |
| 2   | 1        | 2      | 3        | 1      |
| 2   | 1        | 1      | 3        | 0      |
| 2   | 1        | 1      | 2        | 1      |

Candidates after first pass: `1` and `2`. Second pass confirms both appear more than `8 // 3 = 2` times. Result: `[1, 2]`.

**Complexity**
- Time: O(2n) = O(n), two linear passes
- Space: O(1), only four variables regardless of input size

<br><br>

## Summary

| Approach | Time | Space |
|---|---|---|
| Brute Force | O(n^2) | O(1) |
| Hash Map (Two Passes) | O(2n) | O(n) |
| Hash Map (Single Pass) | O(n) | O(n) |
| Boyer-Moore Voting | O(2n) | O(1) |

<br><br>

## Why `num != element2` and `num != element1`?

These guards prevent the same element from being assigned to both candidate slots simultaneously.

Consider the array `[2, 2, 2]` without these guards.

**Without the guards, step by step:**

| num | Condition checked | What happens |
|-----|-------------------|--------------|
| 2   | count1 == 0? Yes  | element1 = 2, count1 = 1 |
| 2   | count1 == 0? No. count2 == 0? Yes | element2 = 2, count2 = 1 |
| 2   | num == element1? Yes | count1 = 2 |

After this, both `element1` and `element2` are `2`. The second pass now double-counts every occurrence of `2`, once for `element1` and once for `element2`. This inflates counts and can push a non-qualifying element into the result in other scenarios.

**With the guards:**

| num | Condition checked | What happens |
|-----|-------------------|--------------|
| 2   | count1 == 0 and 2 != element2 (None)? Yes | element1 = 2, count1 = 1 |
| 2   | count1 == 0? No. Goes to elif num == element1? Yes | count1 = 2 |
| 2   | count1 == 0? No. Goes to elif num == element1? Yes | count1 = 3 |

Now `element2` stays `None` and only `element1` tracks `2` correctly. The second pass counts it once and produces the right result `[2]`.

The same logic applies to `num != element1` on the second condition. If `element1` was just filled but `count2` happens to be `0` at the same step, we do not want the same number claiming the second slot too.