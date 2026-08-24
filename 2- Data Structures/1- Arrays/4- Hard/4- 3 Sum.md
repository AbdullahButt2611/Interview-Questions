# 3Sum

`Amazon` • `Google` • `Meta` • `Microsoft` • `Apple` • `Adobe` • `Bloomberg` • `Uber` • `Goldman Sachs`
<br>

## Problem Statement

Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.

The solution set must **not** contain duplicate triplets.

**Examples**

**Example 1:**
```
Input:  nums = [-1, 0, 1, 2, -1, -4]
Output: [[-1, -1, 2], [-1, 0, 1]]
```

**Example 2:**
```
Input:  nums = [0, 1, 1]
Output: []
```

**Example 3:**
```
Input:  nums = [0, 0, 0]
Output: [[0, 0, 0]]
```

**Constraints**
- `3 <= nums.length <= 3000`
- `-10^5 <= nums[i] <= 10^5`

<br><br>

## Approach 1: Brute Force (Three Loops + Set)

**Idea**

Try every possible combination of three indices `(i, j, k)`. Sort each triplet before storing it in a set so that duplicate orderings (e.g. `[-1, 0, 1]` and `[1, 0, -1]`) are treated as the same triplet.

**Steps**
1. Use three nested loops to pick every triplet.
2. If `nums[i] + nums[j] + nums[k] == 0`, sort the triplet and add it to a set.
3. Convert the set to a list and return.

**Solution**

```python
class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        n = len(nums)
        result = set()

        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if nums[i] + nums[j] + nums[k] == 0:
                        triplet = tuple(sorted([nums[i], nums[j], nums[k]]))
                        result.add(triplet)

        return [list(t) for t in result]
```

**Complexity**

| | |
|---|---|
| Time | O(n^3) |
| Space | O(n) for the result set |

**Problem with this approach**

Three nested loops make this O(n^3). For `n = 3000`, this is 27 billion operations, which will TLE. We need to eliminate one loop.

<br><br>

## Approach 2: Hash Map (Two Loops + Set)

**Idea**

Fix one element `nums[i]`, then reduce the problem to finding two numbers in the rest of the array that sum to `-nums[i]`. Use a hash set built incrementally (only elements seen so far in the inner loop) to find the complement in O(1). This avoids accidentally reusing the same element.

**Steps**
1. For each index `i`, create an empty set `seen`.
2. For each index `j > i`, compute `complement = -nums[i] - nums[j]`.
3. If `complement` is in `seen`, we found a valid triplet. Sort and add to the result set.
4. Add `nums[j]` to `seen` and continue.

**Solution**

```python
class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        n = len(nums)
        result = set()

        for i in range(n):
            seen = set()
            for j in range(i + 1, n):
                complement = -nums[i] - nums[j]
                if complement in seen:
                    triplet = tuple(sorted([nums[i], nums[j], complement]))
                    result.add(triplet)
                seen.add(nums[j])

        return [list(t) for t in result]
```

**Why build `seen` incrementally?**

If we put all elements in the set upfront, we risk using the same element twice. By adding `nums[j]` to `seen` only after checking the complement, we guarantee the complement came from a strictly earlier position.

**Complexity**

| | |
|---|---|
| Time | O(n^2) |
| Space | O(n) for `seen` and the result set |

**Problem with this approach**

This is O(n^2) in time, which is correct. However, the repeated set construction, tuple sorting, and global deduplication via a result set add constant overhead. We can do better in practice by sorting upfront and using two pointers, which avoids all hashing and deduplicates naturally.

<br><br>

## Approach 3: Sort + Two Pointers (Optimal)

**Idea**

Sort the array. Fix one element `nums[i]` and use two pointers (`j` at `i+1`, `k` at the end) to find pairs that sum to `-nums[i]`. Because the array is sorted, we can move pointers intelligently and skip duplicates without any extra data structures.

**Steps**
1. Sort `nums`.
2. For each index `i`, set `j = i + 1` and `k = len(nums) - 1`.
3. While `j < k`, compute `tri_sum = nums[i] + nums[j] + nums[k]`.
   - If `tri_sum < 0`, increment `j` (need a larger value).
   - If `tri_sum > 0`, decrement `k` (need a smaller value).
   - If `tri_sum == 0`, record the triplet, then advance both pointers while skipping duplicates.
4. Skip duplicate values of `nums[i]` in the outer loop to avoid repeating the same fixed element.

**Solution**

```python
class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        result = []

        for i in range(len(nums)):
            # Skip duplicate values for the fixed element
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            j = i + 1
            k = len(nums) - 1

            while j < k:
                tri_sum = nums[i] + nums[j] + nums[k]

                if tri_sum < 0:
                    j += 1
                elif tri_sum > 0:
                    k -= 1
                else:
                    result.append([nums[i], nums[j], nums[k]])

                    j += 1
                    # Skip duplicates for j
                    while j < k and nums[j] == nums[j - 1]:
                        j += 1

                    k -= 1
                    # Skip duplicates for k
                    while j < k and nums[k] == nums[k + 1]:
                        k -= 1

        return result
```

**Explanation**

**Why `if i > 0 and nums[i] == nums[i - 1]: continue`?**

After sorting, equal values are adjacent. If `nums[i]` is the same as `nums[i-1]`, we already explored all triplets with that fixed value in the previous iteration. Running it again would produce exact duplicates in the result. The `i > 0` guard prevents an index-out-of-bounds on the first element.

**Why skip duplicates for `j` and `k` after finding a triplet?**

When we find a valid triplet and advance `j` and `k`, if the new `nums[j]` equals the old `nums[j]` (or similarly for `k`), the sum stays zero and we would record the same triplet again. The inner `while` loops skip past those repeated values to move to genuinely new candidates.

**Why do we only need to check duplicates for `j` (not `k` separately)?**

Since `nums[i]` is already deduplicated by the outer check, and `j` is deduplicated by its own while loop, `k` is implicitly forced to a unique position because the three values together must sum to zero. Skipping `k` duplicates is still done for correctness and efficiency, but the outer two checks are the critical ones.

**Complexity**

| | |
|---|---|
| Time | O(n log n) for sorting + O(n^2) for the two-pointer scan = **O(n^2)** |
| Space | O(1) extra space (output list not counted) |

<br><br>

## Summary

| Approach | Time | Space | Notes |
|---|---|---|---|
| Brute Force (3 loops + set) | O(n^3) | O(n) | Too slow for large inputs |
| Hash Map (2 loops + seen set) | O(n^2) | O(n) | Correct but has hashing overhead |
| Sort + Two Pointers | O(n^2) | O(1) | Optimal: no extra structures, clean duplicate handling |