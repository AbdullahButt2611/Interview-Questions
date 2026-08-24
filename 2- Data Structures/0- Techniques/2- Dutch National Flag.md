# Dutch National Flag

A technique for sorting an array of three distinct values in a single in-place pass, by growing a low region and a high region inward until the unsorted middle vanishes.

## What It Is

The Dutch flag has three colored bands in a fixed order: red, white, blue. Picture a bag of mixed red, white, and blue balls that you must lay out in that exact order. In code we swap the colors for numbers, `0`, `1`, `2`, so the task becomes: given a messy array of `0`s, `1`s, and `2`s, sort it.

```
Input:   [2, 0, 2, 1, 1, 0]
Output:  [0, 0, 1, 1, 2, 2]
```

You could solve this by counting how many of each value exist, then overwriting the array. That works and is `O(n)`, but it makes two passes. Dutch National Flag does the same job in a single pass with in-place swaps, and that single-pass property is the entire reason the technique is worth knowing.

## Core Idea

Keep three pointers and four facts that stay true on every step (the invariants). Everything left of `low` is a finished `0`, everything right of `high` is a finished `2`, the settled `1`s sit between `low` and `mid`, and the stretch from `mid` to `high` is the unknown region still being scanned.

```
[ 0 0 0 | 1 1 | ? ? ? ? | 2 2 2 ]
         ^low   ^mid       ^high+1
  reds    whites  unknown    blues
```

- `arr[0 .. low-1]` are all `0`
- `arr[low .. mid-1]` are all `1`
- `arr[mid .. high]` are unknown (still to inspect)
- `arr[high+1 .. end]` are all `2`

`mid` scans forward. A `0` gets swapped down to the `low` boundary, a `2` gets swapped out to the `high` boundary, and a `1` stays where it is. When `mid` passes `high`, the unknown region is empty and the array is sorted.

<br>

## The Critical Rule: When mid Moves and When It Doesn't

This is the one detail almost everyone gets wrong, and it is an asymmetry:

- On a `0`, swap with `low` and **advance `mid`**.
- On a `2`, swap with `high` and **do not advance `mid`**.

The reason is a single question: after the swap, do we already know the value that landed back at `mid`? On a `0` swap, the value pulled from `low` is guaranteed to be a `1` (the region `low .. mid-1` holds only `1`s), so it is already classified and `mid` can move on. On a `2` swap, the value pulled from `high` comes from the unknown region and has never been inspected, so `mid` must stay and re-examine it next loop.

Run `[1, 2, 0]` to see what breaks if you wrongly advance `mid` on the `2`:

```
correct (mid stays):  [1,2,0] -> [1,0,2] -> [0,1,2]   sorted
buggy   (mid moves):  [1,2,0] -> [1,0,2] -> stop       [1,0,2] wrong, the 0 is stranded
```

<br>

## When To Reach For It

- The values come from a small fixed set of three categories (colors, low/medium/high, negative/zero/positive)
- You need an in-place sort with no extra array
- You want a single pass rather than the two passes a counting approach takes
- More generally, any time you must partition around a pivot into three buckets: less than, equal to, greater than

Reach for counting sort instead when there are many distinct small values, and reach for a stable method when equal elements must keep their original order (see Common Pitfalls).

<br>

## Template Code (Python)

```python
def sort_colors(arr):
    low, mid = 0, 0
    high = len(arr) - 1

    while mid <= high:
        if arr[mid] == 0:
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] == 1:
            mid += 1
        else:  # arr[mid] == 2
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1
            # mid is NOT incremented here
    return arr
```

## Step-by-Step Walkthrough

Tracing `[2, 0, 2, 1, 1, 0]`, watching the unknown region squeeze shut:

| Element at mid | Action | Array | low | mid | high |
|---|---|---|---|---|---|
| start | | `[2,0,2,1,1,0]` | 0 | 0 | 5 |
| `2` | swap mid,high; high-- | `[0,0,2,1,1,2]` | 0 | 0 | 4 |
| `0` | swap low,mid; low++ mid++ | `[0,0,2,1,1,2]` | 1 | 1 | 4 |
| `0` | swap low,mid; low++ mid++ | `[0,0,2,1,1,2]` | 2 | 2 | 4 |
| `2` | swap mid,high; high-- | `[0,0,1,1,2,2]` | 2 | 2 | 3 |
| `1` | mid++ | `[0,0,1,1,2,2]` | 2 | 3 | 3 |
| `1` | mid++ | `[0,0,1,1,2,2]` | 2 | 4 | 3 |
| stop | mid > high | `[0,0,1,1,2,2]` | 2 | 4 | 3 |

## Complexity

| Approach | Time | Space |
|---|---|---|
| Dutch National Flag (single pass) | `O(n)` | `O(1)` |
| Counting then overwrite (two pass) | `O(n)` | `O(1)` |
| General library sort | `O(n log n)` | `O(n)` or `O(log n)` |

Every iteration either increases `mid` or decreases `high`, so the gap `high - mid` shrinks by at least one each loop and the work is bounded by `n`. That is the single pass, and the three integer pointers plus in-place swaps are the `O(1)` space.

<br>

## Variations

### Generalize the pivot (three-way partition)

Drop the `0/1/2` assumption and partition around any pivot value into less-than, equal-to, and greater-than regions. Dutch National Flag is just this with the pivot fixed at `1`.

```python
def three_way_partition(arr, pivot):
    low, mid = 0, 0
    high = len(arr) - 1
    while mid <= high:
        if arr[mid] < pivot:
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] > pivot:
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1
        else:  # equal to pivot
            mid += 1
    return arr
```

<br>

### Three-way quicksort (the real-world payoff)

Using three-way partition as the partition step of quicksort makes it dramatically faster on inputs with many repeated keys. All elements equal to the pivot land in the middle and are never touched again, so recursion only happens on the smaller and larger groups.

```python
def quicksort_3way(arr, lo=0, hi=None):
    if hi is None:
        hi = len(arr) - 1
    if lo >= hi:
        return arr
    pivot = arr[lo]
    lt, i, gt = lo, lo, hi
    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            i += 1
    quicksort_3way(arr, lo, lt - 1)
    quicksort_3way(arr, gt + 1, hi)
    return arr
```

On an input like `[5, 5, 5, ..., 5]`, classic two-way quicksort keeps re-partitioning equal elements and degrades toward `O(n^2)`. The three-way version groups all of them in one partition, leaving both recursive calls empty, so it finishes in `O(n)`.

<br>

### Two-way cousin

When there are only two categories (move all zeros to one side, separate even from odd), a single pair of pointers is enough. That is the same partitioning idea with one boundary instead of two.

<br>

## Variations at a Glance

| Variation | Best For | Time |
|---|---|---|
| Dutch National Flag | Sort an array of three fixed values in place | `O(n)` |
| Three-way partition | Split around a pivot into `<`, `=`, `>` | `O(n)` |
| Three-way quicksort | Sorting data with many duplicate keys | `O(n log n)`, near `O(n)` when duplicates dominate |
| Two-pointer partition | Two categories (move zeros, even/odd) | `O(n)` |

<br>

## Common Pitfalls

- Advancing `mid` after the `2` swap. The swapped-in value is unexamined, so this strands elements. Test `[1, 2, 0]`, which wrongly produces `[1, 0, 2]`.
- Using `mid < high` instead of `mid <= high`. When `mid == high` there is still one element to inspect. Test `[1, 0]`, which wrongly stays `[1, 0]`.
- Treating self-swaps as a problem. When `low == mid` the swap is a harmless no-op, though it can be guarded with `if low != mid` when writes are expensive.
- Assuming the result is stable. The swaps reorder equal elements, so this technique is not stable. If equal records must keep their original relative order, use a counting-based approach instead.

<br>

## Practice Problems (LeetCode)

Recognizing "this is a partitioning problem" is the key step in each of these. No solutions here, just the list to practice against, ordered Easy to Hard.

### Easy

- Move Zeroes (LeetCode 283)
- Sort Array By Parity (LeetCode 905)

### Medium

- Sort Colors (LeetCode 75)
- Partition Array According to Given Pivot (LeetCode 2161)
- Kth Largest Element in an Array (LeetCode 215)
- Sort an Array (LeetCode 912)
- Wiggle Sort II (LeetCode 324)