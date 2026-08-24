# Length of the Longest Subarray with Zero Sum

`HashedIn by Deloitte`

<br>

## Problem Statement

Given an array containing both positive and negative integers, find the length of the longest sub-array whose elements sum up to zero.

### Examples

**Example 1:**
```
Input: N = 6, array[] = {9, -3, 3, -1, 6, -5}
Result: 5
Explanation: Subarrays summing to zero are {-3, 3}, {-1, 6, -5}, and {-3, 3, -1, 6, -5}.
The longest one has length 5.
```

**Example 2:**
```
Input: N = 8, array[] = {6, -2, 2, -8, 1, 7, 4, -10}
Result: 8
Explanation: Subarrays summing to zero include {-2, 2}, {-8, 1, 7}, {-2, 2, -8, 1, 7}, and the entire array.
The longest one has length 8.
```

### Constraints
```
1 <= N <= 10^5
-10^9 <= array[i] <= 10^9
```

<br><br>

## Approach 1: Brute Force (Three Loops)

The most basic idea is to try every possible sub-array, and for each one, add up its elements from scratch to check if the sum equals zero. While doing this, keep track of the longest length found.

To do this, pick a starting index `i`, pick an ending index `j`, and then use a third loop to walk from `i` to `j` and add up every element in between. If this sum equals zero, compare the length `(j - i + 1)` with the best length found so far.

### Code

```python
def longest_zero_sum_subarray(arr):
    n = len(arr)
    max_len = 0

    for i in range(n):
        for j in range(i, n):
            total = 0
            for x in range(i, j + 1):
                total += arr[x]
            if total == 0:
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

We can remove the third loop entirely by keeping a running sum as we extend the sub-array. Instead of recomputing the sum from `i` to `j` every time, we add just the new element `arr[j]` to the existing sum.

We still pick a starting index `i`, but now instead of a separate inner loop to compute the sum, we extend `j` one step at a time and keep adding `arr[j]` directly to a running total. Whenever this total equals zero, we update the maximum length.

### Code

```python
def longest_zero_sum_subarray(arr):
    n = len(arr)
    max_len = 0

    for i in range(n):
        total = 0
        for j in range(i, n):
            total += arr[j]
            if total == 0:
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

This approach is based on prefix sums. If `prefixSum[j]` is the sum of all elements from index `0` to `j`, then the sum of any sub-array from index `i+1` to `j` is simply `prefixSum[j] - prefixSum[i]`.

We want this difference to equal zero, which means:
```
prefixSum[j] = prefixSum[i]
```

In other words, if the same prefix sum value shows up at two different indices, then the elements between those two indices must add up to zero. So, while traversing the array and building the running sum, we check if the current sum has been seen before. If it has, the sub-array between that earlier index and the current index sums to zero. We store only the **first occurrence** of each prefix sum in a hashmap, because using the earliest index gives the longest possible sub-array.

We also insert `{0: -1}` into the hashmap before starting. This handles the case where the running sum itself becomes zero at some index, meaning the sub-array from the very start up to that index sums to zero.

### Code

```python
def longest_zero_sum_subarray(arr):
    first_index = {0: -1}
    total = 0
    max_len = 0

    for i, num in enumerate(arr):
        total += num

        if total in first_index:
            max_len = max(max_len, i - first_index[total])
        else:
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
| Prefix Sum + HashMap | O(n) | O(n) | Most efficient, uses repeated prefix sums to detect zero sum sub-arrays |