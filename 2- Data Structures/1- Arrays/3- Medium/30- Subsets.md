# Subsets

`Meta` • `Amazon` • `Microsoft` • `Fiverr` • `Visnext`

## Problem Statement

Given an integer array `nums` of **unique** elements, return all possible subsets (the **power set**).

The solution set **must not** contain duplicate subsets. Return the solution in **any order**.

## Examples

**Example 1:**

```ini
Input: nums = [1,2,3]
Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
```

**Example 2:**

```ini
Input: nums = [0]
Output: [[],[0]]
```

## Constraints

- `1 <= nums.length <= 10`
- `-10 <= nums[i] <= 10`
- All the numbers of `nums` are **unique**.

<br><br>

## The One Rule to Remember

For every element, you have <mark>only two choices: take it, or leave it</mark>.

- 1 element → `2` choices → `2` subsets.
- 2 elements → `2 × 2` → `4` subsets.
- 3 elements → `2 × 2 × 2` → `8` subsets.
- `n` elements → `2^n` subsets.

So every subset is just **one combination of "take" and "leave" decisions**. The two approaches below are two different ways of making all those decisions.

> The empty subset `[]` (leave everything) is always part of the answer.

<br><br>

## Approach 1: The Simple Way (Grow the List)

### The Idea

Start with only the empty subset. Then bring in the elements **one at a time**.

When a new element arrives, every subset you already have splits into **two versions**:

- The old version **without** the new element (already in the list, keep it).
- A new version **with** the new element (make a copy and add it).

So the list **doubles** with every element: `1 → 2 → 4 → 8`.

**See it with `[1, 2, 3]`:**

```ini
Start:            [ [] ]
Bring in 1:       [ [], [1] ]
Bring in 2:       [ [], [1], [2], [1,2] ]
Bring in 3:       [ [], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3] ]
```

### Steps

1. **Start the result with one empty subset:** `result = [[]]`.
2. **Pick the next element `num`** from `nums`.
3. **Make the new subsets.**
   - Create an empty list `new_subsets`.
   - For every subset already in `result`, make a copy with `num` added at the end.
   - Put that copy into `new_subsets`.
4. **Add `new_subsets` into `result`.**
5. **Repeat** Steps 2 to 4 for every element, then return `result`.

> Why build `new_subsets` separately? If you added copies straight into `result` while looping over it, the loop would keep finding the copies you just added and **never end**.

> Memory hook: <mark>"Every new number doubles the list: keep the old ones, copy them with the new number."</mark>

### Solution

```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = [[]]
        for num in nums:
            new_subsets = []
            for subset in result:
                new_subsets.append(subset + [num])
            result += new_subsets
        return result
```

### Dry Run

```ini
=====================================================
SCENARIO A: nums = [1,2,3]
=====================================================

Setup:
  result = [[]]      (start with only the empty subset)

Iteration 1: num = 1
  new_subsets = []
  Copy every subset in result and add 1:
    subset = []  →  [] + [1] = [1]
    new_subsets = [[1]]
  No more subsets in result. Copying is done.
  Add new_subsets into result:
    result = [[]] + [[1]]
    result = [[], [1]]
  Size went 1 → 2

Iteration 2: num = 2
  new_subsets = []
  Copy every subset in result and add 2:
    subset = []   →  [] + [2]  = [2]
    new_subsets = [[2]]
    subset = [1]  →  [1] + [2] = [1, 2]
    new_subsets = [[2], [1, 2]]
  No more subsets in result. Copying is done.
  Add new_subsets into result:
    result = [[], [1]] + [[2], [1, 2]]
    result = [[], [1], [2], [1, 2]]
  Size went 2 → 4

Iteration 3: num = 3
  new_subsets = []
  Copy every subset in result and add 3:
    subset = []      →  [] + [3]     = [3]
    new_subsets = [[3]]
    subset = [1]     →  [1] + [3]    = [1, 3]
    new_subsets = [[3], [1, 3]]
    subset = [2]     →  [2] + [3]    = [2, 3]
    new_subsets = [[3], [1, 3], [2, 3]]
    subset = [1, 2]  →  [1, 2] + [3] = [1, 2, 3]
    new_subsets = [[3], [1, 3], [2, 3], [1, 2, 3]]
  No more subsets in result. Copying is done.
  Add new_subsets into result:
    result = [[], [1], [2], [1, 2]] + [[3], [1, 3], [2, 3], [1, 2, 3]]
    result = [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
  Size went 4 → 8

Loop finished. All 3 elements brought in.

Size check: 2^3 = 8 subsets ✓
Return result
Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]  ✓


=====================================================
SCENARIO B: nums = [0]
=====================================================

Setup:
  result = [[]]

Iteration 1: num = 0
  new_subsets = []
  Copy every subset in result and add 0:
    subset = []  →  [] + [0] = [0]
    new_subsets = [[0]]
  Add new_subsets into result:
    result = [[], [0]]
  Size went 1 → 2

Loop finished. All 1 element brought in.

Size check: 2^1 = 2 subsets ✓
Return result
Output: [[],[0]]  ✓
```

### Complexity Analysis

- **Time Complexity:** `O(N × 2^N)`, where `N` is the length of `nums`.
  - We create `2^N` subsets in total.
  - Each copy can hold up to `N` elements, so making it costs up to `O(N)`.
- **Space Complexity:** `O(N × 2^N)`.
  - The answer itself holds `2^N` subsets of up to `N` elements each.
  - `new_subsets` is temporary and ends up as part of that same output.

<br><br>

## Approach 2: Bit Manipulation (Light Switches)

### The Idea

Picture one **light switch** for every element.

- Switch **ON** (`1`) → take the element.
- Switch **OFF** (`0`) → leave it.

A row of `n` switches is exactly a **binary number** with `n` digits. And counting from `0` to `2^n - 1` in binary walks through **every possible ON/OFF pattern exactly once**. So each number is one subset.

**See it with `[1, 2, 3]`** (bits read from **right to left**, the rightmost bit belongs to `nums[0]`):

```ini
Number   Binary   Switches (nums[2] nums[1] nums[0])   Subset
  0       000          3:OFF  2:OFF  1:OFF            []
  1       001          3:OFF  2:OFF  1:ON             [1]
  2       010          3:OFF  2:ON   1:OFF            [2]
  3       011          3:OFF  2:ON   1:ON             [1,2]
  4       100          3:ON   2:OFF  1:OFF            [3]
  5       101          3:ON   2:OFF  1:ON             [1,3]
  6       110          3:ON   2:ON   1:OFF            [2,3]
  7       111          3:ON   2:ON   1:ON             [1,2,3]
```

### The Two Tiny Tools We Need

- `1 << j` → a number where **only switch `j` is ON**.
  - `1 << 0 = 001`, `1 << 1 = 010`, `1 << 2 = 100`.
- `mask & (1 << j)` → "Is switch `j` ON in `mask`?"
  - Not zero → **ON**, take `nums[j]`.
  - Zero → **OFF**, skip it.

### Steps

1. **Count the total subsets:** `1 << n` (same as `2^n`).
2. **Loop `mask` from `0` to `2^n - 1`.** Each `mask` is one switch pattern.
3. **Build the subset for this `mask`.**
   - Start with an empty `subset`.
   - For every position `j` from `0` to `n - 1`, check if switch `j` is ON.
   - If ON, add `nums[j]` to `subset`.
4. **Add `subset` to `result`.**
5. **Return `result`** after all masks are done.

> We check the **switch (bit)**, never the **value**. That is why `nums = [0]` still works: the value `0` gets picked because its switch is ON.

> Memory hook: <mark>"Count from 0 to 2^n - 1. Every 1 bit means take that number."</mark>

### Solution

```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        result = []
        for mask in range(1 << n):
            subset = []
            for j in range(n):
                if mask & (1 << j):
                    subset.append(nums[j])
            result.append(subset)
        return result
```

### Dry Run

```ini
=====================================================
SCENARIO A: nums = [1,2,3]
=====================================================

Setup:
  n      = 3
  result = []
  Total masks = 1 << 3 = 8, so mask goes from 0 to 7.

  Switch testers (only one switch ON in each):
    j = 0  →  1 << 0 = 1 = 001  (switch for nums[0] = 1)
    j = 1  →  1 << 1 = 2 = 010  (switch for nums[1] = 2)
    j = 2  →  1 << 2 = 4 = 100  (switch for nums[2] = 3)

Iteration 1: mask = 0 (binary 000)
  subset = []
  j = 0: 000 & 001 = 000 → zero, switch OFF. Skip nums[0] = 1.
  j = 1: 000 & 010 = 000 → zero, switch OFF. Skip nums[1] = 2.
  j = 2: 000 & 100 = 000 → zero, switch OFF. Skip nums[2] = 3.
  subset = []
  result = [[]]

Iteration 2: mask = 1 (binary 001)
  subset = []
  j = 0: 001 & 001 = 001 → not zero, switch ON. Take nums[0] = 1. subset = [1]
  j = 1: 001 & 010 = 000 → zero, switch OFF. Skip nums[1] = 2.
  j = 2: 001 & 100 = 000 → zero, switch OFF. Skip nums[2] = 3.
  subset = [1]
  result = [[], [1]]

Iteration 3: mask = 2 (binary 010)
  subset = []
  j = 0: 010 & 001 = 000 → zero, switch OFF. Skip nums[0] = 1.
  j = 1: 010 & 010 = 010 → not zero, switch ON. Take nums[1] = 2. subset = [2]
  j = 2: 010 & 100 = 000 → zero, switch OFF. Skip nums[2] = 3.
  subset = [2]
  result = [[], [1], [2]]

Iteration 4: mask = 3 (binary 011)
  subset = []
  j = 0: 011 & 001 = 001 → not zero, switch ON. Take nums[0] = 1. subset = [1]
  j = 1: 011 & 010 = 010 → not zero, switch ON. Take nums[1] = 2. subset = [1, 2]
  j = 2: 011 & 100 = 000 → zero, switch OFF. Skip nums[2] = 3.
  subset = [1, 2]
  result = [[], [1], [2], [1, 2]]

Iteration 5: mask = 4 (binary 100)
  subset = []
  j = 0: 100 & 001 = 000 → zero, switch OFF. Skip nums[0] = 1.
  j = 1: 100 & 010 = 000 → zero, switch OFF. Skip nums[1] = 2.
  j = 2: 100 & 100 = 100 → not zero, switch ON. Take nums[2] = 3. subset = [3]
  subset = [3]
  result = [[], [1], [2], [1, 2], [3]]

Iteration 6: mask = 5 (binary 101)
  subset = []
  j = 0: 101 & 001 = 001 → not zero, switch ON. Take nums[0] = 1. subset = [1]
  j = 1: 101 & 010 = 000 → zero, switch OFF. Skip nums[1] = 2.
  j = 2: 101 & 100 = 100 → not zero, switch ON. Take nums[2] = 3. subset = [1, 3]
  subset = [1, 3]
  result = [[], [1], [2], [1, 2], [3], [1, 3]]

Iteration 7: mask = 6 (binary 110)
  subset = []
  j = 0: 110 & 001 = 000 → zero, switch OFF. Skip nums[0] = 1.
  j = 1: 110 & 010 = 010 → not zero, switch ON. Take nums[1] = 2. subset = [2]
  j = 2: 110 & 100 = 100 → not zero, switch ON. Take nums[2] = 3. subset = [2, 3]
  subset = [2, 3]
  result = [[], [1], [2], [1, 2], [3], [1, 3], [2, 3]]

Iteration 8: mask = 7 (binary 111)
  subset = []
  j = 0: 111 & 001 = 001 → not zero, switch ON. Take nums[0] = 1. subset = [1]
  j = 1: 111 & 010 = 010 → not zero, switch ON. Take nums[1] = 2. subset = [1, 2]
  j = 2: 111 & 100 = 100 → not zero, switch ON. Take nums[2] = 3. subset = [1, 2, 3]
  subset = [1, 2, 3]
  result = [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]

Loop finished. mask = 8 is not less than 8, so we stop.

Every pattern from 000 to 111 was used exactly once, so no subset repeats.
Return result
Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]  ✓


=====================================================
SCENARIO B: nums = [0]  (the value itself is zero)
=====================================================

Setup:
  n      = 1
  result = []
  Total masks = 1 << 1 = 2, so mask goes from 0 to 1.

  Switch tester:
    j = 0  →  1 << 0 = 1 = binary 1  (switch for nums[0] = 0)

Iteration 1: mask = 0 (binary 0)
  subset = []
  j = 0: 0 & 1 = 0 → zero, switch OFF. Skip nums[0] = 0.
  subset = []
  result = [[]]

Iteration 2: mask = 1 (binary 1)
  subset = []
  j = 0: 1 & 1 = 1 → not zero, switch ON. Take nums[0] = 0. subset = [0]
  subset = [0]
  result = [[], [0]]

Loop finished. mask = 2 is not less than 2, so we stop.

Note: We tested the SWITCH (bit), not the VALUE.
The value 0 was still taken because its switch was ON.

Return result
Output: [[],[0]]  ✓
```

### Complexity Analysis

- **Time Complexity:** `O(N × 2^N)`.
  - The outer loop runs `2^N` times (one per mask).
  - The inner loop checks all `N` switches for every mask.
- **Space Complexity:** `O(N × 2^N)`.
  - Again, this is the size of the answer.
  - Apart from the answer, only `mask`, `j`, and one `subset` at a time are used, so the extra space is `O(N)`.

<br><br>

## Which One to Pick?

- **Approach 1** is the easiest to picture and explain: "the list doubles with every element."
- **Approach 2** is a classic bit trick. Interviewers like it, and it shows up again in many bitmask problems.
- Both do the same amount of work, so pick the one you can explain most clearly.

> With `N <= 10`, the answer has at most `2^10 = 1024` subsets, so both approaches run instantly.

<br><br>

## Related Problems

- [Letter Combinations of a Phone Number (17)](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)
- [Combination Sum (39)](https://leetcode.com/problems/combination-sum/)
- [Permutations (46)](https://leetcode.com/problems/permutations/)
- [Combinations (77)](https://leetcode.com/problems/combinations/)
- [Subsets II (90)](https://leetcode.com/problems/subsets-ii/)
- [Generalized Abbreviation (320)](https://leetcode.com/problems/generalized-abbreviation/)
- [Letter Case Permutation (784)](https://leetcode.com/problems/letter-case-permutation/)
- [Sum of All Subset XOR Totals (1863)](https://leetcode.com/problems/sum-of-all-subset-xor-totals/)
- [Count Number of Maximum Bitwise-OR Subsets (2044)](https://leetcode.com/problems/count-number-of-maximum-bitwise-or-subsets/)
