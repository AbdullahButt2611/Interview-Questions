# Reverse Pairs

`Google` • `Amazon` • `Microsoft` • `Adobe`

## Problem Statement

Given an integer array `nums`, return the number of reverse pairs in the array.

A reverse pair is a pair `(i, j)` where:

* `0 <= i < j < nums.length`, and
* `nums[i] > 2 * nums[j]`.

### Example 1

```
Input: nums = [1, 3, 2, 3, 1]
Output: 2

Explanation:
The reverse pairs are:
(1, 4)  ->  nums[1] = 3, nums[4] = 1, 3 > 2 * 1
(3, 4)  ->  nums[3] = 3, nums[4] = 1, 3 > 2 * 1
```

### Example 2

```
Input: nums = [2, 4, 3, 5, 1]
Output: 3

Explanation:
The reverse pairs are:
(1, 4)  ->  nums[1] = 4, nums[4] = 1, 4 > 2 * 1
(2, 4)  ->  nums[2] = 3, nums[4] = 1, 3 > 2 * 1
(3, 4)  ->  nums[3] = 5, nums[4] = 1, 5 > 2 * 1
```

### Constraints

* `1 <= nums.length <= 5 * 10^4`
* `-2^31 <= nums[i] <= 2^31 - 1`

<br><br>

## Approach 1: Brute Force

**Idea**

* Check every pair of indices `(i, j)` where `i < j`.
* If `nums[i] > 2 * nums[j]`, it is a reverse pair, so increment a counter.
* This is a direct, literal translation of the definition into code.

### Solution

```python
def reverse_pairs_brute_force(nums):
    n = len(nums)
    count = 0

    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] > 2 * nums[j]:
                count += 1

    return count
```

### Dry Run

Input: `nums = [1, 3, 2, 3, 1]`

```
nums = [1, 3, 2, 3, 1]
index =  0  1  2  3  4

i = 0, nums[i] = 1
    j = 1, nums[j] = 3    1 > 2 * 3 = 6 ?   No
    j = 2, nums[j] = 2    1 > 2 * 2 = 4 ?   No
    j = 3, nums[j] = 3    1 > 2 * 3 = 6 ?   No
    j = 4, nums[j] = 1    1 > 2 * 1 = 2 ?   No

i = 1, nums[i] = 3
    j = 2, nums[j] = 2    3 > 2 * 2 = 4 ?   No
    j = 3, nums[j] = 3    3 > 2 * 3 = 6 ?   No
    j = 4, nums[j] = 1    3 > 2 * 1 = 2 ?   Yes   count = 1

i = 2, nums[i] = 2
    j = 3, nums[j] = 3    2 > 2 * 3 = 6 ?   No
    j = 4, nums[j] = 1    2 > 2 * 1 = 2 ?   No

i = 3, nums[i] = 3
    j = 4, nums[j] = 1    3 > 2 * 1 = 2 ?   Yes   count = 2

i = 4, nums[i] = 1
    (no j greater than 4)

Final count = 2
```

### Complexity

* Time: `O(n^2)`, every pair of indices is visited once.
* Space: `O(1)`, only a counter is used.

<br><br>

### What is the problem with this solution?

* The nested loop always checks all `n * (n - 1) / 2` pairs, regardless of how the data is arranged.
* For `n = 5 * 10^4`, that is close to `2.5 * 10^9` comparisons, which will time out.
* It never uses the fact that once the halves of the array are sorted, many reverse pairs can be counted in bulk instead of one comparison at a time.

### What can we do better?

* We need a way to count "how many earlier elements are more than twice this one" without comparing every pair individually.
* Merge sort already arranges elements in sorted order while combining halves, and once both halves are sorted the crossing pairs can be counted with a single linear pass.

<br><br>

## Approach 2: Divide and Conquer (Modified Merge Sort)

**Idea**

* Sort the array with merge sort, but before each merge, count the reverse pairs that cross the boundary between the two halves.
* A crossing pair uses a left index `i` (in `low .. mid`) and a right index `j` (in `mid + 1 .. high`). This automatically satisfies `i < j` because the whole left half sits before the whole right half in the original order.
* One detail sets this apart from a plain inversion count. The comparison that defines a reverse pair (`nums[i] > 2 * nums[j]`) is not the same as the comparison that decides the merge order (`nums[i] <= nums[j]`). Because of that mismatch, the crossing pairs cannot be counted for free during the merge itself. They get their own dedicated pass, `countPair`, which runs before `merge`.
* By the time `countPair` runs, both halves are already sorted from the recursive calls, so the pass is cheap. For each left element, advance a `right` pointer while `nums[i] > 2 * nums[right]`. Since the left half is sorted ascending, a larger left value can only qualify more right elements, so `right` never has to move backward across the whole left loop. That keeps the counting linear.
* After counting, the standard `merge` runs so the combined section stays sorted in place for the parent call.

### Solution

```python
from typing import List

class Solution:
    def countPair(self, nums, low, mid, high):
        # Both halves (low..mid and mid+1..high) are already sorted.
        # Count pairs where nums[i] > 2 * nums[j], i in left, j in right.
        right = mid + 1
        count = 0

        for i in range(low, mid + 1):
            while right <= high and nums[i] > 2 * nums[right]:
                right += 1
            count += right - (mid + 1)

        return count

    def merge(self, nums, low, mid, high):
        temp = []
        left = low
        right = mid + 1

        while left <= mid and right <= high:
            if nums[left] <= nums[right]:
                temp.append(nums[left])
                left += 1
            else:
                temp.append(nums[right])
                right += 1

        while left <= mid:
            temp.append(nums[left])
            left += 1

        while right <= high:
            temp.append(nums[right])
            right += 1

        for i in range(low, high + 1):
            nums[i] = temp[i - low]

    def mergeSort(self, nums, low, high):
        if low >= high:
            return 0

        mid = (low + high) // 2

        count = self.mergeSort(nums, low, mid)
        count += self.mergeSort(nums, mid + 1, high)
        count += self.countPair(nums, low, mid, high)
        self.merge(nums, low, mid, high)

        return count

    def reversePairs(self, nums: List[int]) -> int:
        return self.mergeSort(nums, 0, len(nums) - 1)
```

### Dry Run

Input: `nums = [1, 3, 2, 3, 1]`

The recursion sorts the array in place and counts crossing pairs at each combine step. The trace below shows the array state as it resolves from the bottom up.

```
mergeSort(0, 4)   mid = 2
    split into left half [0..2] and right half [3..4]

Solve left half [0..2] = [1, 3, 2]

    mergeSort(0, 1)   mid = 0
        left [0..0] = [1], right [1..1] = [3]
        countPair(low=0, mid=0, high=1):
            right = 1
            i = 0, nums[0] = 1   1 > 2 * 3 = 6 ?  No
                   count += right - (mid+1) = 1 - 1 = 0
            returns 0
        merge -> nums[0..1] stays [1, 3]
        state: [1, 3, 2, 3, 1]

    mergeSort(2, 2) -> 0

    countPair(low=0, mid=1, high=2):   left [1, 3], right [2]
        right = 2
        i = 0, nums[0] = 1   1 > 2 * 2 = 4 ?  No    count += 2 - 2 = 0
        i = 1, nums[1] = 3   3 > 2 * 2 = 4 ?  No    count += 2 - 2 = 0
        returns 0
    merge -> nums[0..2] becomes [1, 2, 3]
    state: [1, 2, 3, 3, 1]

    left half total = 0


Solve right half [3..4] = [3, 1]

    mergeSort(3, 3) -> 0
    mergeSort(4, 4) -> 0
    countPair(low=3, mid=3, high=4):   left [3], right [1]
        right = 4
        i = 3, nums[3] = 3   3 > 2 * 1 = 2 ?  Yes   right = 5
               count += right - (mid+1) = 5 - 4 = 1
        returns 1
    merge -> nums[3..4] becomes [1, 3]
    state: [1, 2, 3, 1, 3]

    right half total = 1


Combine at the top   countPair(low=0, mid=2, high=4)
left half [1, 2, 3]   right half [1, 3]
    right = 3
    i = 0, nums[0] = 1
        right = 3, nums[3] = 1   1 > 2 * 1 = 2 ?  No
        count += right - (mid+1) = 3 - 3 = 0
    i = 1, nums[1] = 2
        right = 3, nums[3] = 1   2 > 2 * 1 = 2 ?  No
        count += 3 - 3 = 0
    i = 2, nums[2] = 3
        right = 3, nums[3] = 1   3 > 2 * 1 = 2 ?  Yes   right = 4
        right = 4, nums[4] = 3   3 > 2 * 3 = 6 ?  No
        count += right - (mid+1) = 4 - 3 = 1
    returns 1
merge -> nums becomes [1, 1, 2, 3, 3]

Total reverse pairs = 0 (left) + 1 (right) + 1 (cross) = 2
```

Final answer matches the expected output: `2`

### Complexity

* Time: `O(n log n)`, the array is split `log n` times, and each level does `O(n)` work for the counting pass and the merge combined.
* Space: `O(n)`, for the temporary list used while merging, plus the recursion stack of depth `O(log n)`.

<br><br>

### What is the problem with this solution?

* It reorders the array as a side effect of sorting, so the original ordering of `nums` is lost by the time the function returns.
* The counting logic sits right next to the merge step, which is fine for a single total but takes some care to adapt if a follow up asks for a per index breakdown instead of one number.

### What can we do better?

* For a single offline total, this divide and conquer solution is already optimal and is usually the expected answer in an interview.
* If the original order must be preserved, sort a copy of the array instead of `nums`, or run the merge on an array of indices and read the values back through the original array at the end.

<br><br>

## Related Concepts

* Merge Sort
* Divide and Conquer

<br><br>

## Related Problems

* Count Inversions
* Count of Smaller Numbers After Self (LeetCode 315)
* Global and Local Inversions (LeetCode 775)
* Sort an Array (LeetCode 912)