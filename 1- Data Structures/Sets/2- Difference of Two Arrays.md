# Find the Difference of Two Arrays
`LeetCode 75`

## Problem Statement

You are given two **0-indexed** integer arrays `nums1` and `nums2`.

Return a list `answer` of size **2** where:

* `answer[0]` contains all **distinct** integers in `nums1` that are **not** in `nums2`.
* `answer[1]` contains all **distinct** integers in `nums2` that are **not** in `nums1`.

The order of numbers inside each list does not matter.

<br><br>

## Approach 1: Using Sets (Simple and Clear)

This method uses built-in sets. Since sets remove repeated items and allow fast lookup, they help solve the task in a clean way.

### Code

```python
class Solution:
    def findDifference(self, nums1: List[int], nums2: List[int]) -> List[List[int]]:
        set1, set2 = set(nums1), set(nums2)
        return [list(set1 - set2), list(set2 - set1)]
```

### Explanation

* Convert both arrays to sets.
* Use set subtraction to find items that appear in one but not the other.
* Return the two lists.

### What can be better?

This method is already short and fast. But we can also write it in a more manual way if we want full control.

<br><br>

## Approach 2: Manual Check with Loops

This method uses loops to check items one by one. It matches the logic of the code you shared.

### Code

```python
class Solution:
    def findDifference(self, nums1: List[int], nums2: List[int]) -> List[List[int]]:
        set1, set2 = set(nums1), set(nums2)
        result = [[], []]

        for num in set1:
            if num not in set2:
                result[0].append(num)

        for num in set2:
            if num not in set1:
                result[1].append(num)

        return result
```

### Explanation

* Turn both lists into sets.
* Loop through both sets.
* Add numbers that do not appear in the other set.

### What is the difference from the first method?

* It does the same thing but with more steps.
* It is still fast but not as short as the first one.

<br><br>

## Final Notes

For this task, **Approach 1** is the best in both speed and form. The manual loop method is fine too if you need more control.

You can add any of the above versions to your repository.
