# Zig Zag Sequence

`HackerRank`

## Problem Statement

Given an array of `n` **distinct** integers, transform the array into a **zig zag sequence** by permuting the array elements.

A sequence is called a zig zag sequence if the **first `k` elements** are in **increasing** order and the **last `k` elements** are in **decreasing** order, where `k = (n + 1) / 2`.

You need to find the **lexicographically smallest** zig zag sequence of the given array.

## Examples

**Example 1:**

```ini
Input: a = [2,3,5,1,4]
Output: [1,2,5,4,3]
Explanation: n = 5, so k = 3. The first 3 elements (1, 2, 5) go up, and the last 3 elements (5, 4, 3) go down.
[1,4,5,3,2] is also a zig zag sequence, but [1,2,5,4,3] is smaller because at index 1, 2 < 4.
```

**Example 2:**

```ini
Input: a = [1,2,3,4,5,6,7]
Output: [1,2,3,7,6,5,4]
Explanation: n = 7, so k = 4. The first 4 elements (1, 2, 3, 7) go up, and the last 4 elements (7, 6, 5, 4) go down.
```

## Constraints

- `1 <= n <= 10^4`
- `n` is always **odd**.
- `1 <= a[i] <= 10^9`
- All elements of `a` are **distinct**.

<br><br>

## Approach

### The One Rule to Remember

A zig zag sequence is a <mark>mountain: climb up, reach the top, walk down</mark>.

```ini
                7
             3     6
          2           5
       1                 4
```

- The middle spot (the **summit**) belongs to both the climb and the walk down, so it must hold the **biggest** number.
- "Lexicographically smallest" means the **leftmost** spots matter most. So the left side gets the **smallest** numbers, going up.
- Whatever is left goes on the right side, going **down**.

### The Trick

Sort the array and compare it with the answer:

```ini
Sorted:  [1, 2, 3, 4, 5, 6, 7]
Answer:  [1, 2, 3, 7, 6, 5, 4]
```

The left half is already done. The right half just needs to be **flipped**.

### Step by Step

1. **Sort** the array.
2. **Find the summit:** `mid = n // 2`.
3. **Swap** `a[mid]` with the last element.
   - The biggest number moves to the summit.
   - The old middle number (the smallest of the right side) moves to the end, which is already its final spot.
4. **Reverse** the part between them (`mid + 1` to `n - 2`), using two pointers that move toward each other.

> Memory hook: <mark>"Sort it. Send the king to the summit. Flip what is in between."</mark>

<br><br>

## Solution

```python
def findZigZagSequence(a, n):
    a.sort()
    mid = n // 2
    a[mid], a[n - 1] = a[n - 1], a[mid]

    st = mid + 1
    ed = n - 2
    while st <= ed:
        a[st], a[ed] = a[ed], a[st]
        st = st + 1
        ed = ed - 1

    return a
```

<br><br>

## Dry Run

```ini
=====================================================
SCENARIO A: a = [2,3,5,1,4], n = 5
=====================================================

Step 1: Sort the array.
  Before: [2, 3, 5, 1, 4]
  After:  [1, 2, 3, 4, 5]

  Index:   0  1  2  3  4
  Value:   1  2  3  4  5

Step 2: Find the summit index.
  mid = n // 2 = 5 // 2 = 2
  The summit is index 2 (currently holding 3).

Step 3: Swap the middle and the last element.
  a[mid] = a[2] = 3
  a[n-1] = a[4] = 5   (the biggest number)
  Swap them.

  Before: [1, 2, 3, 4, 5]
  After:  [1, 2, 5, 4, 3]

  5 is now on the summit.
  3 is now at the end. It is the smallest of the right side, so it belongs at the bottom.

Step 4: Set up the two pointers for the reverse.
  st = mid + 1 = 2 + 1 = 3
  ed = n - 2   = 5 - 2 = 3
  The part to flip is index 3 to index 3 (just one element: 4).

Iteration 1:
  Loop check: is st (3) <= ed (3)? YES. Enter loop.
  Swap a[3] and a[3]: the element swaps with itself. Nothing changes.
  Array: [1, 2, 5, 4, 3]
  Move pointers: st = 3 + 1 = 4, ed = 3 - 1 = 2

Iteration 2:
  Loop check: is st (4) <= ed (2)? NO. Exit loop.

Final check:
  First k = 3 elements: 1 < 2 < 5   (going up)   ✓
  Last k = 3 elements:  5 > 4 > 3   (going down) ✓

Return [1, 2, 5, 4, 3]
Output: [1,2,5,4,3]  ✓


=====================================================
SCENARIO B: a = [1,2,3,4,5,6,7], n = 7
=====================================================

Step 1: Sort the array.
  Before: [1, 2, 3, 4, 5, 6, 7]
  After:  [1, 2, 3, 4, 5, 6, 7]   (already sorted, no change)

  Index:   0  1  2  3  4  5  6
  Value:   1  2  3  4  5  6  7

Step 2: Find the summit index.
  mid = n // 2 = 7 // 2 = 3
  The summit is index 3 (currently holding 4).

Step 3: Swap the middle and the last element.
  a[mid] = a[3] = 4
  a[n-1] = a[6] = 7   (the biggest number)
  Swap them.

  Before: [1, 2, 3, 4, 5, 6, 7]
  After:  [1, 2, 3, 7, 5, 6, 4]

  7 is now on the summit.
  4 is now at the end. It is the smallest of the right side, so it belongs at the bottom.
  But the middle part (5, 6) is still going UP. It must be flipped.

Step 4: Set up the two pointers for the reverse.
  st = mid + 1 = 3 + 1 = 4
  ed = n - 2   = 7 - 2 = 5
  The part to flip is index 4 to index 5 (values 5 and 6).

Iteration 1:
  Loop check: is st (4) <= ed (5)? YES. Enter loop.
  Swap a[4] = 5 and a[5] = 6.
  Before: [1, 2, 3, 7, 5, 6, 4]
  After:  [1, 2, 3, 7, 6, 5, 4]
  Move pointers: st = 4 + 1 = 5, ed = 5 - 1 = 4

Iteration 2:
  Loop check: is st (5) <= ed (4)? NO. The pointers crossed. Exit loop.

Final check:
  First k = 4 elements: 1 < 2 < 3 < 7   (going up)   ✓
  Last k = 4 elements:  7 > 6 > 5 > 4   (going down) ✓

Return [1, 2, 3, 7, 6, 5, 4]
Output: [1,2,3,7,6,5,4]  ✓


=====================================================
SCENARIO C: a = [9,1,8,2,7,3,6,4,5], n = 9  (longer flip)
=====================================================

Step 1: Sort the array.
  Before: [9, 1, 8, 2, 7, 3, 6, 4, 5]
  After:  [1, 2, 3, 4, 5, 6, 7, 8, 9]

  Index:   0  1  2  3  4  5  6  7  8
  Value:   1  2  3  4  5  6  7  8  9

Step 2: Find the summit index.
  mid = n // 2 = 9 // 2 = 4
  The summit is index 4 (currently holding 5).

Step 3: Swap the middle and the last element.
  a[mid] = a[4] = 5
  a[n-1] = a[8] = 9   (the biggest number)
  Swap them.

  Before: [1, 2, 3, 4, 5, 6, 7, 8, 9]
  After:  [1, 2, 3, 4, 9, 6, 7, 8, 5]

  9 is now on the summit.
  5 is now at the end, in its final place.
  The middle part (6, 7, 8) is still going UP. It must be flipped.

Step 4: Set up the two pointers for the reverse.
  st = mid + 1 = 4 + 1 = 5
  ed = n - 2   = 9 - 2 = 7
  The part to flip is index 5 to index 7 (values 6, 7, 8).

Iteration 1:
  Loop check: is st (5) <= ed (7)? YES. Enter loop.
  Swap a[5] = 6 and a[7] = 8.
  Before: [1, 2, 3, 4, 9, 6, 7, 8, 5]
  After:  [1, 2, 3, 4, 9, 8, 7, 6, 5]
  Move pointers: st = 5 + 1 = 6, ed = 7 - 1 = 6

Iteration 2:
  Loop check: is st (6) <= ed (6)? YES. Enter loop.
  Swap a[6] and a[6]: the element swaps with itself. Nothing changes.
  Array: [1, 2, 3, 4, 9, 8, 7, 6, 5]
  Move pointers: st = 6 + 1 = 7, ed = 6 - 1 = 5

Iteration 3:
  Loop check: is st (7) <= ed (5)? NO. The pointers crossed. Exit loop.

Final check:
  First k = 5 elements: 1 < 2 < 3 < 4 < 9   (going up)   ✓
  Last k = 5 elements:  9 > 8 > 7 > 6 > 5   (going down) ✓

Return [1, 2, 3, 4, 9, 8, 7, 6, 5]
Output: [1,2,3,4,9,8,7,6,5]  ✓


=====================================================
SCENARIO D: a = [42], n = 1  (single element)
=====================================================

Step 1: Sort the array.
  [42] stays [42].

Step 2: Find the summit index.
  mid = n // 2 = 1 // 2 = 0
  The summit is index 0. It is also the first and the last element.

Step 3: Swap the middle and the last element.
  a[0] swaps with a[0]: the element swaps with itself. Nothing changes.
  Array: [42]

Step 4: Set up the two pointers for the reverse.
  st = mid + 1 = 0 + 1 = 1
  ed = n - 2   = 1 - 2 = -1

Iteration 1:
  Loop check: is st (1) <= ed (-1)? NO. The loop never runs.

Final check:
  A single number is both the climb and the walk down. ✓

Return [42]
Output: [42]  ✓
```

<br><br>

## Complexity Analysis

- **Time Complexity:** `O(N log N)`, where `N` is the length of the array.
  - Sorting takes `O(N log N)`.
  - The swap is `O(1)`.
  - The reverse loop touches about half of the right side, which is `O(N)`.
  - Sorting is the biggest cost, so the total is `O(N log N)`.
- **Space Complexity:** `O(1)` extra.
  - Everything happens inside the same array.
  - Only a few variables (`mid`, `st`, `ed`) are used.
  - Note: Python's built in sort may use up to `O(N)` temporary memory internally.

<br><br>

## Related Problems

- [Next Permutation (31)](https://leetcode.com/problems/next-permutation/)
- [Rotate Array (189)](https://leetcode.com/problems/rotate-array/)
- [Wiggle Sort (280)](https://leetcode.com/problems/wiggle-sort/)
- [Wiggle Sort II (324)](https://leetcode.com/problems/wiggle-sort-ii/)
- [Reverse String (344)](https://leetcode.com/problems/reverse-string/)
- [Longest Mountain in Array (845)](https://leetcode.com/problems/longest-mountain-in-array/)
- [Peak Index in a Mountain Array (852)](https://leetcode.com/problems/peak-index-in-a-mountain-array/)
- [Valid Mountain Array (941)](https://leetcode.com/problems/valid-mountain-array/)
- [Find in Mountain Array (1095)](https://leetcode.com/problems/find-in-mountain-array/)
- [Minimum Number of Removals to Make Mountain Array (1671)](https://leetcode.com/problems/minimum-number-of-removals-to-make-mountain-array/)
