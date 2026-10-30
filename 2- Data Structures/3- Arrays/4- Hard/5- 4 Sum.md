# 4Sum

`Amazon` • `Adobe` • `Bloomberg`
<br>

## Problem Statement

Given an array `nums` of `n` integers and an integer `target`, return an array of all the unique quadruplets `[nums[a], nums[b], nums[c], nums[d]]` such that:

- `0 <= a, b, c, d < n`
- `a`, `b`, `c`, and `d` are **distinct**
- `nums[a] + nums[b] + nums[c] + nums[d] == target`

You may return the answer in any order.

**Examples**

**Example 1:**
```
Input:  nums = [1, 0, -1, 0, -2, 2], target = 0
Output: [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
```

**Example 2:**
```
Input:  nums = [2, 2, 2, 2, 2], target = 8
Output: [[2, 2, 2, 2]]
```

**Constraints**
- `1 <= nums.length <= 200`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`

<br><br>

## Approach 1: Brute Force (Four Loops + Set)

**Idea**

Try every possible combination of four indices `(a, b, c, d)`. Sort each quadruplet before storing it in a set so that duplicate orderings are treated as the same quadruplet.

**Steps**
1. Use four nested loops to pick every unique combination of indices.
2. If `nums[a] + nums[b] + nums[c] + nums[d] == target`, sort the quadruplet and add it to a set.
3. Convert the set to a list and return.

**Solution**

```python
class Solution:
    def fourSum(self, nums: list[int], target: int) -> list[list[int]]:
        n = len(nums)
        result = set()

        for a in range(n):
            for b in range(a + 1, n):
                for c in range(b + 1, n):
                    for d in range(c + 1, n):
                        if nums[a] + nums[b] + nums[c] + nums[d] == target:
                            quad = tuple(sorted([nums[a], nums[b], nums[c], nums[d]]))
                            result.add(quad)

        return [list(q) for q in result]
```

**Complexity**

| | |
|---|---|
| Time | O(n^4) |
| Space | O(n) for the result set |

**Problem with this approach**

Four nested loops make this O(n^4). For `n = 200`, this is 1.6 billion operations, which will TLE. We need to eliminate at least one loop.

<br><br>

## Approach 2: Hash Map (Three Loops + Seen Set)

**Idea**

Fix two elements `nums[a]` and `nums[b]` using two outer loops, then reduce the problem to finding two numbers in the remaining portion of the array that sum to `target - nums[a] - nums[b]`. Use a hash set built incrementally (only elements seen so far in the innermost loop) to find the complement in O(1).

**Steps**
1. For each pair of indices `(a, b)`, create an empty set `seen`.
2. For each index `c > b`, compute `complement = target - nums[a] - nums[b] - nums[c]`.
3. If `complement` is in `seen`, we found a valid quadruplet. Sort and add it to the result set.
4. Add `nums[c]` to `seen` and continue.

**Solution**

```python
class Solution:
    def fourSum(self, nums: list[int], target: int) -> list[list[int]]:
        n = len(nums)
        result = set()

        for a in range(n):
            for b in range(a + 1, n):
                seen = set()
                for c in range(b + 1, n):
                    complement = target - nums[a] - nums[b] - nums[c]
                    if complement in seen:
                        quad = tuple(sorted([nums[a], nums[b], nums[c], complement]))
                        result.add(quad)
                    seen.add(nums[c])

        return [list(q) for q in result]
```

**Why build `seen` incrementally?**

If we put all remaining elements in the set upfront, we risk using the same element twice. By adding `nums[c]` to `seen` only after checking the complement, we guarantee the complement came from a strictly earlier position within the innermost loop.

**Complexity**

| | |
|---|---|
| Time | O(n^3) |
| Space | O(n) for `seen` and the result set |

**Problem with this approach**

This is O(n^3) in time, which is correct and will pass given the constraint `n <= 200`. However, the repeated set construction, tuple sorting, and global deduplication via a result set add noticeable constant overhead. We can do better in practice by sorting upfront and using two pointers, which avoids all hashing and deduplicates naturally.

<br><br>

## Approach 3: Sort + Two Pointers (Optimal)

**Idea**

Sort the array. Fix two elements `nums[a]` and `nums[b]` using two outer loops, then use two pointers (`c` at `b+1`, `d` at the end) to find pairs that sum to `target - nums[a] - nums[b]`. Because the array is sorted, we can move pointers intelligently and skip duplicates without any extra data structures.

**Steps**
1. Sort `nums`.
2. For each index `a`, skip it if it is a duplicate of `nums[a-1]`.
3. For each index `b > a`, skip it if it is a duplicate of `nums[b-1]` (and `b > a + 1`).
4. Set `c = b + 1` and `d = len(nums) - 1`.
5. While `c < d`, compute `quad_sum = nums[a] + nums[b] + nums[c] + nums[d]`.
   - If `quad_sum < target`, increment `c` (need a larger value).
   - If `quad_sum > target`, decrement `d` (need a smaller value).
   - If `quad_sum == target`, record the quadruplet, then advance both pointers while skipping duplicates.

**Solution**

```python
class Solution:
    def fourSum(self, nums: list[int], target: int) -> list[list[int]]:
        nums.sort()
        result = []
        n = len(nums)

        for a in range(n - 3):
            # Skip duplicate values for the first fixed element
            if a > 0 and nums[a] == nums[a - 1]:
                continue

            for b in range(a + 1, n - 2):
                # Skip duplicate values for the second fixed element
                if b > a + 1 and nums[b] == nums[b - 1]:
                    continue

                c = b + 1
                d = n - 1

                while c < d:
                    quad_sum = nums[a] + nums[b] + nums[c] + nums[d]

                    if quad_sum < target:
                        c += 1
                    elif quad_sum > target:
                        d -= 1
                    else:
                        result.append([nums[a], nums[b], nums[c], nums[d]])

                        c += 1
                        # Skip duplicates for c
                        while c < d and nums[c] == nums[c - 1]:
                            c += 1

                        d -= 1
                        # Skip duplicates for d
                        while c < d and nums[d] == nums[d + 1]:
                            d -= 1

        return result
```

**Explanation**

**Why `if a > 0 and nums[a] == nums[a - 1]: continue`?**

After sorting, equal values are adjacent. If `nums[a]` equals `nums[a-1]`, we already explored all quadruplets with that fixed first value in the previous iteration. Running it again would produce exact duplicates. The `a > 0` guard prevents an index-out-of-bounds on the first element.

**Why `if b > a + 1 and nums[b] == nums[b - 1]: continue`?**

The same logic applies to the second fixed element. We use `b > a + 1` (rather than `b > 0`) because `b` starts fresh from `a + 1` on every outer iteration, so the very first position for `b` in each outer loop is always valid regardless of what `nums[b]` equals.

**Why skip duplicates for `c` and `d` after finding a quadruplet?**

When we find a valid quadruplet and advance `c` and `d`, if the new `nums[c]` equals the old `nums[c]` (or similarly for `d`), the sum stays equal to target and we would record the same quadruplet again. The inner `while` loops skip past those repeated values to move to genuinely new candidates.

**Complexity**

| | |
|---|---|
| Time | O(n log n) for sorting + O(n^3) for the two outer loops and two-pointer scan = **O(n^3)** |
| Space | O(1) extra space (output list not counted) |

<br><br>

## Summary

| Approach | Time | Space | Notes |
|---|---|---|---|
| Brute Force (4 loops + set) | O(n^4) | O(n) | Too slow for any meaningful input |
| Hash Map (3 loops + seen set) | O(n^3) | O(n) | Correct but has hashing and sorting overhead |
| Sort + Two Pointers | O(n^3) | O(1) | Optimal: no extra structures, clean duplicate handling |