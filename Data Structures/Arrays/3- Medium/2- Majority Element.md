# 169. Majority Element

`Amazon` • `Google` • `Apple` • `Meta` • `Microsoft` • `Adobe` • `Uber` • `LinkedIn`
<br>

## Problem Statement

Given an array `nums` of size `n`, return the majority element.

The majority element is the element that appears more than `⌊n / 2⌋` times. You may assume that the majority element always exists in the array.

**Examples**

```
Input: nums = [3,2,3]
Output: 3
```

```
Input: nums = [2,2,1,1,1,2,2]
Output: 2
```

**Constraints**

- `n == nums.length`
- `1 <= n <= 5 * 10^4`
- `-10^9 <= nums[i] <= 10^9`
- The majority element always exists in the array.

<br><br>

## Approach 1: Brute Force

**Approach:** For every element in the array, count how many times it appears by iterating through the entire array. If its count exceeds `n / 2`, return it.

**Problem:** This results in a nested loop, giving O(n^2) time complexity. For large inputs (up to 5 * 10^4), this is far too slow and will time out.

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        n = len(nums)
        n_by_2 = n // 2

        for i in range(n):
            count = 0
            for j in range(n):
                if nums[j] == nums[i]:
                    count += 1
            if count > n_by_2:
                return nums[i]
```

**Complexity**
- Time: O(n^2)
- Space: O(1)

**What can we do better?** Instead of recounting every element from scratch, we can use a hash map to store the frequency of each element in a single pass and look it up in O(1).

<br><br>

## Approach 2: HashMap (Better)

**Approach:** Traverse the array once and store the frequency of each element in a dictionary. After building the frequency map, iterate over it to find the element whose count exceeds `n / 2`.

**Problem:** This is a significant improvement in time, but we now use O(n) extra space to store the frequency map. We need to find a way to solve this in constant space.

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        frequency = {}
        n_by_2 = len(nums) // 2

        for num in nums:
            if num in frequency:
                frequency[num] += 1
            else:
                frequency[num] = 1

        for num, freq in frequency.items():
            if freq > n_by_2:
                return num
```

**Complexity**
- Time: O(n)
- Space: O(n)

**What can we do better?** We can eliminate the hash map entirely and solve this in O(1) space using the Boyer-Moore Voting Algorithm, which exploits the guaranteed majority property.

<br><br>

## Approach 3: Boyer-Moore Voting Algorithm (Optimal)

**Approach:** Maintain a `candidate` element and a `count`. Traverse the array once. When `count` reaches 0, set the current element as the new candidate. If the current element matches the candidate, increment count; otherwise decrement it. Since the majority element appears more than `n / 2` times, it is guaranteed to survive this cancellation process and remain as the final candidate.

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        element = nums[0]
        count = 0

        for num in nums:
            if count == 0:
                element = num
                count = 1
            elif element == num:
                count += 1
            else:
                count -= 1

        return element
```

**Complexity**
- Time: O(n)
- Space: O(1)

**Why can we directly return `element` here?**

The problem explicitly guarantees that a majority element always exists. Because of this guarantee, after one pass, the surviving candidate is always the majority element. We do not need to verify it with a second pass.

<br><br>

## Note: When the Majority is NOT Guaranteed

If the problem does NOT guarantee the existence of a majority element, the Boyer-Moore algorithm alone is not sufficient. The candidate that survives the first pass might just be the most frequent element without actually exceeding the `n / 2` threshold. In that case, a second verification pass is required.

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        element = nums[0]
        count = 0

        # Phase 1: Find the candidate
        for num in nums:
            if count == 0:
                element = num
                count = 1
            elif element == num:
                count += 1
            else:
                count -= 1

        # Phase 2: Verify the candidate
        count = 0
        n_by_2 = len(nums) // 2

        for num in nums:
            if num == element:
                count += 1

        if count > n_by_2:
            return element
        else:
            return -1  # No majority element exists
```

**Complexity**
- Time: O(n)
- Space: O(1)

<br><br>

## About Boyer-Moore Voting Algorithm

The Boyer-Moore Voting Algorithm was originally designed to find a majority element in a single pass using constant space. The core idea is based on pairwise cancellation.

Think of each element as a vote for itself. Whenever two different elements meet, they cancel each other out. Since the majority element appears more than half the time, it can never be fully cancelled by all the other elements combined, no matter how they are arranged. After all cancellations, the majority element is the one left standing as the candidate.

The algorithm tracks just two variables: a `candidate` and a `count`. When count drops to zero, the current element takes over as the new candidate. This elegantly simulates the cancellation without needing any extra data structure.

It is particularly powerful in streaming scenarios where you cannot store all elements in memory and need to identify the majority in a single sweep.