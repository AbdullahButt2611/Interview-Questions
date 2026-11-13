## Merge Strings Alternately
`Leetcode 75`

You are given two strings word1 and word2. Merge the strings by adding letters in alternating order, starting with word1. If a string is longer than the other, append the additional letters onto the end of the merged string.

Return the merged string.

#### Example 1:

Input: word1 = "abc", word2 = "pqr" \
Output: "apbqcr" \
Explanation: The merged string will be merged as so: \
word1:  a   b   c \
word2:    p   q   r \
merged: a p b q c r

---

### Brute Force Solution

```
class Solution(object):
    def mergeAlternately(self, word1, word2):
        result = ""

        while word1 and word2:
            result += word1[:1]
            result += word2[:1]

            word1 = word1[1:]
            word2 = word2[1:]
        
        if word1: 
            result += word1
        
        if word2: 
            result += word2
        
        return result
```

#### Points to Ponder

1. ##### String concatenation inefficiency:
    In Python, strings are immutable, so `result += word[:1]` creates a new string every time → This results in **O(n²)** time complexity for large inputs.
2. ##### Slicing Overhead:
    Using `word1 = word1[1:]` creates a new string each time, which also increases memory usage.

---

### Optimized Approach #1 - Use a List (Avoid String Concatenation)

Instead of repeatedly creating new strings, we append to a list and join at the end.
This changes complexity to O(n).

```
class Solution(object):
    def mergeAlternately(self, word1, word2):
        result = []
        i, j = 0, 0
        
        while i < len(word1) and j < len(word2):
            result.append(word1[i])
            result.append(word2[j])
            i += 1
            j += 1
        
        if i < len(word1):
            result.append(word1[i:])
        if j < len(word2):
            result.append(word2[j:])
        
        return "".join(result)
```

##### Why Better
`.append()` is `O(1)`, and `"".join()` is `O(n)` → total `O(n)` time.

---

### Optimized Approach #2 — Zip + Join
- zip takes two (or more) iterables and returns an iterator of tuples, where each tuple contains one item from each iterable, paired by position.
- **Important**: zip stops when the shortest iterable is exhausted.

#### Examples:
```
list(zip([1,2,3], ['a','b','c']))
# => [(1, 'a'), (2, 'b'), (3, 'c')]
```

If you know Python well, you can use zip to pair characters and flatten them.

```
class Solution(object):
    def mergeAlternately(self, word1, word2):
        merged = [a + b for a, b in zip(word1, word2)]
        return "".join(merged) + word1[len(word2):] + word2[len(word1):]
```