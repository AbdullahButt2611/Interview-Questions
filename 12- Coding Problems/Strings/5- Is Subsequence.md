# Is Subsequence
`LeetCode 75`

## Problem Statement

Given two strings `s` and `t`, return `true` if `s` is a subsequence of `t`, or `false` otherwise.

A subsequence of a string is a new string that is formed from the original string by deleting some (or none) of the characters without disturbing the relative positions of the remaining characters.
For example, "ace" is a subsequence of "abcde" while "aec" is not.

### Example 1:

**Input:**

```text
s = "abc", t = "ahbgdc"
```

**Output:**

```text
true
```

### Example 2:

**Input:**

```text
s = "axc", t = "ahbgdc"
```

**Output:**

```text
false
```

### Constraints

* 0 <= s.length <= 100
* 0 <= t.length <= 10^4
* `s` and `t` consist only of lowercase English letters.

<br><br>

## Approach: Two Pointer Technique

### Intuition

We can think of this as checking whether all characters of `s` appear in `t` in the same order. We will use two pointers to track positions in both strings.

1. Keep one pointer `i` for string `s` and one for string `t` (the loop).
2. Iterate over each character in `t`.
3. If the current character in `t` matches the current character in `s`, move the pointer `i` to the next position in `s`.
4. If at any point, `i` reaches the length of `s`, that means every character in `s` was found in order.

### Code

```python
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        i = 0
        for ch in t:
            if i < len(s) and ch == s[i]:
                i += 1
        return i == len(s)
```

### Explanation

* We start with `i = 0` which tracks the progress in `s`.
* For each character `ch` in `t`, we compare it with `s[i]`.
* If they match, move to the next character in `s`.
* If `i` reaches `len(s)` before the loop ends, it means all characters of `s` are found.

**Example walkthrough:**

```
s = "abc", t = "ahbgdc"
```

* Start: i = 0 (s[i] = 'a')
* t[0] = 'a' → match → i = 1
* t[1] = 'h' → no match
* t[2] = 'b' → match → i = 2
* t[3] = 'g' → no match
* t[4] = 'd' → no match
* t[5] = 'c' → match → i = 3 → len(s) = 3 → return `True`

### Complexity Analysis

* **Time Complexity:** O(len(t))
  We go through all characters of `t` once.
* **Space Complexity:** O(1)
  We only use a few variables, no extra space.

### Pros

* Very efficient for single checks.
* Easy to understand and implement.

### Cons

* If we need to check *many* `s` strings against the same `t`, this would re-scan `t` each time.

<br>

## Final Thoughts

The two-pointer approach is ideal for this problem and forms the foundation for many string and sequence matching problems. It’s clean, simple, and efficient for single queries.
