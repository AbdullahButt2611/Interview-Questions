# Longest Subarray with given Sum K (Positives)

`Arcesium` • `Citadel Securities` • `UKG`

**Topic:** Prefix Sum

<br>

## Problem Statement

You are given an array `nums` of size `n` containing only positive integers, and an integer `k`.

Find the length of the longest sub-array whose elements add up exactly to `k`. If no such sub-array exists, return `0`.

### Examples

**Example 1:**
```
Input: nums = [10, 5, 2, 7, 1, 9], k = 15
Output: 4
Explanation: The sub-array [5, 2, 7, 1] sums to 15 and has length 4. No longer sub-array sums to 15.
```

**Example 2:**
```
Input: nums = [-3, 2, 1], k = 6
Output: 0
Explanation: No sub-array sums to 6, so the output is 0.
```

### Constraints
```
1 <= n <= 10^5
1 <= nums[i] <= 10^9
1 <= k <= 10^9
```

<br><br>

## Approach 1: Brute Force (Three Loops)

The most basic idea is to try every possible sub-array, and for each one, add up its elements from scratch to check if the sum equals `k`. While doing this, keep track of the longest length found.

To do this, pick a starting index `i`, pick an ending index `j`, and then use a third loop to walk from `i` to `j` and add up every element in between. If this sum equals `k`, compare the length `(j - i + 1)` with the best length found so far.

### Code

```python
def longest_subarray(nums, k):
    n = len(nums)
    max_len = 0

    for i in range(n):
        for j in range(i, n):
            total = 0
            for x in range(i, j + 1):
                total += nums[x]
            if total == k:
                max_len = max(max_len, j - i + 1)
    return max_len
```

### Complexity
- **Time:** O(n³), since for every pair of `(i, j)` we use a third loop to compute the sum from scratch.
- **Space:** O(1), no extra space is used.

### What's the problem here?

We are recalculating the sum of the same elements again and again, even though most of the work overlaps with the previous sub-array we just checked. There is no need for that third loop at all, we can carry the sum forward instead of recomputing it every time.

<br><br>

## Approach 2: Brute Force with Running Sum (Two Loops)

We can remove the third loop entirely by keeping a running sum as we extend the sub-array. Instead of recomputing the sum from `i` to `j` every time, we add just the new element `nums[j]` to the existing sum.

We still pick a starting index `i`, but now instead of a separate inner loop to compute the sum, we extend `j` one step at a time and keep adding `nums[j]` directly to a running total. Whenever this total equals `k`, we update the maximum length.

### Code

```python
def longest_subarray(nums, k):
    n = len(nums)
    max_len = 0

    for i in range(n):
        total = 0
        for j in range(i, n):
            total += nums[j]
            if total == k:
                max_len = max(max_len, j - i + 1)
    return max_len
```

### Complexity
- **Time:** O(n²), since we now only use two nested loops, and each element is added to the running sum exactly once per starting index `i`.
- **Space:** O(1), no extra space is used.

### What's the problem here?

This is much better than before, but for large arrays (n up to 10^5), an O(n²) solution will still time out. We are still repeating work across different starting points `i`, since the sums of overlapping ranges are still being recalculated separately for every `i`. We need a way to reuse the total sum information across all starting points at once.

<br><br>

## Approach 3: Prefix Sum with HashMap (Single Pass)

This approach is based on prefix sums and works for any integers, including negative numbers, making it a more general technique to know.

If `prefixSum[j]` is the sum of all elements from index `0` to `j`, then the sum of any sub-array from index `i+1` to `j` is simply `prefixSum[j] - prefixSum[i]`.

We want this difference to equal `k`, which means:
```
prefixSum[j] - k = prefixSum[i]
```

So, while traversing the array and building the running sum, we check if `(currentSum - k)` has been seen before as a prefix sum. If it has, the sub-array between that earlier index and the current index sums to `k`. We store only the **first occurrence** of each prefix sum in a hashmap, because using the earliest index gives the longest possible sub-array.

### Code

```python
def longest_subarray(nums, k):
    first_index = {}
    total = 0
    max_len = 0

    for i, num in enumerate(nums):
        total += num

        if total == k:
            max_len = max(max_len, i + 1)

        if (total - k) in first_index:
            max_len = max(max_len, i - first_index[total - k])

        if total not in first_index:
            first_index[total] = i
    return max_len
```

### Complexity
- **Time:** O(n), since each element is visited once and hashmap operations are O(1) on average.
- **Space:** O(n), for storing prefix sums in the hashmap.

<br><br>

## Summary

| Approach | Time | Space | Notes |
|---|---|---|---|
| Brute Force (Three Loops) | O(n³) | O(1) | Recomputes the sum from scratch every time |
| Brute Force (Running Sum) | O(n²) | O(1) | Carries the sum forward, avoids the third loop |
| Prefix Sum + HashMap | O(n) | O(n) | Most efficient, works for positives and negatives |