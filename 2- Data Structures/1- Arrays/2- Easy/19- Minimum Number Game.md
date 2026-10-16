# Minimum Number Game

`Amazon` • `Google` • `Microsoft` • `Meta` • `Bloomberg` • `BT Group` • `Educative`

<br>

## Problem Statement

You are given a **0-indexed** integer array `nums` of **even** length and there is also an empty array `arr`. Alice and Bob decided to play a game where in every round Alice and Bob will do one move. The rules of the game are as follows:

- Every round, first Alice will remove the **minimum** element from `nums`, and then Bob does the same.
- Now, first Bob will append the removed element in the array `arr`, and then Alice does the same.
- The game continues until `nums` becomes empty.

Return _the resulting array_ `arr`.

## Examples

**Example 1:**

```ini
Input: nums = [5,4,2,3]
Output: [3,2,5,4]
Explanation: In round one, first Alice removes 2 and then Bob removes 3. Then in arr firstly Bob appends 3 and then Alice appends 2. So arr = [3,2].
At the beginning of round two, nums = [5,4]. Now, first Alice removes 4 and then Bob removes 5. Then both append in arr which becomes [3,2,5,4].
```

**Example 2:**

```ini
Input: nums = [2,5]
Output: [5,2]
Explanation: In round one, first Alice removes 2 and then Bob removes 5. Then in arr firstly Bob appends and then Alice appends. So arr = [5,2].
```

## Constraints

- `2 <= nums.length <= 100`
- `1 <= nums[i] <= 100`
- `nums.length % 2 == 0`

<br><br>

## Key Observation

Let's think about what actually happens in each round:

- Alice always takes the **smallest** number left.
- Bob then takes the **next smallest** number left.
- But when adding to `arr`, **Bob goes first**, then Alice.

So in every round, the two smallest numbers get added to `arr` in **reversed order** (bigger one first, smaller one second).

If we **sort** `nums` first, the smallest numbers are always sitting right at the front, in pairs:

- Pair 1 = `nums[0]`, `nums[1]`
- Pair 2 = `nums[2]`, `nums[3]`
- and so on...

<mark>The whole game is just: sort the array, then flip every pair of neighbours.</mark>

All three approaches below use this idea. They only differ in **how** they flip the pairs.

<br><br>

## Approach 1: Sort + Slice Off Pairs (Direct Simulation)

### Idea

This approach copies the game almost word for word:

- Sort `nums` so the smallest numbers are at the front.
- Create an empty list `arr`.
- While `nums` still has numbers in it:
  - Take the first two numbers. The first one is Alice's pick, the second one is Bob's pick.
  - Remove those two numbers from `nums` by keeping only the part after them (`nums[2:]`).
  - Add Bob's number to `arr`, then add Alice's number.
- When `nums` is empty, return `arr`.

### Code

```python
class Solution:
    def numberGame(self, nums: List[int]) -> List[int]:
        nums.sort()
        arr = []
        while nums:
            alice, bob = nums[:2]
            nums = nums[2:]
            arr.append(bob)
            arr.append(alice)
        return arr
```

### Dry Run

```ini
Input: nums = [5, 4, 2, 3]

Step 0: Sort nums
  Before sorting : nums = [5, 4, 2, 3]
  After sorting  : nums = [2, 3, 4, 5]
  arr = []

Iteration 1:
  Check: nums = [2, 3, 4, 5] is not empty, so the loop runs
  alice, bob = nums[:2]   ->  nums[:2] = [2, 3]
                              alice = 2 (smallest)
                              bob   = 3 (next smallest)
  nums = nums[2:]         ->  a NEW list is built from index 2 onwards
                              nums = [4, 5]
  arr.append(bob)         ->  Bob adds first   ->  arr = [3]
  arr.append(alice)       ->  Alice adds next  ->  arr = [3, 2]

Iteration 2:
  Check: nums = [4, 5] is not empty, so the loop runs
  alice, bob = nums[:2]   ->  nums[:2] = [4, 5]
                              alice = 4
                              bob   = 5
  nums = nums[2:]         ->  a NEW list is built from index 2 onwards
                              nums = []
  arr.append(bob)         ->  arr = [3, 2, 5]
  arr.append(alice)       ->  arr = [3, 2, 5, 4]

Loop Check:
  nums = [] is empty, so the loop stops

Final Answer: arr = [3, 2, 5, 4]
```

### Complexity

- **Time:** `O(n log n)` for sorting, plus `O(n²)` in total for the slicing (explained below).
- **Space:** `O(n)` for the `arr` list, plus the temporary lists created by slicing.

### What Is the Issue With This Approach?

- The line `nums = nums[2:]` looks harmless, but it is **not free**.
- Every time it runs, Python builds a **brand new list** and copies every remaining element into it.
- With `n` numbers:
  - Round 1 copies `n - 2` numbers
  - Round 2 copies `n - 4` numbers
  - Round 3 copies `n - 6` numbers, and so on
- Adding all of that up gives roughly `n² / 4` copies, which is <mark>O(n²) of wasted work</mark>.
- We never actually needed to remove anything. We only needed to **read** the numbers two at a time.

So the fix is simple: instead of chopping the list, just **walk through it** using an index.

<br><br>

## Approach 2: Sort + Step Through Pairs With an Index

### Idea

Same plan as before, but we stop shrinking the list:

- Sort `nums`.
- Create an empty list `arr`.
- Use an index `i` that starts at `0` and jumps by `2` each time (`0, 2, 4, ...`).
  - `nums[i]` is Alice's number (the smaller one of the pair).
  - `nums[i + 1]` is Bob's number (the bigger one of the pair).
  - Add `nums[i + 1]` to `arr` first (Bob), then `nums[i]` (Alice).
- Return `arr`.

Since the length is always even, `i + 1` never goes out of bounds.

### Code

```python
class Solution:
    def numberGame(self, nums: List[int]) -> List[int]:
        nums.sort()
        arr = []

        for i in range(0, len(nums), 2):
            arr.append(nums[i + 1])
            arr.append(nums[i])

        return arr
```

### Dry Run

```ini
Input: nums = [5, 4, 2, 3]

Step 0: Sort nums
  Before sorting : nums = [5, 4, 2, 3]
  After sorting  : nums = [2, 3, 4, 5]
                   index:  0  1  2  3
  arr = []
  range(0, 4, 2) gives i = 0, then i = 2

Iteration 1 (i = 0):
  Pair we are looking at  ->  nums[0] = 2, nums[1] = 3
  arr.append(nums[i + 1]) ->  nums[1] = 3 (Bob)    ->  arr = [3]
  arr.append(nums[i])     ->  nums[0] = 2 (Alice)  ->  arr = [3, 2]
  nums is NOT changed     ->  nums = [2, 3, 4, 5]

Iteration 2 (i = 2):
  Pair we are looking at  ->  nums[2] = 4, nums[3] = 5
  arr.append(nums[i + 1]) ->  nums[3] = 5 (Bob)    ->  arr = [3, 2, 5]
  arr.append(nums[i])     ->  nums[2] = 4 (Alice)  ->  arr = [3, 2, 5, 4]
  nums is NOT changed     ->  nums = [2, 3, 4, 5]

Loop Check:
  Next i would be 4, but 4 is not less than len(nums) = 4, so the loop stops

Final Answer: arr = [3, 2, 5, 4]
```

### Complexity

- **Time:** `O(n log n)` for sorting. The loop itself is only `O(n)`.
- **Space:** `O(n)` for the separate `arr` list.

### What Is the Issue With This Approach?

- The `O(n²)` slicing problem is gone. This is already a good solution.
- But look closely: `arr` ends up holding **exactly the same numbers** as the sorted `nums`, just with each pair flipped.
- So we are building a whole second list when the first one is already sitting right there.
- Since the problem lets us change `nums`, <mark>we can flip the pairs directly inside nums</mark> and skip the extra list completely.

<br><br>

## Approach 3: Sort + Swap Neighbours In Place (Optimal)

### Idea

- Sort `nums`.
- Use an index `i` that jumps by `2` (`0, 2, 4, ...`).
- At every step, **swap** `nums[i]` and `nums[i + 1]`.
  - Before the swap: smaller number first (Alice's order).
  - After the swap: bigger number first (Bob's order, which is what `arr` needs).
- Return `nums` itself. It now looks exactly like `arr` would.

In Python, `a, b = b, a` swaps two values in one line, no temporary variable needed.

### Code

```python
class Solution:
    def numberGame(self, nums: List[int]) -> List[int]:
        nums.sort()
        for i in range(0, len(nums), 2):
            nums[i], nums[i + 1] = nums[i + 1], nums[i]
        return nums
```

### Dry Run

```ini
Input: nums = [5, 4, 2, 3]

Step 0: Sort nums
  Before sorting : nums = [5, 4, 2, 3]
  After sorting  : nums = [2, 3, 4, 5]
                   index:  0  1  2  3
  No extra list is created
  range(0, 4, 2) gives i = 0, then i = 2

Iteration 1 (i = 0):
  Values before swap  ->  nums[0] = 2, nums[1] = 3
  Swap them           ->  nums[0] becomes 3, nums[1] becomes 2
  nums now            ->  [3, 2, 4, 5]
                           ^^^^
                           first pair flipped

Iteration 2 (i = 2):
  Values before swap  ->  nums[2] = 4, nums[3] = 5
  Swap them           ->  nums[2] becomes 5, nums[3] becomes 4
  nums now            ->  [3, 2, 5, 4]
                                 ^^^^
                                 second pair flipped

Loop Check:
  Next i would be 4, but 4 is not less than len(nums) = 4, so the loop stops

Final Answer: nums = [3, 2, 5, 4]
```

### Complexity

- **Time:** `O(n log n)` for sorting. The swapping loop is `O(n)`.
- **Space:** `O(1)` extra space, because we reuse `nums` instead of building a new list (ignoring the memory Python's sort uses internally).

### Why This Is the Best One

- No slicing, so no hidden `O(n²)` copying (fixes Approach 1).
- No second list, so no extra `O(n)` memory (improves on Approach 2).
- It is also the shortest and cleanest code of the three.

<br><br>

## Quick Comparison

- **Approach 1 (Slice Off Pairs)**
  - Time: `O(n²)` because of repeated slicing
  - Extra Space: `O(n)`
  - Easiest to read, since it mirrors the story exactly
- **Approach 2 (Index Stepping)**
  - Time: `O(n log n)`
  - Extra Space: `O(n)` for `arr`
  - Fixes the slicing problem
- **Approach 3 (In-Place Swap)**
  - Time: `O(n log n)`
  - Extra Space: `O(1)`
  - <mark>Best choice for interviews</mark>

<br><br>

## Related Problems

- [Min Max Game (2293)](https://leetcode.com/problems/min-max-game/)
- [Array Partition (561)](https://leetcode.com/problems/array-partition/)
- [Swap Nodes in Pairs (24)](https://leetcode.com/problems/swap-nodes-in-pairs/)
- [Sort Array By Parity II (922)](https://leetcode.com/problems/sort-array-by-parity-ii/)
- [Rearrange Array Elements by Sign (2149)](https://leetcode.com/problems/rearrange-array-elements-by-sign/)
- [Last Stone Weight (1046)](https://leetcode.com/problems/last-stone-weight/)
- [Wiggle Sort (280)](https://leetcode.com/problems/wiggle-sort/)
