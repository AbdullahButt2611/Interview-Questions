# Moore's Voting Algorithm

A single-pass, constant-space technique for finding the element that appears more than half the time, by letting differing elements cancel each other out until only the dominant one survives. Also known as the Boyer-Moore Voting Algorithm.

## What It Is

You have a list of items where one item appears **more than half** the time (strictly more than half, not exactly half). That item is the **majority element**, and the task is to find it.

```
Input:   [2, 2, 1, 1, 1, 2, 2]
Output:  2          # 2 appears 4 times out of 7, and 4 > 3.5
```

The obvious approach counts how often each item appears in a hash map, then picks the largest. That works in `O(n)` time but costs `O(n)` space to hold the counts. Moore's algorithm gets the same answer in a single pass using only two variables, so the win is memory: `O(1)` instead of `O(n)`.

## Core Idea

Picture every item as a soldier carrying a colored flag, where same item means same color. Whenever two soldiers of different colors meet, both fall and leave the field (a one-for-one knockout). Soldiers of the same color never fight. If one color is more than half the army, the others combined are fewer than half, so they run out of soldiers before they can wipe that color out. At least one soldier of the majority color is always left standing.

In code this becomes two variables: `candidate` (who is currently standing) and `count` (a net tug-of-war score). When `count` hits `0`, the throne is empty and the next item claims it. A matching item reinforces (`count + 1`), a differing item knocks one off (`count - 1`).

The invariant that makes it correct: a strict majority appears more times than every other element added together, so the others can never drive its score permanently to zero. Note that `count` is a net balance, **not** the true frequency of the candidate.

<br>

## The Verification Caveat

The algorithm does not answer "is there a majority?". It answers "**if** a majority exists, this is the only value it could be." When a majority is **not** guaranteed, you must add a second pass to confirm the candidate actually clears the bar, and the comparison must be strict (`>`, not `>=`), because `n/2` exact occurrences is not a majority.

## When To Reach For It

- You need the element appearing more than `n/2` of the time (or more than `n/k` for the generalizations)
- You need `O(1)` extra space, or a single sweep, or a streaming solution where you cannot store every value
- The wording hints at a "dominant" or "more than half" element
- More generally, "which few items are heavy hitters using tiny memory"

<br>

## Template Code (Python)

The safe version, with verification, so it works even when a majority is not guaranteed:

```python
def majority_element(nums):
    candidate, count = None, 0

    # Pass 1: find the only possible candidate
    for x in nums:
        if count == 0:
            candidate, count = x, 1
        elif x == candidate:
            count += 1
        else:
            count -= 1

    # Pass 2: verify it really is a majority
    if nums.count(candidate) > len(nums) // 2:
        return candidate
    return None
```

If the problem guarantees a majority exists (for example LeetCode 169), you can drop Pass 2 and `return candidate` directly.

## Step-by-Step Walkthrough

Tracing `[2, 2, 1, 1, 1, 2, 2]`, watching the throne change hands:

| Element | Action | candidate | count |
|---|---|---|---|
| `2` | count is 0, claim throne | `2` | 1 |
| `2` | matches, reinforce | `2` | 2 |
| `1` | differs, knockout | `2` | 1 |
| `1` | differs, knockout | `2` | 0 |
| `1` | count is 0, claim throne | `1` | 1 |
| `2` | differs, knockout | `1` | 0 |
| `2` | count is 0, claim throne | `2` | 1 |

The throne flips from `2` to `1` and back to `2`. The candidate is only trustworthy after the full pass, never mid-loop.

## Complexity

| Approach | Time | Space |
|---|---|---|
| Boyer-Moore voting (single pass) | `O(n)` | `O(1)` |
| Boyer-Moore with verification (two passes) | `O(n)` | `O(1)` |
| Count frequencies in a map | `O(n)` | `O(n)` |

One loop visits each of `n` items with constant work per item, giving `O(n)`. Two passes is still `2n`, which is `O(n)`. Only two scalar variables are kept, so the extra space is `O(1)`.

<br>

## Variations

The real shape of the problem is "which elements appear more than a `1/k` fraction of the time". A counting fact drives every variation: at most `k - 1` elements can each appear more than `n/k` times, since `k` of them would sum past `n`.

### More than n/3 (two candidates)

Keep two thrones and two scores. A miss against both knocks both down at once. At most two such elements can exist (LeetCode 229).

```python
def majority_n3(nums):
    cand1, cand2 = None, None
    count1, count2 = 0, 0

    for x in nums:
        if cand1 is not None and x == cand1:
            count1 += 1
        elif cand2 is not None and x == cand2:
            count2 += 1
        elif count1 == 0:
            cand1, count1 = x, 1
        elif count2 == 0:
            cand2, count2 = x, 1
        else:
            count1 -= 1
            count2 -= 1

    return [c for c in (cand1, cand2)
            if c is not None and nums.count(c) > len(nums) // 3]
```

The branch order is critical: check "does `x` match an existing throne?" **before** "is a throne empty?". Reverse them and a value equal to `cand1` can wrongly grab the empty second throne, putting the same value on both. Verification is mandatory here, since no element is promised to clear the `n/3` bar.

<br>

### More than n/k (Misra-Gries)

The same structure scales. Maintain up to `k - 1` candidate-count pairs. For each item, reinforce its throne if present, seat it on a free throne if one exists, otherwise decrement every throne by one and evict any that reach zero. A second pass verifies the true counts. This is the Misra-Gries algorithm, and Moore's vote is its `k = 2` instance.

<br>

### Streaming / heavy hitters

When the input is a stream you see once and cannot re-scan, the single pass alone gives a useful but partial guarantee. The surviving candidates are a **superset** of the true frequent items, so there are no false negatives, but there can be false positives. Exactness needs the verification pass, which is exactly what you cannot do on a true one-pass stream.

<br>

## Variations at a Glance

| Variation | Best For | Time |
|---|---|---|
| Boyer-Moore (n/2) | One element appearing more than half the time | `O(n)` |
| Two-candidate (n/3) | All elements appearing more than a third of the time | `O(n)` |
| Misra-Gries (n/k) | All elements appearing more than a `1/k` fraction | `O(n*k)` |
| Streaming single pass | Approximate heavy hitters with tiny memory | `O(n*k)` |

<br>

## Common Pitfalls

- Skipping the verification pass when a majority is not guaranteed. The survivor may just be the least-cancelled value without truly exceeding the threshold.
- Using `>=` instead of `>` in verification. Majority is *strictly* more than `n/2`, so exactly `n/2` occurrences must fail.
- Wrong branch order in the `n/3` version. Reinforce-before-seat is mandatory. Test `[1, 1]`: the buggy order seats `1` on both thrones.
- Reading `count` as a frequency. It is a net tug-of-war score, so the candidate can end with a count far below its real number of appearances.
- Trusting the candidate mid-pass. The throne can change hands several times, so only the value after the full pass is meaningful.

<br>

## Practice Problems (LeetCode)

Recognizing "this is a dominant-element problem" is the key step. No solutions here, just the list, ordered Easy to Hard.

### Easy

- Majority Element (LeetCode 169)

### Medium

- Majority Element II (LeetCode 229)