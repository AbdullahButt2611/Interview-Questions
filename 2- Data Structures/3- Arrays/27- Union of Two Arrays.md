# Union of Two Sorted Arrays

`LinkedIn` • `Amazon` • `Microsoft` • `Google`

<br>

## Problem Statement

Given two sorted arrays `nums1` and `nums2`, return an array that contains the **union** of these two arrays. The elements in the union must be in **ascending order**.

The union of two arrays is an array where all values are **distinct** and are present in either the first array, the second array, or both.

### Examples

**Example 1**
```
Input:  nums1 = [1, 2, 3, 4, 5], nums2 = [1, 2, 7]
Output: [1, 2, 3, 4, 5, 7]

Explanation: 1 and 2 are common to both. 3, 4, 5 are only in nums1. 7 is only in nums2.
```

**Example 2**
```
Input:  nums1 = [3, 4, 6, 7, 9, 9], nums2 = [1, 5, 7, 8, 8]
Output: [1, 3, 4, 5, 6, 7, 8, 9]

Explanation: 7 is common to both. Duplicates within each array (9, 8) appear only once in the result.
```

### Constraints

- `1 <= nums1.length, nums2.length <= 10^5`
- `-10^9 <= nums1[i], nums2[i] <= 10^9`
- Both `nums1` and `nums2` are sorted in **non-decreasing** order.
- Arrays may contain **duplicate** elements.

<br><br>

## Approach 1: Brute Force using a Set

### Intuition

The simplest idea: dump everything into a `set`. A set automatically discards duplicates. Since Python's `set` is unordered, sort the result before returning.

### Steps

1. Insert all elements from both arrays into a `set`.
2. Convert the set to a sorted list and return it.

### Solution

```python
class Solution:
    def unionArray(self, nums1: list[int], nums2: list[int]) -> list[int]:
        return sorted(set(nums1) | set(nums2))
```

### Complexity Analysis

| | Complexity |
|---|---|
| **Time** | O((m + n) log(m + n)) (inserting into set is O(m + n), sorting is O((m + n) log(m + n))) |
| **Space** | O(m + n) (for the set storing all unique elements) |

<br>

### Problem with Approach 1

While clean and readable, this approach **ignores the fact that both arrays are already sorted**. We are paying an extra O((m + n) log(m + n)) cost for sorting a result that we could have built in sorted order directly. We can do better.

<br><br>

## Approach 2: Two Pointers (Optimal)

### Intuition

Since both arrays are already sorted, we can use two pointers (one for each array) and merge them similar to the merge step in Merge Sort. At each step, we pick the smaller of the two current elements. We skip duplicates by checking if the element we are about to add is the same as the last element added to the result.

This way, we build the union directly in sorted order without any extra sorting step.

### Steps

1. Initialize two pointers `i = 0` (for `nums1`) and `j = 0` (for `nums2`).
2. While both pointers are in bounds:
   - If `nums1[i] <= nums2[j]`, consider `nums1[i]`. Add it to result only if it differs from the last added element. Advance `i`.
   - Otherwise, consider `nums2[j]`. Add it only if it differs from the last added element. Advance `j`.
3. Drain any remaining elements from either array, skipping duplicates.
4. Return the result.

### Dry Run (Example 2)

```
nums1 = [3, 4, 6, 7, 9, 9]
nums2 = [1, 5, 7, 8, 8]

i=0, j=0  → nums1[0]=3 > nums2[0]=1 → add 1      → result=[1]
i=0, j=1  → nums1[0]=3 < nums2[1]=5 → add 3      → result=[1,3]
i=1, j=1  → nums1[1]=4 < nums2[1]=5 → add 4      → result=[1,3,4]
i=2, j=1  → nums1[2]=6 > nums2[1]=5 → add 5      → result=[1,3,4,5]
i=2, j=2  → nums1[2]=6 < nums2[2]=7 → add 6      → result=[1,3,4,5,6]
i=3, j=2  → nums1[3]=7 = nums2[2]=7 → add 7      → result=[1,3,4,5,6,7]
             (nums1[i] <= nums2[j] branch, advance i)
i=4, j=2  → nums1[4]=9 > nums2[2]=7 → already added → j++ → j=3
i=4, j=3  → nums1[4]=9 > nums2[3]=8 → add 8      → result=[1,3,4,5,6,7,8]
i=4, j=4  → nums1[4]=9 > nums2[4]=8 → already added → j++ → j=5
j exhausted → drain nums1: add 9     → result=[1,3,4,5,6,7,8,9]
              next nums1[5]=9 == last → skip

Final: [1, 3, 4, 5, 6, 7, 8, 9] ✓
```

### Solution

```python
class Solution:
    def unionArray(self, nums1: list[int], nums2: list[int]) -> list[int]:
        i, j = 0, 0
        result = []

        while i < len(nums1) and j < len(nums2):
            if nums1[i] <= nums2[j]:
                if not result or result[-1] != nums1[i]:
                    result.append(nums1[i])
                i += 1
            else:
                if not result or result[-1] != nums2[j]:
                    result.append(nums2[j])
                j += 1

        # Drain remaining elements from nums1
        while i < len(nums1):
            if not result or result[-1] != nums1[i]:
                result.append(nums1[i])
            i += 1

        # Drain remaining elements from nums2
        while j < len(nums2):
            if not result or result[-1] != nums2[j]:
                result.append(nums2[j])
            j += 1

        return result
```

### Complexity Analysis

| | Complexity |
|---|---|
| **Time** | O(m + n) (each element from both arrays is visited exactly once) |
| **Space** | O(m + n) (for the result array, no auxiliary data structures) |

> **Note:** The result array is necessary to store the output. If output space is not counted, space complexity is O(1).

<br><br>

## Comparison of Approaches

| Approach | Time Complexity | Space Complexity | Uses Sorted Property |
|---|---|---|---|
| Brute Force (Set) | O((m + n) log(m + n)) | O(m + n) | No |
| Two Pointers | **O(m + n)** | O(m + n) | **Yes** |

<br><br>

## Edge Cases

```python
# One empty array
nums1 = [], nums2 = [1, 2, 3]
# Output: [1, 2, 3]

# Both arrays identical
nums1 = [1, 1, 2], nums2 = [1, 1, 2]
# Output: [1, 2]

# No common elements
nums1 = [1, 3, 5], nums2 = [2, 4, 6]
# Output: [1, 2, 3, 4, 5, 6]

# All duplicates within a single array
nums1 = [5, 5, 5], nums2 = [5, 5]
# Output: [5]
```

<br><br>

## Key Takeaways

- When both input arrays are **sorted**, always look for a two-pointer approach before reaching for a set or sort-based solution.
- The duplicate-skipping check `result[-1] != current` works correctly here because the arrays are sorted, so all duplicates of a value appear consecutively.
- This problem is essentially a merge step from **Merge Sort**, with an added deduplication condition.