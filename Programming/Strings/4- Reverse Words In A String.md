# Reverse Words in a String
`LeetCode 75`
## Problem Statement

Given an input string `s`, reverse the order of the words.

* A word is defined as a sequence of non-space characters.
* Words in `s` will be separated by at least one space.
* Return a string of words in reverse order, concatenated by a single space.
* The returned string should have no leading or trailing spaces and only a single space between words.

### Examples

**Example 1:**

```
Input: s = "the sky is blue"
Output: "blue is sky the"
```

**Example 2:**

```
Input: s = "  hello world  "
Output: "world hello"
```

**Example 3:**

```
Input: s = "a good   example"
Output: "example good a"
```

### Constraints

* 1 <= s.length <= 10^4
* s contains English letters (upper-case and lower-case), digits, and spaces.
* There is at least one word in s.

<br><br>

## Approaches

### Approach 1: Brute Force using Python Built-ins

**Idea:**

* Use `split()` to automatically handle spaces and generate a list of words.
* Reverse the list of words.
* Join the words with a single space.

**Code:**

```python
class Solution:
    def reverseWords(self, s: str) -> str:
        words = s.split()              # splits by any whitespace and removes extras
        reversed_words = words[::-1]   # reverse the list
        return " ".join(reversed_words)
```

**Complexity:**

* Time: O(n), since we traverse the string once.
* Space: O(n), to store the list of words.




### Approach 2: Manual Split and Reverse (Step 04)

**Problem with Approach 1:**

* While the built-in `split()` is convenient, understanding the manual splitting process helps improve grasp of string traversal, list manipulation, and handling multiple spaces without relying on built-ins.

**Idea:**

1. Traverse the string character by character.
2. Build words manually by accumulating characters.
3. Append complete words to a list whenever a space is encountered.
4. Reverse the list of words.
5. Join words with a single space.

**Code:**

```python
class Solution:
    def reverseWords(self, s: str) -> str:
        words = []  # list to store words
        word = ""  # temporary string to build a word

        for c in s:
            if c != " ":
                word += c       # accumulate characters into word
            elif word:
                words.append(word)  # word completed, add to list
                word = ""      # reset for next word

        if word:              # append the last word if exists
            words.append(word)

        reversed_words = words[::-1]  # reverse the list
        return " ".join(reversed_words)  # join with single space
```

**Complexity:**

* Time: O(n), single traversal of the string.
* Space: O(n), for the list of words.

**Explanation:**

* This approach manually handles spaces and multiple spaces between words.
* Each word is accumulated in a temporary string.
* When a space is encountered, the word is appended to the list.
* Finally, reversing the list gives the words in reversed order, and joining them ensures a single space between words.

<br><br>

### Summary

| Approach                         | Time Complexity | Space Complexity | Notes                                                   |
| -------------------------------- | --------------- | ---------------- | ------------------------------------------------------- |
| Built-in split & reverse         | O(n)            | O(n)             | Clean and efficient, uses Python built-ins              |
| Manual split & reverse (Step 04) | O(n)            | O(n)             | Educational, manually handles spaces and word splitting |

