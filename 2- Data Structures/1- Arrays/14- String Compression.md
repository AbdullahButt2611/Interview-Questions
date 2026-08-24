# String Compression
`LeetCode 75`

## Problem Statement

Given an array of characters `chars`, compress it using the following algorithm:

Begin with an empty string `s`. For each group of consecutive repeating characters in `chars`:

* If the group's length is 1, append the character to `s`.
* Otherwise, append the character followed by the group's length.

The compressed string `s` should **not** be returned separately, but instead be stored **in-place** in the input character array `chars`. Group lengths that are 10 or longer will be split into multiple characters in `chars`.

After you are done modifying the input array, return the new length of the array.

> **Note:** The characters in the array beyond the returned length do not matter and should be ignored.

### Example 1:

**Input:** `chars = ["a","a","b","b","c","c","c"]`
**Output:** `Return 6, and the first 6 characters of the input array should be: ["a","2","b","2","c","3"]`
**Explanation:** The groups are "aa", "bb", and "ccc". This compresses to "a2b2c3".

### Example 2:

**Input:** `chars = ["a"]`
**Output:** `Return 1, and the first character of the input array should be: ["a"]`

### Example 3:

**Input:** `chars = ["a","b","b","b","b","b","b","b","b","b","b","b","b"]`
**Output:** `Return 4, and the first 4 characters of the input array should be: ["a","b","1","2"]`
**Explanation:** The groups are "a" and "bbbbbbbbbbbb". This compresses to "ab12".

### Constraints:

* `1 <= chars.length <= 2000`
* `chars[i]` is a lowercase English letter, uppercase English letter, digit, or symbol.

<br><br>

## Approach 1: Without In-Place Constraint

### Idea

We can traverse the array, count consecutive repeating characters, and build the compressed version as a new string. After that, we overwrite the original array with the compressed content.

### Code

```python
class Solution:
    def compress(self, chars: List[str]) -> int:
        if not chars:
            return 0

        s = ""
        count = 1

        for i in range(1, len(chars) + 1):
            if i < len(chars) and chars[i] == chars[i - 1]:
                count += 1
            else:
                s += chars[i - 1]
                if count > 1:
                    s += str(count)
                count = 1

        for i in range(len(s)):
            chars[i] = s[i]

        return len(s)
```

### Explanation

* Traverse the list and count consecutive identical characters.
* Append the character and its count (if greater than 1) to a temporary string.
* Copy the result back into the original array.

### Complexity

* **Time Complexity:** O(n)
* **Space Complexity:** O(n)

<br>

## Approach 2: In-Place Compression

### Idea

Instead of creating a new string, we can perform the compression directly inside the `chars` array using a pointer to track where to write the next character or digit.

### Code

```python
class Solution:
    def compress(self, chars: List[str]) -> int:
        if not chars:
            return 0

        write_pos = 0
        count = 1

        for i in range(1, len(chars) + 1):
            if i < len(chars) and chars[i] == chars[i - 1]:
                count += 1
            else:
                chars[write_pos] = chars[i - 1]
                write_pos += 1

                if count > 1:
                    for c in str(count):
                        chars[write_pos] = c
                        write_pos += 1
                count = 1

        return write_pos
```

### Explanation

* `write_pos` keeps track of where to write the compressed data.
* Each time a new character sequence ends, we write the character and its count.
* No slicing or string concatenation is used, ensuring it’s done completely in-place.

### Complexity

* **Time Complexity:** O(n)
* **Space Complexity:** O(1)

<br>

## Approach 3: Optimized and Cleaner Two-Pointer Approach

### Idea

This version improves readability and separates reading from writing using two pointers:

* `read` pointer scans the array to count characters.
* `write` pointer writes the compressed form.

### Code

```python
class Solution:
    def compress(self, chars: List[str]) -> int:
        write = 0
        read = 0

        while read < len(chars):
            char = chars[read]
            count = 0

            # Count consecutive occurrences of the same character
            while read < len(chars) and chars[read] == char:
                read += 1
                count += 1

            # Write the character
            chars[write] = char
            write += 1

            # Write the count if greater than 1
            if count > 1:
                for c in str(count):
                    chars[write] = c
                    write += 1

        return write
```

### Explanation

* The `read` pointer iterates through the input to identify character groups.
* The `write` pointer stores compressed results directly in the input list.
* This separation enhances readability and ensures the solution remains both efficient and elegant.

### Complexity

* **Time Complexity:** O(n)
* **Space Complexity:** O(1)

<br>

## Summary

| Approach | Description                    | Time | Space |
| -------- | ------------------------------ | ---- | ----- |
| 1        | Without in-place constraint    | O(n) | O(n)  |
| 2        | In-place compression           | O(n) | O(1)  |
| 3        | Optimized two-pointer approach | O(n) | O(1)  |

