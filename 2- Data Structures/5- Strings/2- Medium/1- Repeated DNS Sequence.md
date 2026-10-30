# Repeated DNA Sequences

`Google` • `LinkedIn` • `Amazon` • `Eduucative`

## Problem Statement

The DNA sequence is composed of a series of nucleotides abbreviated as `'A'`, `'C'`, `'G'`, and `'T'`.

- For example, `"ACGAATTCCG"` is a DNA sequence.

When studying DNA, it is useful to identify repeated sequences within the DNA.

Given a string `s` that represents a DNA sequence, return all the **10-letter-long** sequences (substrings) that occur **more than once** in a DNA molecule. You may return the answer in **any order**.

## Examples

**Example 1:**

```ini
Input: s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
Output: ["AAAAACCCCC","CCCCCAAAAA"]
Explanation: "AAAAACCCCC" starts at index 0 and again at index 10.
"CCCCCAAAAA" starts at index 5 and again at index 16.
```

**Example 2:**

```ini
Input: s = "AAAAAAAAAAAAA"
Output: ["AAAAAAAAAA"]
Explanation: "AAAAAAAAAA" appears 4 times (the copies overlap), but it is listed only once.
```

## Constraints

- `1 <= s.length <= 10^5`
- `s[i]` is either `'A'`, `'C'`, `'G'`, or `'T'`.

<br><br>

## Approach

### The One Rule to Remember

<mark>If you have seen it before, it is a repeat.</mark>

- Keep a memory of every 10-letter piece you have already met.
- When a piece shows up that is already in your memory, you found a repeat.

### The Idea: A 10-Letter Window

Imagine a small window that shows exactly **10 letters** at a time.

```ini
s = A A A A A C C C C C A A A A A C C C ...
    [  window at i=0  ]
      [  window at i=1  ]
        [  window at i=2  ]
```

- Put the window at the very start of the string.
- Read the 10 letters inside it. That is one piece.
- Slide the window **one step** to the right and read the next piece.
- Keep sliding until the window reaches the end of the string.

This way, we look at **every** 10-letter piece of the string, one by one.

### Two Notebooks

We keep two notebooks (two sets):

- **`seq_seen`** is the "I have met this" notebook.
  - Every piece we read goes in here.
- **`repeated_seq`** is the "this is a repeat" notebook.
  - A piece goes in here only when we meet it a **second** time.

> Why is `repeated_seq` a set and not a list? A piece can appear 3, 4, or more times. A list would write it down again and again. A set keeps only **one copy**, so the answer never has duplicates.

### How Many Windows?

- A 10-letter window fits only while there are at least 10 letters left.
- The last window starts at index `len(s) - 10`.
- So the window starts go from `0` to `len(s) - 10`, which is `range(len(s) - 9)`.

> If the string is shorter than 10 letters, `len(s) - 9` is zero or negative, so the loop never runs and the answer is an empty list. No special check is needed.

### Step by Step

1. **Get ready.**
   - Create an empty `seq_seen` set.
   - Create an empty `repeated_seq` set.
2. **Slide the window.** For every start index `i` from `0` to `len(s) - 10`:
   - **Read** the piece: `seq = s[i:i+10]`.
   - **Check** the "met" notebook: is `seq` already in `seq_seen`?
     - **Yes:** this is a repeat. Add it to `repeated_seq`.
     - **No:** nothing special, it is new.
   - **Remember** it: add `seq` to `seq_seen`.
3. **Finish.**
   - Turn `repeated_seq` into a list and return it.

> Memory hook: <mark>"Slide the window, read 10 letters. Seen before? It's a repeat. Always remember what you saw."</mark>

<br><br>

## Solution

```python
class Solution:
    def findRepeatedDnaSequences(self, s: str) -> list[str]:
        seq_seen = set()
        repeated_seq = set()

        for i in range(len(s) - 9):
            seq = s[i:i+10]
            if seq in seq_seen:
                repeated_seq.add(seq)
            seq_seen.add(seq)

        return list(repeated_seq)
```

<br><br>

## Dry Run

```ini
=====================================================
SCENARIO A: s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
=====================================================

The string with its indexes:

  Index:  0         1         2         3
          01234567890123456789012345678901
  s    =  AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT

Setup:
  len(s)       = 32
  seq_seen     = set()   (empty)
  repeated_seq = set()   (empty)
  Loop range:  range(32 - 9) = range(23)
  So i goes from 0 to 22 (23 windows in total).

Iteration 1: i = 0
  Read:     seq = s[0:10] = "AAAAACCCCC"
  Check:    Is "AAAAACCCCC" in seq_seen? NO. First time we meet it.
  Remember: add "AAAAACCCCC" to seq_seen.
  seq_seen size = 1
  repeated_seq  = {}

Iteration 2: i = 1
  Read:     seq = s[1:11] = "AAAACCCCCA"
  Check:    Is "AAAACCCCCA" in seq_seen? NO. New.
  Remember: add "AAAACCCCCA" to seq_seen.
  seq_seen size = 2
  repeated_seq  = {}

Iteration 3: i = 2
  Read:     seq = s[2:12] = "AAACCCCCAA"
  Check:    Is "AAACCCCCAA" in seq_seen? NO. New.
  Remember: add "AAACCCCCAA" to seq_seen.
  seq_seen size = 3
  repeated_seq  = {}

Iteration 4: i = 3
  Read:     seq = s[3:13] = "AACCCCCAAA"
  Check:    Is "AACCCCCAAA" in seq_seen? NO. New.
  Remember: add "AACCCCCAAA" to seq_seen.
  seq_seen size = 4
  repeated_seq  = {}

Iteration 5: i = 4
  Read:     seq = s[4:14] = "ACCCCCAAAA"
  Check:    Is "ACCCCCAAAA" in seq_seen? NO. New.
  Remember: add "ACCCCCAAAA" to seq_seen.
  seq_seen size = 5
  repeated_seq  = {}

Iteration 6: i = 5
  Read:     seq = s[5:15] = "CCCCCAAAAA"
  Check:    Is "CCCCCAAAAA" in seq_seen? NO. New.
  Remember: add "CCCCCAAAAA" to seq_seen.
  seq_seen size = 6
  repeated_seq  = {}

Iteration 7: i = 6
  Read:     seq = s[6:16] = "CCCCAAAAAC"
  Check:    Is "CCCCAAAAAC" in seq_seen? NO. New.
  Remember: add "CCCCAAAAAC" to seq_seen.
  seq_seen size = 7
  repeated_seq  = {}

Iteration 8: i = 7
  Read:     seq = s[7:17] = "CCCAAAAACC"
  Check:    Is "CCCAAAAACC" in seq_seen? NO. New.
  Remember: add "CCCAAAAACC" to seq_seen.
  seq_seen size = 8
  repeated_seq  = {}

Iteration 9: i = 8
  Read:     seq = s[8:18] = "CCAAAAACCC"
  Check:    Is "CCAAAAACCC" in seq_seen? NO. New.
  Remember: add "CCAAAAACCC" to seq_seen.
  seq_seen size = 9
  repeated_seq  = {}

Iteration 10: i = 9
  Read:     seq = s[9:19] = "CAAAAACCCC"
  Check:    Is "CAAAAACCCC" in seq_seen? NO. New.
  Remember: add "CAAAAACCCC" to seq_seen.
  seq_seen size = 10
  repeated_seq  = {}

Iteration 11: i = 10
  Read:     seq = s[10:20] = "AAAAACCCCC"
  Check:    Is "AAAAACCCCC" in seq_seen? YES. We met it at i = 0.
            This is a REPEAT. Add it to repeated_seq.
  Remember: add "AAAAACCCCC" to seq_seen (already there, so nothing changes).
  seq_seen size = 10
  repeated_seq  = {"AAAAACCCCC"}

Iteration 12: i = 11
  Read:     seq = s[11:21] = "AAAACCCCCC"
  Check:    Is "AAAACCCCCC" in seq_seen? NO.
            (Careful: we saw "AAAACCCCCA" at i = 1, but that ends in A, not C.
             One letter different means a different piece.)
  Remember: add "AAAACCCCCC" to seq_seen.
  seq_seen size = 11
  repeated_seq  = {"AAAAACCCCC"}

Iteration 13: i = 12
  Read:     seq = s[12:22] = "AAACCCCCCA"
  Check:    Is "AAACCCCCCA" in seq_seen? NO. New.
  Remember: add "AAACCCCCCA" to seq_seen.
  seq_seen size = 12
  repeated_seq  = {"AAAAACCCCC"}

Iteration 14: i = 13
  Read:     seq = s[13:23] = "AACCCCCCAA"
  Check:    Is "AACCCCCCAA" in seq_seen? NO. New.
  Remember: add "AACCCCCCAA" to seq_seen.
  seq_seen size = 13
  repeated_seq  = {"AAAAACCCCC"}

Iteration 15: i = 14
  Read:     seq = s[14:24] = "ACCCCCCAAA"
  Check:    Is "ACCCCCCAAA" in seq_seen? NO. New.
  Remember: add "ACCCCCCAAA" to seq_seen.
  seq_seen size = 14
  repeated_seq  = {"AAAAACCCCC"}

Iteration 16: i = 15
  Read:     seq = s[15:25] = "CCCCCCAAAA"
  Check:    Is "CCCCCCAAAA" in seq_seen? NO. New.
  Remember: add "CCCCCCAAAA" to seq_seen.
  seq_seen size = 15
  repeated_seq  = {"AAAAACCCCC"}

Iteration 17: i = 16
  Read:     seq = s[16:26] = "CCCCCAAAAA"
  Check:    Is "CCCCCAAAAA" in seq_seen? YES. We met it at i = 5.
            This is a REPEAT. Add it to repeated_seq.
  Remember: add "CCCCCAAAAA" to seq_seen (already there, so nothing changes).
  seq_seen size = 15
  repeated_seq  = {"AAAAACCCCC", "CCCCCAAAAA"}

Iteration 18: i = 17
  Read:     seq = s[17:27] = "CCCCAAAAAG"
  Check:    Is "CCCCAAAAAG" in seq_seen? NO. New.
  Remember: add "CCCCAAAAAG" to seq_seen.
  seq_seen size = 16
  repeated_seq  = {"AAAAACCCCC", "CCCCCAAAAA"}

Iteration 19: i = 18
  Read:     seq = s[18:28] = "CCCAAAAAGG"
  Check:    Is "CCCAAAAAGG" in seq_seen? NO. New.
  Remember: add "CCCAAAAAGG" to seq_seen.
  seq_seen size = 17
  repeated_seq  = {"AAAAACCCCC", "CCCCCAAAAA"}

Iteration 20: i = 19
  Read:     seq = s[19:29] = "CCAAAAAGGG"
  Check:    Is "CCAAAAAGGG" in seq_seen? NO. New.
  Remember: add "CCAAAAAGGG" to seq_seen.
  seq_seen size = 18
  repeated_seq  = {"AAAAACCCCC", "CCCCCAAAAA"}

Iteration 21: i = 20
  Read:     seq = s[20:30] = "CAAAAAGGGT"
  Check:    Is "CAAAAAGGGT" in seq_seen? NO. New.
  Remember: add "CAAAAAGGGT" to seq_seen.
  seq_seen size = 19
  repeated_seq  = {"AAAAACCCCC", "CCCCCAAAAA"}

Iteration 22: i = 21
  Read:     seq = s[21:31] = "AAAAAGGGTT"
  Check:    Is "AAAAAGGGTT" in seq_seen? NO. New.
  Remember: add "AAAAAGGGTT" to seq_seen.
  seq_seen size = 20
  repeated_seq  = {"AAAAACCCCC", "CCCCCAAAAA"}

Iteration 23: i = 22  (the last window, it ends exactly at index 31)
  Read:     seq = s[22:32] = "AAAAGGGTTT"
  Check:    Is "AAAAGGGTTT" in seq_seen? NO. New.
  Remember: add "AAAAGGGTTT" to seq_seen.
  seq_seen size = 21
  repeated_seq  = {"AAAAACCCCC", "CCCCCAAAAA"}

Loop finished. i = 23 is outside range(23), so we stop.

Summary:
  23 windows were read.
  21 different pieces were seen.
  2 of them showed up twice:
    "AAAAACCCCC"  at i = 0 and i = 10
    "CCCCCAAAAA"  at i = 5 and i = 16

Return list(repeated_seq)
Output: ["AAAAACCCCC","CCCCCAAAAA"]  ✓  (any order is accepted)


=====================================================
SCENARIO B: s = "AAAAAAAAAAAAA"  (same piece many times)
=====================================================

The string with its indexes:

  Index:  0         1
          0123456789012
  s    =  AAAAAAAAAAAAA

Setup:
  len(s)       = 13
  seq_seen     = set()   (empty)
  repeated_seq = set()   (empty)
  Loop range:  range(13 - 9) = range(4)
  So i goes from 0 to 3 (4 windows in total).

Iteration 1: i = 0
  Read:     seq = s[0:10] = "AAAAAAAAAA"
  Check:    Is "AAAAAAAAAA" in seq_seen? NO. First time we meet it.
  Remember: add "AAAAAAAAAA" to seq_seen.
  seq_seen     = {"AAAAAAAAAA"}
  repeated_seq = {}

Iteration 2: i = 1
  Read:     seq = s[1:11] = "AAAAAAAAAA"
  Check:    Is "AAAAAAAAAA" in seq_seen? YES. This is a REPEAT.
            Add it to repeated_seq.
  Remember: add to seq_seen (already there, nothing changes).
  seq_seen     = {"AAAAAAAAAA"}
  repeated_seq = {"AAAAAAAAAA"}

Iteration 3: i = 2
  Read:     seq = s[2:12] = "AAAAAAAAAA"
  Check:    Is "AAAAAAAAAA" in seq_seen? YES. A repeat again.
            Add it to repeated_seq.
            It is ALREADY in repeated_seq, and a set keeps only one copy.
            So nothing changes.
  Remember: add to seq_seen (already there, nothing changes).
  seq_seen     = {"AAAAAAAAAA"}
  repeated_seq = {"AAAAAAAAAA"}

Iteration 4: i = 3  (the last window, it ends exactly at index 12)
  Read:     seq = s[3:13] = "AAAAAAAAAA"
  Check:    Is "AAAAAAAAAA" in seq_seen? YES. A repeat again.
            Already in repeated_seq. Nothing changes.
  Remember: nothing changes.
  seq_seen     = {"AAAAAAAAAA"}
  repeated_seq = {"AAAAAAAAAA"}

Loop finished. i = 4 is outside range(4), so we stop.

Note: The piece appeared 4 times, but the answer lists it only ONCE.
That is exactly why repeated_seq is a set and not a list.
(With a list, the output would wrongly be ["AAAAAAAAAA","AAAAAAAAAA","AAAAAAAAAA"].)

Return list(repeated_seq)
Output: ["AAAAAAAAAA"]  ✓


=====================================================
SCENARIO C: s = "ACGT"  (shorter than 10 letters)
=====================================================

Setup:
  len(s)       = 4
  seq_seen     = set()
  repeated_seq = set()
  Loop range:  range(4 - 9) = range(-5)

Iteration 1:
  range(-5) is empty. The loop never runs.
  A 10-letter window cannot fit inside a 4-letter string.

Return list(repeated_seq) = []
Output: []  ✓
```

<br><br>

## Complexity Analysis

- **Time Complexity:** `O(N)`, where `N` is the length of `s`.
  - The window slides about `N - 9` times.
  - Each step cuts a 10-letter piece and looks it up in a set. The length `10` is fixed, so each step is constant work.
  - More precisely it is `O(10 × N)`, and since `10` never changes, that is `O(N)`.
- **Space Complexity:** `O(N)`.
  - `seq_seen` can hold up to `N - 9` different pieces, each 10 letters long.
  - `repeated_seq` holds at most the same number of pieces.

<br><br>

## Related Problems

- [Contains Duplicate (217)](https://leetcode.com/problems/contains-duplicate/)
- [Contains Duplicate II (219)](https://leetcode.com/problems/contains-duplicate-ii/)
- [Find All Anagrams in a String (438)](https://leetcode.com/problems/find-all-anagrams-in-a-string/)
- [Find All Duplicates in an Array (442)](https://leetcode.com/problems/find-all-duplicates-in-an-array/)
- [Repeated Substring Pattern (459)](https://leetcode.com/problems/repeated-substring-pattern/)
- [Permutation in String (567)](https://leetcode.com/problems/permutation-in-string/)
- [Repeated String Match (686)](https://leetcode.com/problems/repeated-string-match/)
- [Longest Duplicate Substring (1044)](https://leetcode.com/problems/longest-duplicate-substring/)
- [Longest Repeating Substring (1062)](https://leetcode.com/problems/longest-repeating-substring/)
- [Substring with Concatenation of All Words (30)](https://leetcode.com/problems/substring-with-concatenation-of-all-words/)
