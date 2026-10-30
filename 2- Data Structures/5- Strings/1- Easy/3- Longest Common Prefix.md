# Longest Common Prefix

`Meta` • `Google` • `Amazon` • `Microsoft` • `Apple` • `Adobe` • `Bloomberg` • `Visa` • `SAP` • `Educative`

## Problem Statement

Write a function to find the **longest common prefix** string amongst an array of strings.

If there is no common prefix, return an empty string `""`.

- A **prefix** is the beginning part of a word, always starting from the very first letter.
- For example, `"f"`, `"fl"`, and `"flo"` are all prefixes of `"flower"`.

## Examples

**Example 1:**

```ini
Input: strs = ["flower","flow","flight"]
Output: "fl"
Explanation: All three words start with "fl". The third letter is "o", "o", and "i", so they stop matching there.
```

**Example 2:**

```ini
Input: strs = ["dog","racecar","car"]
Output: ""
Explanation: There is no common prefix among the input strings. Even the first letters (d, r, c) are different.
```

## Constraints

- `1 <= strs.length <= 200`
- `0 <= strs[i].length <= 200`
- `strs[i]` consists of only lowercase English letters if it is non-empty.

<br><br>

## The One Rule to Remember

<mark>A common prefix can never be longer than any single word, and it must match every word from the very first letter.</mark>

- The moment two words disagree at some position, the common prefix ends right there.
- Both approaches below are just two different ways of finding that first point of disagreement.

<br><br>

## Approach 1: Sort, Then Compare Only the First and Last Word

### The Idea: Think of a Dictionary Page

Picture one page of a dictionary.

- If the **first word** on the page starts with `"fl"`,
- and the **last word** on the page also starts with `"fl"`,
- then **every word in between** must start with `"fl"` too. They are sandwiched between the two.

Sorting turns our list into exactly that dictionary page.

- After sorting, words that look alike sit next to each other.
- The **first** word and the **last** word are the two **most different** words in the whole list.
- So if those two agree on some beginning letters, **all** the words agree on them.

> We do not need to compare all the words. <mark>Only the two ends of the sorted list need to agree.</mark>

### See It With an Example

```ini
Before sorting:  ["flower", "flow", "flight"]
After sorting:   ["flight", "flow", "flower"]
                    ↑                   ↑
                  first               last
```

- `"flight"` comes first because `i` comes before `o` in the alphabet.
- `"flow"` comes before `"flower"` because a shorter word that is the start of a longer word always comes first.
- Now compare only `"flight"` and `"flower"`: they share `"fl"`. That is the answer.

### Step by Step

1. **Start with an empty answer.**
   - `result = ""`.
2. **Sort the list** in alphabetical order.
3. **Pick the two ends.**
   - `first` is the first word after sorting.
   - `last` is the last word after sorting.
4. **Walk through `first`, one letter at a time** (position `i = 0, 1, 2, ...`).
   - Is `first[i]` the same as `last[i]`?
   - **Yes:** add that letter to `result` and keep going.
   - **No:** the words disagree here. Stop the loop.
5. **Return `result`.**

> Why is it safe to loop over `first` and read `last[i]`? After sorting, either `first` is the shorter one, or the two words disagree somewhere before `last` runs out of letters. Either way, the loop stops before going past the end of `last`.

> Memory hook: <mark>"Sort it like a dictionary. If the first and the last agree, everyone agrees."</mark>

### Solution

```python
def longest_common_prefix(strs):
    result = ""

    # Sort the array of strings
    strs.sort()

    # Get the first and last strings
    first = list(strs[0])
    last = list(strs[-1])

    # Start comparing characters
    for i in range(len(first)):
        if first[i] != last[i]:
            break
        result += first[i]

    return result

# Example usage:
strings = ["flower", "flow", "flight"]
print(longest_common_prefix(strings))  # Output: "fl"
```

### Dry Run

```ini
=====================================================
SCENARIO A: strs = ["flower","flow","flight"]
=====================================================

Setup:
  result = ""

Step 1: Sort the list.
  Before: ["flower", "flow", "flight"]

  How the sorting decides:
    "flight" vs "flow":   f = f, l = l, then i vs o. i comes first. So "flight" goes first.
    "flow" vs "flower":   f, l, o, w all match. "flow" runs out first.
                          The shorter word comes first. So "flow" goes before "flower".

  After:  ["flight", "flow", "flower"]

Step 2: Pick the two ends.
  first = list("flight") = ['f', 'l', 'i', 'g', 'h', 't']
  last  = list("flower") = ['f', 'l', 'o', 'w', 'e', 'r']
  Loop range: range(len(first)) = range(6), so i goes from 0 to 5.

Step 3: Compare letter by letter.

  Iteration 1: i = 0
    first[0] = 'f', last[0] = 'f'
    Are they different? NO. They match.
    Add the letter: result = "" + "f" = "f"

  Iteration 2: i = 1
    first[1] = 'l', last[1] = 'l'
    Are they different? NO. They match.
    Add the letter: result = "f" + "l" = "fl"

  Iteration 3: i = 2
    first[2] = 'i', last[2] = 'o'
    Are they different? YES. The two ends disagree here.
    break → exit the loop immediately.
    (Positions 3, 4, 5 are never checked.)

Notice: we never looked at "flow" (the middle word).
It is sandwiched between "flight" and "flower", so it must also start with "fl".

Return result = "fl"
Output: "fl"  ✓


=====================================================
SCENARIO B: strs = ["dog","racecar","car"]
=====================================================

Setup:
  result = ""

Step 1: Sort the list.
  Before: ["dog", "racecar", "car"]
  First letters are d, r, c. In the alphabet: c, d, r.
  After:  ["car", "dog", "racecar"]

Step 2: Pick the two ends.
  first = list("car")     = ['c', 'a', 'r']
  last  = list("racecar") = ['r', 'a', 'c', 'e', 'c', 'a', 'r']
  Loop range: range(3), so i goes from 0 to 2.

Step 3: Compare letter by letter.

  Iteration 1: i = 0
    first[0] = 'c', last[0] = 'r'
    Are they different? YES.
    break → exit the loop immediately.
    Nothing was ever added to result.

Return result = ""
Output: ""  ✓


=====================================================
SCENARIO C: strs = ["ab","a"]  (the longer word is given first)
=====================================================

Setup:
  result = ""

Step 1: Sort the list.
  Before: ["ab", "a"]
  "a" is the start of "ab", so the shorter word "a" goes first.
  After:  ["a", "ab"]

Step 2: Pick the two ends.
  first = list("a")  = ['a']
  last  = list("ab") = ['a', 'b']
  Loop range: range(1), so i takes only the value 0.

Step 3: Compare letter by letter.

  Iteration 1: i = 0
    first[0] = 'a', last[0] = 'a'
    Are they different? NO. They match.
    Add the letter: result = "" + "a" = "a"

  Loop finished. first has no more letters (i = 1 is outside range(1)).

Note: Sorting put the shorter word first, so the loop ended
when "a" ran out. We never tried to read a letter that does not exist.

Return result = "a"
Output: "a"  ✓


=====================================================
SCENARIO D: strs = ["abc","","abd"]  (one word is empty)
=====================================================

Setup:
  result = ""

Step 1: Sort the list.
  Before: ["abc", "", "abd"]
  The empty word "" comes before everything.
  After:  ["", "abc", "abd"]

Step 2: Pick the two ends.
  first = list("")    = []
  last  = list("abd") = ['a', 'b', 'd']
  Loop range: range(0). The loop has nothing to do.

Step 3: Compare letter by letter.

  Iteration 1:
    range(0) is empty. The loop never runs.

Note: If any word is empty, the common prefix must be empty.
Sorting puts "" first, so this case is handled automatically.

Return result = ""
Output: ""  ✓
```

### Complexity Analysis

Let `N` be the number of words and `M` be the length of the longest word.

- **Time Complexity:** `O(N × M × log N)`.
  - Sorting needs about `N log N` comparisons.
  - Each comparison between two words can look at up to `M` letters.
  - The final letter by letter check is only `O(M)`, which is tiny next to the sort.
- **Space Complexity:** `O(M)` extra.
  - `first`, `last`, and `result` each hold at most `M` letters.
  - Note: Python's built in sort may also use up to `O(N)` temporary memory internally.

### The Demerit

- **Sorting does far more work than needed.**
  - We only want to compare **two** words, but we arrange **all** `N` words to find them.
  - That costs `O(N × M × log N)`, while just reading every letter once would cost only `O(N × M)`.
- **It changes the input list.**
  - `strs.sort()` sorts the list **in place**, so the caller's original list is now in a different order.
  - In real code (and in interviews), quietly changing someone else's data is a side effect people do not expect.
- **It cannot stop early.**
  - In `["dog", "racecar", "car"]`, the very first letters already disagree.
  - But the code still sorts the whole list before it finds that out.

> We need a way that does **not** sort, does **not** touch the input order, and can **give up early** when there is clearly no common prefix. Approach 2 does all three.

<br><br>

## Approach 2: Guess Big, Then Shrink (Horizontal Scanning)

### The Idea: Filing Down a Key

Imagine a key that is a bit too long to fit in several locks.

- You file a little off the **end** of the key and try again.
- You keep filing until it fits the lock.
- Then you try the next lock with the **same, already filed** key.
- After the last lock, whatever is left of the key fits **every** lock.

Here, the key is our **guess** for the prefix, and the locks are the words.

- The common prefix can never be longer than the first word, so start by guessing the **entire first word**.
- For every other word, keep chopping the **last letter** off the guess until the word starts with it.
- The guess only ever gets **shorter**, never longer. So whatever survives all the words is the answer.

### Step by Step

1. **Handle the empty list.**
   - If there are no words, return `""`.
2. **Make the first guess.**
   - `prefix` = the whole first word.
3. **Go through every other word, one by one.**
   - Does this word **start with** `prefix`?
   - **Yes:** this word is happy. Move on to the next word.
   - **No:** chop the last letter off `prefix` and ask again.
4. **Give up early if the guess becomes empty.**
   - If `prefix` shrinks down to `""`, there is no common prefix at all.
   - Return `""` right away. The remaining words do not need to be checked.
5. **All words done?**
   - Return `prefix`. It fits every word.

> Why check against the already shrunk `prefix`? Because it already fits all the earlier words. If it also fits the current word, it fits everyone so far. That is how the answer builds up word by word.

> Memory hook: <mark>"Guess the whole first word. Chop from the end until every word agrees."</mark>

### Solution

```python
class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        if not strs:
            return ""

        prefix = strs[0]

        for string in strs[1:]:
            while not string.startswith(prefix):
                prefix = prefix[:-1]
                if not prefix:
                    return ""

        return prefix
```

### Dry Run

```ini
=====================================================
SCENARIO A: strs = ["flower","flow","flight"]
=====================================================

Check: Is strs empty? NO. Continue.

Setup:
  prefix = strs[0] = "flower"   (the first guess is the whole first word)
  Words left to check: strs[1:] = ["flow", "flight"]

Word 1: string = "flow"

  While check 1:
    Does "flow" start with "flower"? NO. ("flower" is even longer than "flow".)
    Chop the last letter: prefix = "flower"[:-1] = "flowe"
    Is prefix empty? NO. Keep going.

  While check 2:
    Does "flow" start with "flowe"? NO. ("flowe" has 5 letters, "flow" has only 4.)
    Chop the last letter: prefix = "flowe"[:-1] = "flow"
    Is prefix empty? NO. Keep going.

  While check 3:
    Does "flow" start with "flow"? YES. Exit the while loop.

  prefix = "flow"   (fits "flower" and "flow")

Word 2: string = "flight"

  While check 1:
    Does "flight" start with "flow"? NO. (Third letter: 'i' vs 'o'.)
    Chop the last letter: prefix = "flow"[:-1] = "flo"
    Is prefix empty? NO. Keep going.

  While check 2:
    Does "flight" start with "flo"? NO. (Third letter: 'i' vs 'o'.)
    Chop the last letter: prefix = "flo"[:-1] = "fl"
    Is prefix empty? NO. Keep going.

  While check 3:
    Does "flight" start with "fl"? YES. Exit the while loop.

  prefix = "fl"   (fits "flower", "flow", and "flight")

All words checked. The for loop is finished.

How the guess shrank:
  "flower" → "flowe" → "flow" → "flo" → "fl"

The original list was never sorted or changed.

Return prefix = "fl"
Output: "fl"  ✓


=====================================================
SCENARIO B: strs = ["dog","racecar","car"]  (early exit)
=====================================================

Check: Is strs empty? NO. Continue.

Setup:
  prefix = strs[0] = "dog"
  Words left to check: strs[1:] = ["racecar", "car"]

Word 1: string = "racecar"

  While check 1:
    Does "racecar" start with "dog"? NO.
    Chop the last letter: prefix = "dog"[:-1] = "do"
    Is prefix empty? NO. Keep going.

  While check 2:
    Does "racecar" start with "do"? NO.
    Chop the last letter: prefix = "do"[:-1] = "d"
    Is prefix empty? NO. Keep going.

  While check 3:
    Does "racecar" start with "d"? NO.
    Chop the last letter: prefix = "d"[:-1] = ""
    Is prefix empty? YES. There is no common prefix at all.
    Return "" immediately.

Word 2 ("car") is NEVER checked. This is the early exit.
(Approach 1 had to sort all three words before it could find this out.)

Output: ""  ✓


=====================================================
SCENARIO C: strs = ["interview","internet","interval"]
=====================================================

Check: Is strs empty? NO. Continue.

Setup:
  prefix = strs[0] = "interview"
  Words left to check: strs[1:] = ["internet", "interval"]

Word 1: string = "internet"

  While check 1:
    Does "internet" start with "interview"? NO.
    Chop: prefix = "intervie"
    Is prefix empty? NO.

  While check 2:
    Does "internet" start with "intervie"? NO.
    Chop: prefix = "intervi"
    Is prefix empty? NO.

  While check 3:
    Does "internet" start with "intervi"? NO.
    Chop: prefix = "interv"
    Is prefix empty? NO.

  While check 4:
    Does "internet" start with "interv"? NO. (Sixth letter: 'n' vs 'v'.)
    Chop: prefix = "inter"
    Is prefix empty? NO.

  While check 5:
    Does "internet" start with "inter"? YES. Exit the while loop.

  prefix = "inter"

Word 2: string = "interval"

  While check 1:
    Does "interval" start with "inter"? YES. Exit the while loop right away.
    Nothing is chopped. This word was happy with the guess immediately.

  prefix = "inter"

All words checked. The for loop is finished.

Note: Once the guess is short enough, later words often pass on the
very first check. The guess never has to grow back.

Return prefix = "inter"
Output: "inter"  ✓


=====================================================
SCENARIO D: strs = ["alone"]  (only one word)
=====================================================

Check: Is strs empty? NO. Continue.

Setup:
  prefix = strs[0] = "alone"
  Words left to check: strs[1:] = []   (nothing)

For loop:
  The list is empty. The loop never runs.

Note: A single word is its own longest common prefix.

Return prefix = "alone"
Output: "alone"  ✓
```

### Complexity Analysis

Let `N` be the number of words and `M` be the length of the longest word.

- **Time Complexity:** `O(N × M + M²)`.
  - Every word gets one successful `startswith` check, which looks at up to `M` letters: `O(N × M)`.
  - The guess only ever shrinks, so in total it can be chopped at most `M` times across the **whole** run. Each failed check costs up to `M`: `O(M²)`.
  - With `M <= 200`, the chopping part is tiny, so in practice this behaves like `O(N × M)`, with **no sorting** and an **early exit**.
- **Space Complexity:** `O(M)`.
  - `prefix` holds at most `M` letters.
  - Each chop (`prefix[:-1]`) makes a new, shorter string of at most `M` letters.
  - The input list is never sorted or modified.

<br><br>

## Which One to Pick?

- **Approach 1** is a neat trick and easy to remember: "sort it, compare the two ends."
- **Approach 2** is usually the better answer in interviews:
  - No sorting, so less work.
  - The input list stays exactly as it was given.
  - It stops the moment the guess becomes empty.

<br><br>

## Related Problems

- [Implement Trie (Prefix Tree) (208)](https://leetcode.com/problems/implement-trie-prefix-tree/)
- [Replace Words (648)](https://leetcode.com/problems/replace-words/)
- [Longest Word in Dictionary (720)](https://leetcode.com/problems/longest-word-in-dictionary/)
- [Search Suggestions System (1268)](https://leetcode.com/problems/search-suggestions-system/)
- [Check If a Word Occurs As a Prefix of Any Word in a Sentence (1455)](https://leetcode.com/problems/check-if-a-word-occurs-as-a-prefix-of-any-word-in-a-sentence/)
- [Counting Words With a Given Prefix (2185)](https://leetcode.com/problems/counting-words-with-a-given-prefix/)
- [Count Prefixes of a Given String (2255)](https://leetcode.com/problems/count-prefixes-of-a-given-string/)
- [Sum of Prefix Scores of Strings (2416)](https://leetcode.com/problems/sum-of-prefix-scores-of-strings/)
- [Count Prefix and Suffix Pairs I (3042)](https://leetcode.com/problems/count-prefix-and-suffix-pairs-i/)
- [Find the Length of the Longest Common Prefix (3043)](https://leetcode.com/problems/find-the-length-of-the-longest-common-prefix/)
