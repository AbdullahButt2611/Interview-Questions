# 136. Single Number

`Amazon` • `Google` • `Microsoft` • `Facebook` • `Bloomberg` • `Adobe`
<br>

## Problem Statement

Given a non-empty array of integers `nums`, every element appears twice except for one. Find that single one.

You must implement a solution with a **linear runtime complexity** and use only **constant extra space**.

**Example 1:**
```
Input:  nums = [2,2,1]
Output: 1
```

**Example 2:**
```
Input:  nums = [4,1,2,1,2]
Output: 4
```

**Example 3:**
```
Input:  nums = [1]
Output: 1
```

**Constraints:**
- `1 <= nums.length <= 3 * 10^4`
- `-3 * 10^4 <= nums[i] <= 3 * 10^4`
- Each element in the array appears twice except for one element which appears only once.

<br><br>

## Approach 1: Brute Force (Nested Loop)

**Intuition:**
For each element, scan the rest of the array to check if it appears again. If no second occurrence is found, that element is the answer.

**Steps:**
1. For each index `i`, iterate through every other index `j`.
2. Count how many times `nums[i]` appears in the array.
3. If the count is `1`, return `nums[i]`.

```python
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        for i in range(len(nums)):
            count = 0
            for j in range(len(nums)):
                if nums[j] == nums[i]:
                    count += 1
            if count == 1:
                return nums[i]
```

**Complexity Analysis:**
| | |
|---|---|
| **Time** | O(n²) - for each element we scan the entire array |
| **Space** | O(1) - no extra data structures used |

**Problem with this approach:**
Even though space is constant, the time complexity is O(n²) which is too slow for the given constraint of `n = 3 * 10^4`. We are repeatedly scanning the array from scratch for every single element. We need a way to track what we have seen in a single pass.

<br><br>

## Approach 2: HashMap / Frequency Count

**Intuition:**
Instead of re-scanning for every element, we can make a single pass and store the frequency of each number in a hash map. A second pass through the map then finds the one number with a frequency of `1`.

**Steps:**
1. Initialize an empty dictionary `freq`.
2. Iterate through `nums` and count occurrences of each number.
3. Iterate through the dictionary and return the key whose value is `1`.

```python
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        freq = {}

        for num in nums:
            freq[num] = freq.get(num, 0) + 1

        for num, count in freq.items():
            if count == 1:
                return num
```

**Complexity Analysis:**
| | |
|---|---|
| **Time** | O(n) - two linear passes through the data |
| **Space** | O(n) - the dictionary stores up to n/2 + 1 unique keys |

**Problem with this approach:**
This satisfies the time constraint but violates the space constraint. The problem explicitly requires O(1) extra space. In the worst case, the dictionary holds nearly half the elements of the array. We need a smarter approach that does not store any element at all.

<br><br>

## Approach 3: XOR Bit Manipulation (Optimal)

**Intuition:**
XOR has two key properties that make it perfect for this problem:

- `a ^ a = 0` (any number XORed with itself is 0)
- `a ^ 0 = a` (any number XORed with 0 is itself)
- XOR is commutative and associative, so order does not matter.

If we XOR all numbers together, every pair cancels out to `0`, and only the single unpaired number remains.

```
[4, 1, 2, 1, 2]
0 ^ 4 = 4
4 ^ 1 = 5
5 ^ 2 = 7
7 ^ 1 = 6
6 ^ 2 = 4   <- the single number
```

**Steps:**
1. Initialize `result = 0`.
2. XOR every number in `nums` into `result`.
3. Return `result`.

```python
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        result = 0

        for num in nums:
            result = result ^ num

        return result
```

**Dry Run:**

```
nums = [4, 1, 2, 1, 2]

result = 0
result ^ 4 = 4
result ^ 1 = 5    (4  ^ 1)
result ^ 2 = 7    (5  ^ 2)
result ^ 1 = 6    (7  ^ 1) -- the pair of 1 cancels out
result ^ 2 = 4    (6  ^ 2) -- the pair of 2 cancels out

Output: 4 ✓
```

**Complexity Analysis:**
| | |
|---|---|
| **Time** | O(n) - single pass through the array |
| **Space** | O(1) - only one integer variable used |

**Why this is optimal:**
This is the only approach that satisfies both constraints simultaneously: O(n) time and O(1) space. Every element is visited exactly once and no extra memory is allocated. XOR is also extremely fast at the hardware level, making this the most efficient solution possible.

<br><br>

## Summary

| Approach | Time | Space | Meets Constraints |
|---|---|---|---|
| Brute Force (Nested Loop) | O(n²) | O(1) | No - time too slow |
| HashMap / Frequency Count | O(n) | O(n) | No - uses extra space |
| XOR Bit Manipulation | O(n) | O(1) | Yes - optimal |

**Recommended solution for interviews:** Approach 3 - XOR Bit Manipulation.

**Key insight to remember:** XOR cancels duplicate pairs. Any number that appears an even number of times vanishes, leaving only the element that appears an odd number of times.