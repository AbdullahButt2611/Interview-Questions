# 485. Max Consecutive Ones

`Microsoft` • `Meta` • `Amazon` • `Accenture` • `Yandex`
<br>

## Problem Statement

Given a binary array `nums`, return the maximum number of consecutive `1`'s in the array.

**Example 1:**
```
Input:  nums = [1,1,0,1,1,1]
Output: 3
Explanation: The first two digits or the last three digits are consecutive 1s.
             The maximum number of consecutive 1s is 3.
```

**Example 2:**
```
Input:  nums = [1,0,1,1,0,1]
Output: 2
```

**Constraints:**
- `1 <= nums.length <= 10^5`
- `nums[i]` is either `0` or `1`

<br><br>

## Approach 1: Brute Force (Nested Loop)

**Intuition:**
The most straightforward idea is to check every possible subarray of the input. For each starting index, extend the window as long as we keep seeing `1`s, track the length of that run, and update a global maximum.

**Steps:**
1. Iterate over every index `i` as a potential start of a consecutive run.
2. For each `i`, walk forward with a second pointer `j` while `nums[j] == 1`.
3. The length of the run is `j - i`. Compare it with the current maximum.
4. Return the maximum after all pairs are checked.

```python
class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        max_ones = 0

        for i in range(len(nums)):
            count = 0
            for j in range(i, len(nums)):
                if nums[j] == 1:
                    count += 1
                    max_ones = max(max_ones, count)
                else:
                    break

        return max_ones
```

**Complexity Analysis:**
| | |
|---|---|
| **Time** | O(n²) - for each element we potentially scan the rest of the array |
| **Space** | O(1) - only two integer variables used |

**Problem with this approach:**
We are doing redundant work. Once we hit a `0` from some starting index `i`, we break out and start again from `i+1`, re-examining elements we have already visited. For an array of size `10^5`, this can perform up to `~5 x 10^9` operations in the worst case (an all-ones array), which will TLE. We need to scan the array only once.

<br><br>

## Approach 2: Linear Scan with Running Counter (Optimal)

**Intuition:**
We do not need to re-examine any element. A single left-to-right pass is enough. We maintain a `count` of the current consecutive run of `1`s. Every time we see a `1`, we increment it. Every time we see a `0`, the run is broken so we reset `count` to `0` and update `max_ones`.

There is one subtle edge case: if the array ends with a run of `1`s, we never hit a `0` to trigger the final comparison, so we must do one last `max` update after the loop exits.

**Steps:**
1. Initialize `max_ones = 0` and `count = 0`.
2. For each number in `nums`:
   - If `num == 1`, increment `count`.
   - Otherwise, update `max_ones = max(max_ones, count)` and reset `count = 0`.
3. After the loop, do a final `max_ones = max(max_ones, count)` to handle a trailing run of `1`s.
4. Return `max_ones`.

```python
class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        max_ones = 0
        count = 0

        for num in nums:
            if num == 1:
                count += 1
            else:
                max_ones = max(max_ones, count)
                count = 0

        max_ones = max(max_ones, count)  # handles trailing run of 1s
        return max_ones
```

**Dry Run:**

```
nums = [1, 1, 0, 1, 1, 1]

num=1  -> count=1, max_ones=0
num=1  -> count=2, max_ones=0
num=0  -> max_ones=max(0,2)=2, count=0
num=1  -> count=1, max_ones=2
num=1  -> count=2, max_ones=2
num=1  -> count=3, max_ones=2

After loop: max_ones=max(2,3)=3 ✓
```

**Complexity Analysis:**
| | |
|---|---|
| **Time** | O(n) - single pass through the array |
| **Space** | O(1) - only two integer variables used |

**Why this is optimal:**
Every element must be examined at least once to determine the answer (we cannot skip any element without risking missing the longest run). Therefore, O(n) time is a lower bound and this solution matches it. Space is O(1) since no auxiliary data structures are used.

<br><br>

## Approach 3: Pythonic One-liner (Using `split`)

**Intuition:**
If we convert the binary array to a string (e.g., `"11011100"`), consecutive `1`s become substrings of `1`s separated by `0`s. Splitting on `"0"` gives us all those substrings and the answer is simply the length of the longest one.

```python
class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        return max(len(s) for s in "".join(map(str, nums)).split("0"))
```

**Complexity Analysis:**
| | |
|---|---|
| **Time** | O(n) - string construction and split are both linear |
| **Space** | O(n) - a string of length n is created |

**Note:** This is a clean Python trick but uses O(n) extra space for the string. In an interview, Approach 2 is preferred for being space-optimal and language-agnostic. This is best used as a follow-up to show Python fluency.

<br><br>

## Summary

| Approach | Time | Space | Notes |
|---|---|---|---|
| Brute Force (Nested Loop) | O(n²) | O(1) | Too slow for n = 10^5 |
| Linear Scan (Running Counter) | O(n) | O(1) | Optimal. Preferred in interviews |
| Pythonic `split` trick | O(n) | O(n) | Clean but uses extra space |

**Recommended solution for interviews:** Approach 2 - Linear Scan with Running Counter.