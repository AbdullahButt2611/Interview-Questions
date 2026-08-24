# Median of Two Sorted Arrays I

`Amazon` • `Google` • `Microsoft` • `Apple` • `Meta`

## Problem Statement

- You are given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively.
- Return the **median** of the two sorted arrays.

## Examples

**Example 1**

```ini
Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.
```

**Example 2**

```ini
Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
```

## Constraints

- `nums1.length == m`
- `nums2.length == n`
- `0 <= m <= 1000`
- `0 <= n <= 1000`
- `1 <= m + n <= 2000`
- `-10^6 <= nums1[i], nums2[i] <= 10^6`

<br><br>

## Approach 1: Merge Into a New Array (Brute Force)

First, let us be clear on what we are actually looking for. The **median** is simply the middle value of a sorted list.

- If the list has an **odd** count of numbers, the median is the single number sitting right in the middle. Example: `[1, 2, 3]` has a median of `2`.
- If the list has an **even** count of numbers, there is no single middle number, so we take the two middle numbers and average them. Example: `[1, 2, 3, 4]` has a median of `(2 + 3) / 2 = 2.5`.

Our numbers are just split across two arrays, but the goal stays exactly the same. The simplest idea is to actually build the full sorted array first.

- Both arrays are already sorted, so we can merge them like the merge step of merge sort.
- Keep two pointers, one on each array, and always copy the smaller current element into a brand new array.
- Once one array runs out, dump the rest of the other array into the new array.
- Now we have one fully sorted array of size `m + n`, so the median is easy to read:
  - **Odd** total length: pick the middle element.
  - **Even** total length: average the two middle elements.

The problem here is memory. We build a whole new array of size `m + n` just to read one or two values from the middle of it, so the extra space is `O(m + n)`. That feels wasteful, and it is the part we want to fix.

<br><br>

## Approach 2: Two Pointers Without Extra Space (This Solution)

The key insight is simple: we never actually needed the full merged array. We only care about the one or two elements sitting in the middle.

So we do the exact same merge walk, but instead of storing every element, we just count how many elements we have passed and grab the ones at the middle positions.

Here is the plan in plain words:

- First, figure out the two middle positions of the imaginary merged array:
  - `ind2 = (n + m) // 2` (the second middle index)
  - `ind1 = ind2 - 1` (the first middle index)
- Walk through both arrays with two pointers `i` and `j`, always moving the pointer that points to the smaller value. This is just the merge step, without saving anything.
- Keep a counter `cnt` for how many elements we have virtually placed so far.
  - When `cnt` reaches `ind1`, save that value as `first`.
  - When `cnt` reaches `ind2`, save that value as `second`.
- When one array is fully used up, keep walking through whatever is left in the other array, still watching the counter.
- Finally:
  - If the total length is **odd**, the answer is `second` (the exact middle element).
  - If the total length is **even**, the answer is the average of `first` and `second`.

<mark>This solution runs in O(n + m) time, not the O(log (m+n)) the problem asks for. It is still a big improvement over merging because it uses only O(1) extra space, and it is a clean stepping stone before learning the full binary search version.</mark>

<br><br>

## Code

```python
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        first, second = -1, -1
        n, m = len(nums1), len(nums2)

        ind1, ind2 = ((n + m) // 2) - 1, (n + m) // 2

        i, j = 0, 0
        cnt = 0

        while i < n and j < m:
            if nums1[i] < nums2[j]:
                if cnt == ind1:
                    first = nums1[i]
                if cnt == ind2:
                    second = nums1[i]
                cnt += 1
                i += 1
            else:
                if cnt == ind1:
                    first = nums2[j]
                if cnt == ind2:
                    second = nums2[j]
                cnt += 1
                j += 1

        while i < n:
            if cnt == ind1:
                first = nums1[i]
            if cnt == ind2:
                second = nums1[i]
            cnt += 1
            i += 1

        while j < m:
            if cnt == ind1:
                first = nums2[j]
            if cnt == ind2:
                second = nums2[j]
            cnt += 1
            j += 1

        if (n + m) % 2 == 1:
            return second

        return (first + second) / 2
```

<br><br>

## Dry Run

**Example 2:** `nums1 = [1,2]`, `nums2 = [3,4]` (even total length)

```ini
Setup:
  n = 2, m = 2
  ind2 = (2 + 2) // 2   = 2
  ind1 = ind2 - 1       = 1
  i = 0, j = 0, cnt = 0
  first = -1, second = -1

Main loop runs while i < 2 AND j < 2

Iteration 1:
  i = 0, j = 0
  compare nums1[0]=1  vs  nums2[0]=3   ->  1 < 3, take from nums1
  cnt(0) == ind1(1)?  No
  cnt(0) == ind2(2)?  No
  update: cnt -> 1, i -> 1

Iteration 2:
  i = 1, j = 0
  compare nums1[1]=2  vs  nums2[0]=3   ->  2 < 3, take from nums1
  cnt(1) == ind1(1)?  Yes  ->  first = nums1[1] = 2
  cnt(1) == ind2(2)?  No
  update: cnt -> 2, i -> 2

Main loop stops because i = 2 is not < 2

Leftover loop for nums1 -> skipped (i = 2 is not < 2)

Leftover loop for nums2 runs while j < 2

Iteration 3:
  j = 0
  value nums2[0] = 3
  cnt(2) == ind1(1)?  No
  cnt(2) == ind2(2)?  Yes  ->  second = nums2[0] = 3
  update: cnt -> 3, j -> 1

Iteration 4:
  j = 1
  value nums2[1] = 4
  cnt(3) == ind1(1)?  No
  cnt(3) == ind2(2)?  No
  update: cnt -> 4, j -> 2

Leftover loop stops because j = 2 is not < 2

Final:
  total length (n + m) = 4  ->  even
  answer = (first + second) / 2 = (2 + 3) / 2 = 2.5
```

**Example 1:** `nums1 = [1,3]`, `nums2 = [2]` (odd total length)

```ini
Setup:
  n = 2, m = 1
  ind2 = (2 + 1) // 2   = 1
  ind1 = ind2 - 1       = 0
  i = 0, j = 0, cnt = 0
  first = -1, second = -1

Main loop runs while i < 2 AND j < 1

Iteration 1:
  i = 0, j = 0
  compare nums1[0]=1  vs  nums2[0]=2   ->  1 < 2, take from nums1
  cnt(0) == ind1(0)?  Yes  ->  first = nums1[0] = 1
  cnt(0) == ind2(1)?  No
  update: cnt -> 1, i -> 1

Iteration 2:
  i = 1, j = 0
  compare nums1[1]=3  vs  nums2[0]=2   ->  3 < 2 is false, take from nums2 (else branch)
  cnt(1) == ind1(0)?  No
  cnt(1) == ind2(1)?  Yes  ->  second = nums2[0] = 2
  update: cnt -> 2, j -> 1

Main loop stops because j = 1 is not < 1

Leftover loop for nums1 runs while i < 2

Iteration 3:
  i = 1
  value nums1[1] = 3
  cnt(2) == ind1(0)?  No
  cnt(2) == ind2(1)?  No
  update: cnt -> 3, i -> 2

Leftover loop stops because i = 2 is not < 2

Leftover loop for nums2 -> skipped (j = 1 is not < 1)

Final:
  total length (n + m) = 3  ->  odd
  answer = second = 2
```

<br><br>

## Complexity Analysis

- **Time:** `O(n + m)` because in the worst case we walk across both arrays once.
- **Space:** `O(1)` because we only keep a few variables (`first`, `second`, `i`, `j`, `cnt`) and never build a new array.

<br><br>

## Related Problems

- [Merge Sorted Array (88)](https://leetcode.com/problems/merge-sorted-array/)
- [Merge k Sorted Lists (23)](https://leetcode.com/problems/merge-k-sorted-lists/)
- [Kth Largest Element in an Array (215)](https://leetcode.com/problems/kth-largest-element-in-an-array/)
- [Kth Smallest Element in a Sorted Matrix (378)](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/)
- [Find K-th Smallest Pair Distance (719)](https://leetcode.com/problems/find-k-th-smallest-pair-distance/)