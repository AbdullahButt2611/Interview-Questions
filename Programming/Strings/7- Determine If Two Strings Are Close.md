# Determine if Two Strings Are Close
`LeetCode 75`

## Problem Statement

Two strings are called **close** if one string can be changed into the other by using the following operations any number of times:

**Operation 1**: Swap any two existing characters.

* Example: `abcde -> aecdb`

**Operation 2**: Pick two existing characters and change all occurrences of the first character into the second character, and all occurrences of the second character into the first character.

* Example: `aacabb -> bbcbaa` (all `a` become `b` and all `b` become `a`)

You are given two strings `word1` and `word2`.

Return `true` if `word1` and `word2` are close. Otherwise, return `false`.

## Constraints

* `1 <= word1.length, word2.length <= 10^5`
* `word1` and `word2` contain only lowercase English letters

## Key Observations

* Operation 1 allows any reordering of characters.
* Operation 2 allows renaming characters, but only between characters that already exist in the string.
* No new characters can be created.
* Character counts matter, but exact character names do not.

<br><br>

## Approach 1: Direct Mapping Check (Initial Idea)

### Idea

1. If the lengths of both strings are different, return `false`.
2. Try to map characters from `word1` to characters in `word2` so that counts match.
3. Make sure the mapping is consistent in both directions.

### Why This Is Not Ideal

* This approach becomes complex when multiple characters have the same count.
* It requires careful handling of conflicts in mapping.
* Implementation is longer and easier to get wrong.

Because of this, we look for a cleaner and safer method.

<br><br>

## Approach 2: Frequency and Character Set Check (Final Solution)

### Idea

Two strings are close if and only if:

1. They have the same length.
2. They use the same set of characters.
3. The list of character frequencies is the same when order is ignored.

### Why This Works

* Operation 1 means order does not matter.
* Operation 2 means we can swap character names, but only among existing characters.
* So:

  * The set of characters must match.
  * The multiset of frequencies must match.

### Steps

1. If lengths are different, return `false`.
2. Count the frequency of each character in both strings.
3. Check that both strings contain the same characters.
4. Sort the frequency values of both strings.
5. If the sorted frequency lists are equal, return `true`. Otherwise, return `false`.

### Code (Python)

```python
class Solution:
    def closeStrings(self, word1: str, word2: str) -> bool:
        if len(word1) != len(word2):
            return False

        from collections import Counter

        freq1 = Counter(word1)
        freq2 = Counter(word2)

        # Same character set check
        if set(freq1.keys()) != set(freq2.keys()):
            return False

        # Same frequency distribution check
        if sorted(freq1.values()) != sorted(freq2.values()):
            return False

        return True
```

### Explanation

* `Counter` helps count how many times each character appears.
* Comparing key sets ensures no extra or missing characters.
* Sorting the frequency values removes the effect of character names.
* If both checks pass, the strings can be transformed using the allowed operations.

## Time and Space Complexity

* **Time Complexity**: `O(n log n)` due to sorting frequencies
* **Space Complexity**: `O(1)` since there are at most 26 lowercase letters

<br><br>

## Final Notes

This approach is short, clear, and safe for large inputs. It directly matches what the allowed operations can and cannot change, which makes it a strong choice for interviews and practice problems.
