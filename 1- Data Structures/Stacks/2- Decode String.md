# Decode String
`LeetCode 75`

## Problem Statement

You are given an encoded string `s`. Your task is to return its decoded form.

The encoding rule is:

```
k[encoded_string]
```

* `encoded_string` is repeated exactly `k` times.
* `k` is always a positive integer.
* The input string is always valid.
* There are no spaces in the input.
* Brackets are well formed.
* The original data does not contain digits. Digits are used only for repeat counts.

The decoded string length will never be more than `10^5`.

## Examples

### Example 1

**Input**

```
3[a]2[bc]
```

**Output**

```
aaabcbc
```

### Example 2

**Input**

```
3[a2[c]]
```

**Output**

```
accaccacc
```

### Example 3

**Input**

```
2[abc]3[cd]ef
```

**Output**

```
abcabccdcdcdef
```

<br><br>

## Approach 1: Brute Force Expansion (Not Recommended)

### Idea

One basic idea is to scan the string and expand every pattern as soon as we see it. This works only for very simple cases without nesting.

### Problem With This Approach

* It fails when brackets are nested.
* Managing indexes becomes hard.
* Code becomes messy and error prone.

Because of these issues, this approach is not suitable for interviews.

<br><br>

## Approach 2: Stack Based Solution (Recommended)

### Idea

We process the string from left to right and use a stack to keep track of:

* The string built so far before a `[` appears
* The repeat count linked with that bracket

When we close a bracket `]`, we repeat the current string and attach it back to the previous one.

This method works well even for nested patterns.

### Algorithm

1. Create a stack to store pairs of `(previous_string, repeat_count)`
2. Keep a variable `current_string` for the active text
3. Keep a variable `num` to build repeat counts
4. For each character in the input:

   * If it is a digit, build the number
   * If it is `[`, push current data to stack and reset
   * If it is `]`, pop from stack and repeat
   * If it is a letter, add it to current string
5. Return `current_string`

### Python Code

```python
class Solution:
    def decodeString(self, s: str) -> str:
        stack = []
        current = ""
        num = 0

        for ch in s:
            if ch.isdigit():
                num = num * 10 + int(ch)
            elif ch == '[':
                stack.append((current, num))
                current = ""
                num = 0
            elif ch == ']':
                prev, count = stack.pop()
                current = prev + current * count
            else:
                current += ch

        return current
```

### Explanation

* The stack saves the state before entering a bracket
* When `]` is found, the last saved state is restored
* Nested brackets work naturally because of stack order

### Time and Space Complexity

* **Time Complexity:** `O(n)` where `n` is the length of the input string
* **Space Complexity:** `O(n)` due to stack usage

<br><br>

## Final Notes

* This is the expected solution in most interviews
* Clean logic and easy to explain
* Handles all edge cases within given limits

---

**End of Problem**
