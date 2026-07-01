# Count Inversions

`Amazon` • `Microsoft` • `Adobe` • `Flipkart`

## Problem Statement

Given an integer array `nums`, return the number of inversions in the array.

Two elements `nums[i]` and `nums[j]` form an inversion if `nums[i] > nums[j]` and `i < j`.

The inversion count indicates how close an array is to being sorted. A sorted array has an inversion count of `0`. An array sorted in descending order has the maximum possible inversion count.

### Example 1

```
Input: nums = [2, 3, 7, 1, 3, 5]
Output: 5

Explanation:
The responsible pairs are:
nums[0], nums[3]  ->  2 > 1  and  0 < 3
nums[1], nums[3]  ->  3 > 1  and  1 < 3
nums[2], nums[3]  ->  7 > 1  and  2 < 3
nums[2], nums[4]  ->  7 > 3  and  2 < 4
nums[2], nums[5]  ->  7 > 5  and  2 < 5
```

### Example 2

```
Input: nums = [-10, -5, 6, 11, 15, 17]
Output: 0

Explanation:
nums is already sorted, hence no inversions are present.
```

### Constraints

* `1 <= nums.length <= 10^5`
* `-10^9 <= nums[i] <= 10^9`

<br><br>

## Approach 1: Brute Force

**Idea**

* Check every pair of indices `(i, j)` where `i < j`.
* If `nums[i] > nums[j]`, it is an inversion, so increment a counter.
* This is a direct, literal translation of the definition into code.

### Solution

```python
def count_inversions_brute_force(nums):
    n = len(nums)
    count = 0

    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] > nums[j]:
                count += 1

    return count
```

### Dry Run

Input: `nums = [2, 3, 7, 1, 3, 5]`

```
nums = [2, 3, 7, 1, 3, 5]
index =  0  1  2  3  4  5

i = 0, nums[i] = 2
    j = 1, nums[j] = 3    2 > 3 ?  No
    j = 2, nums[j] = 7    2 > 7 ?  No
    j = 3, nums[j] = 1    2 > 1 ?  Yes   count = 1
    j = 4, nums[j] = 3    2 > 3 ?  No
    j = 5, nums[j] = 5    2 > 5 ?  No

i = 1, nums[i] = 3
    j = 2, nums[j] = 7    3 > 7 ?  No
    j = 3, nums[j] = 1    3 > 1 ?  Yes   count = 2
    j = 4, nums[j] = 3    3 > 3 ?  No
    j = 5, nums[j] = 5    3 > 5 ?  No

i = 2, nums[i] = 7
    j = 3, nums[j] = 1    7 > 1 ?  Yes   count = 3
    j = 4, nums[j] = 3    7 > 3 ?  Yes   count = 4
    j = 5, nums[j] = 5    7 > 5 ?  Yes   count = 5

i = 3, nums[i] = 1
    j = 4, nums[j] = 3    1 > 3 ?  No
    j = 5, nums[j] = 5    1 > 5 ?  No

i = 4, nums[i] = 3
    j = 5, nums[j] = 5    3 > 5 ?  No

Final count = 5
```

### Complexity

* Time: `O(n^2)`, every pair of indices is visited once.
* Space: `O(1)`, only a counter is used.

<br><br>

### What is the problem with this solution?

* The nested loop always checks all `n * (n - 1) / 2` pairs, no matter how the data is arranged.
* For `n = 10^5`, that is close to `5 * 10^9` comparisons, which will time out.
* It never uses the fact that once we know one element is out of place, several inversions can often be inferred together instead of being checked one by one.

### What can we do better?

* We need a way to count "how many smaller elements come after the current one" without comparing every pair individually.
* Merge sort already groups elements in sorted order while combining halves, so we can piggyback the counting on top of that process.

<br><br>

## Approach 2: Divide and Conquer (Modified Merge Sort)

**Idea**

* Split the array into a left half and a right half.
* Recursively count inversions inside the left half, then inside the right half.
* The only inversions left to count are the ones that cross between the two halves, meaning a left element that is greater than a right element.
* If both halves are already sorted, crossing inversions can be counted for free while merging them.
* During the merge step, walking two pointers left to right, whenever an element from the right half is placed before the left half is exhausted, that right element is smaller than every remaining element in the left half. All of those remaining left elements form an inversion with it, and they can all be added at once.

### Solution

```python
def count_inversions(nums):
    def merge_sort_and_count(arr):
        if len(arr) <= 1:
            return arr, 0

        mid = len(arr) // 2
        left, left_count = merge_sort_and_count(arr[:mid])
        right, right_count = merge_sort_and_count(arr[mid:])

        merged = []
        i = j = 0
        cross_count = 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
                cross_count += len(left) - i

        merged.extend(left[i:])
        merged.extend(right[j:])

        return merged, left_count + right_count + cross_count

    _, total = merge_sort_and_count(nums)
    return total
```

### Dry Run

Input: `nums = [2, 3, 7, 1, 3, 5]`

```
Split:  [2, 3, 7, 1, 3, 5]
             |
       -------------
       |           |
   [2, 3, 7]    [1, 3, 5]


Solve left half [2, 3, 7]

    Split:  [2, 3, 7]
                 |
           -------------
           |           |
         [2]        [3, 7]

    Solve [3, 7]
        Split into [3] and [7], both size 1, 0 inversions each
        Merge [3] and [7]:
            left = [3]   right = [7]
            i=0 j=0   3 <= 7 ?  Yes   take 3 from left   i=1
            left exhausted, append remaining right -> [7]
            merged = [3, 7]   cross_count = 0

    Merge [2] and [3, 7]:
        left = [2]   right = [3, 7]
        i=0 j=0   2 <= 3 ?  Yes   take 2 from left   i=1
        left exhausted, append remaining right -> [3, 7]
        merged = [2, 3, 7]   cross_count = 0

    left_count = 0, right_count = 0, cross_count = 0
    Left half result: [2, 3, 7]   total inversions = 0


Solve right half [1, 3, 5]

    Split:  [1, 3, 5]
                 |
           -------------
           |           |
         [1]        [3, 5]

    Solve [3, 5]
        Split into [3] and [5], both size 1, 0 inversions each
        Merge [3] and [5]:
            left = [3]   right = [5]
            i=0 j=0   3 <= 5 ?  Yes   take 3 from left   i=1
            left exhausted, append remaining right -> [5]
            merged = [3, 5]   cross_count = 0

    Merge [1] and [3, 5]:
        left = [1]   right = [3, 5]
        i=0 j=0   1 <= 3 ?  Yes   take 1 from left   i=1
        left exhausted, append remaining right -> [3, 5]
        merged = [1, 3, 5]   cross_count = 0

    left_count = 0, right_count = 0, cross_count = 0
    Right half result: [1, 3, 5]   total inversions = 0


Merge left half [2, 3, 7] and right half [1, 3, 5]
left_count = 0   right_count = 0

    left  = [2, 3, 7]   size = 3
    right = [1, 3, 5]

    i=0 j=0   left[i]=2   right[j]=1   2 <= 1 ?  No
              take 1 from right   j=1
              cross_count += len(left) - i = 3 - 0 = 3   cross_count = 3

    i=0 j=1   left[i]=2   right[j]=3   2 <= 3 ?  Yes
              take 2 from left   i=1

    i=1 j=1   left[i]=3   right[j]=3   3 <= 3 ?  Yes
              take 3 from left   i=2

    i=2 j=1   left[i]=7   right[j]=3   7 <= 3 ?  No
              take 3 from right   j=2
              cross_count += len(left) - i = 3 - 2 = 1   cross_count = 4

    i=2 j=2   left[i]=7   right[j]=5   7 <= 5 ?  No
              take 5 from right   j=3
              cross_count += len(left) - i = 3 - 2 = 1   cross_count = 5

    right exhausted, append remaining left -> [7]

    merged = [1, 2, 3, 3, 5, 7]
    cross_count = 5

Total inversions = left_count + right_count + cross_count
                  = 0 + 0 + 5
                  = 5
```

Final answer matches the expected output: `5`

### Complexity

* Time: `O(n log n)`, the array is split `log n` times, and each level does `O(n)` work while merging.
* Space: `O(n)`, for the temporary lists created during merging.
<br><br>
### What is the problem with this solution?

* It permanently reorders the array as a side effect of sorting, which is a problem if the original order of `nums` needs to be preserved afterward.
* The counting logic is tightly mixed into the merge step, which makes it a little harder to adapt if a follow up question asks for something like the inversion count contributed by each individual index rather than a single total.

### What can we do better?

* If the original array order must be preserved, the merge step can be done on index copies instead of the values themselves, then the values can be restored from the original array at the end.
* For most interview settings, this divide and conquer solution is already the expected, optimal answer.

<br><br>

## Related Concepts

* Merge Sort

<br><br>

## Related Problems

* Reverse Pairs (LeetCode 493)
* Count of Smaller Numbers After Self (LeetCode 315)
* Global and Local Inversions (LeetCode 775)
* Count the Number of Inversions (LeetCode 3193)
* Sort an Array (LeetCode 912)