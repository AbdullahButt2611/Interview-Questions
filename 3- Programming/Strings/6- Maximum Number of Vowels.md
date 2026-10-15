# Maximum Number of Vowels in a Substring of Given Length
`LeetCode 75`

## Problem Statement

Given a string `s` and an integer `k`, return the **maximum number of vowel letters** in any substring of `s` with length `k`.

Vowel letters in English are `'a'`, `'e'`, `'i'`, `'o'`, and `'u'`.

### Example 1:

**Input:**
s = "abciiidef", k = 3\
**Output:**
3\
**Explanation:** The substring "iii" contains 3 vowels.

### Example 2:

**Input:**
s = "aeiou", k = 2\
**Output:**
2\
**Explanation:** Any substring of length 2 contains 2 vowels.

### Example 3:

**Input:**
s = "leetcode", k = 3\
**Output:**
2\
**Explanation:** Substrings like "lee", "eet", and "ode" each contain 2 vowels.

<br>

## Approach: Sliding Window

We can solve this problem efficiently using the **sliding window** technique. Instead of recalculating the number of vowels for each substring, we maintain a running count as the window moves.

### Steps:

1. Create a set of vowels for constant-time lookup.
2. Count the number of vowels in the first window (first `k` characters).
3. As we slide the window:

   * Subtract 1 if the outgoing character is a vowel.
   * Add 1 if the incoming character is a vowel.
4. Keep updating the maximum vowel count found.

This reduces the time complexity from O(n * k) to O(n).

<br>

## Solution Code

```python
class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        vowels = {'a', 'e', 'i', 'o', 'u'}
        count = 0

        # Initial window
        for i in range(k):
            if s[i] in vowels:
                count += 1
        
        max_vowels = count

        # Slide the window
        for i in range(k, len(s)):
            if s[i - k] in vowels:
                count -= 1
            if s[i] in vowels:
                count += 1
            max_vowels = max(max_vowels, count)

        return max_vowels
```

<br>

## Explanation

* We start by counting vowels in the first `k` characters.
* As the window moves forward, we remove the effect of the first character and add the effect of the new one.
* We track the highest count during the process.

This method ensures that each character is processed exactly once.

<br>

## Complexity Analysis

| Metric               | Complexity | Explanation                                              |
| -------------------- | ---------- | -------------------------------------------------------- |
| **Time Complexity**  | O(n)       | Each character is visited once while sliding the window. |
| **Space Complexity** | O(1)       | Only a fixed-size set and counters are used.             |

<br>

## Summary

✅ Uses Sliding Window for efficiency.\
✅ Simple logic with linear time complexity.\
✅ Ideal for interview discussions and performance-critical string problems.
