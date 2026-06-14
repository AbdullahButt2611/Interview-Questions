# Alternate Numbers

`Amazon` • `Microsoft` • `Paytm` • `VMware` • `Intuit`
<br>
## Problem Statement

Given an integer array `nums` containing both positive and negative numbers, rearrange the array so that positive and negative numbers appear alternately, starting with a positive number.

If the number of positive and negative elements is not the same, place the remaining elements of the larger group at the end of the array in their original order.

Return the rearranged array. The relative order of elements within each group (positives among themselves, negatives among themselves) must be preserved.

## Examples

### Example 1

**Input:** `nums = [1, 2, 3, -1, -2]`
**Output:** `[1, -1, 2, -2, 3]`

**Explanation:** The positive numbers in order are `[1, 2, 3]` and the negative numbers in order are `[-1, -2]`. Alternating one from each group gives `1, -1, 2, -2`. The negatives run out first, so the leftover positive `3` is appended at the end.

### Example 2

**Input:** `nums = [4, -1, 2, -7, 3, -5, 6]`
**Output:** `[4, -1, 2, -7, 3, -5, 6]`

**Explanation:** The positive numbers in order are `[4, 2, 3, 6]` and the negative numbers in order are `[-1, -7, -5]`. Alternating gives `4, -1, 2, -7, 3, -5`, and the leftover positive `6` is appended at the end. The array already follows the required pattern, so the output is the same as the input.

### Example 3

**Input:** `nums = [1, -1, -2, -3, 4, 5]`
**Output:** `[1, -1, 4, -2, 5, -3]`

**Explanation:** The positive numbers in order are `[1, 4, 5]` and the negative numbers in order are `[-1, -2, -3]`. Both groups have exactly 3 elements, so they alternate fully: `1, -1, 4, -2, 5, -3`.

## Constraints

- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
- `nums[i] != 0`

## Follow-up

Can you solve it in O(n) time and O(n) extra space while preserving the relative order of elements?

<br><br>

## Approach 1: Brute Force (In-Place Rotation)

### Intuition

Think about what the final array should look like before writing any code. If `countPos` is the number of positive elements and `countNeg` is the number of negative elements, then:

- The first `2 * min(countPos, countNeg)` positions strictly alternate, starting with positive at index `0`, negative at index `1`, and so on.
- All remaining positions (if any) belong to whichever group is larger, and they simply continue in their original relative order.

So, before touching the array, we can compute an "expected sign" for every index without using any extra array, just two counters. Once we know what sign should sit at index `i`, we walk through the array left to right. If `nums[i]` already has the expected sign, we leave it alone. If it does not, we scan forward to find the nearest element that does have the expected sign, and rotate the segment between `i` and that element so the needed value slides into position `i` while everything in between shifts one step to the right. A rotation never changes the relative order of the elements it shifts, so the order requirement stays satisfied.

### Algorithm

1. Count `countPos` (positive elements) and `countNeg` (negative elements).
2. Let `limit = 2 * min(countPos, countNeg)`. This is how many indices strictly alternate.
3. Let `fillerIsPositive = countPos > countNeg`. This tells us the sign of the leftover block (only relevant when `i >= limit`).
4. For each index `i` from `0` to `n - 1`:
   - If `i < limit`, the expected sign is positive when `i` is even and negative when `i` is odd.
   - If `i >= limit`, the expected sign is `fillerIsPositive`.
   - If `nums[i]` already matches the expected sign, move to the next index.
   - Otherwise, find the smallest `j > i` such that `nums[j]` matches the expected sign, then rotate `nums[i..j]` one step to the right (the value at `j` moves to `i`, and everything from `i` to `j - 1` shifts right by one).
5. Return `nums`.

### Code

```python
def rearrange_alternate(nums):
    n = len(nums)
    count_pos = sum(1 for x in nums if x > 0)
    count_neg = n - count_pos
    limit = 2 * min(count_pos, count_neg)
    filler_is_positive = count_pos > count_neg

    for i in range(n):
        if i < limit:
            want_positive = (i % 2 == 0)
        else:
            want_positive = filler_is_positive

        if (nums[i] > 0) == want_positive:
            continue

        j = i + 1
        while (nums[j] > 0) != want_positive:
            j += 1

        value = nums[j]
        for k in range(j, i, -1):
            nums[k] = nums[k - 1]
        nums[i] = value

    return nums
```

### Explanation

The first pass computes `countPos` and `countNeg`, which gives us `limit` and `fillerIsPositive` in O(n) time and O(1) space. The main loop then walks through the array exactly once at the outer level. For every index where the current sign already matches the expected sign, no work is done. For an index where it does not match, we search forward for the nearest correct value and rotate it into place. The rotation shifts a contiguous block of the array by one position, which preserves the relative order of every element involved, so both the alternating pattern and the original ordering within each sign group are respected.

### Complexity

- **Time:** O(n^2) in the worst case. Each mismatch can require scanning and rotating up to O(n) elements, and this can happen for O(n) indices (for example, when all negatives appear before all positives in the input).
- **Space:** O(1) extra space, since the rearrangement happens in place using only a few counters and indices.

### Problem with this approach

With `nums.length` up to `10^5`, an O(n^2) solution can require on the order of `10^10` operations in the worst case, which is far too slow for the given constraints. The rotation step is the bottleneck: every time an element is out of place, we pay for shifting a large chunk of the array just to slide one value into position. To fix this, we need a way to place every element directly into its final position in a single pass, without repeatedly shifting the array.

<br><br>

## Approach 2: Separate and Merge (Optimal)

### Intuition

Instead of fixing the array in place, build the answer from scratch. Walk through `nums` once and copy every positive number into one list and every negative number into another list, in the order they appear. Because we only append while scanning left to right, both lists automatically preserve the original relative order of their respective groups, with no extra effort.

Once the two lists exist, build the result by taking one element from the positive list, then one from the negative list, repeating until one list runs out. Whatever remains in the longer list is already in the correct relative order, so it can simply be copied to the end of the result as is. This directly satisfies the follow-up: a single pass to split, a single pass to merge, and one extra array to hold the lists and the result, all O(n) time and O(n) space.

### Algorithm

1. Create two empty lists, `pos` and `neg`.
2. Iterate through `nums` once. Append each positive value to `pos` and each negative value to `neg`, preserving the order in which they appear.
3. Create an empty result array.
4. Use two pointers `i` and `j`, both starting at `0`. While `i < len(pos)` and `j < len(neg)`, append `pos[i]` then `neg[j]` to the result, and increment both pointers.
5. Append any remaining elements of `pos` (from index `i` onward) to the result, in order.
6. Append any remaining elements of `neg` (from index `j` onward) to the result, in order.
7. Return the result.

### Code

```python
def rearrange_alternate(nums):
    pos = [x for x in nums if x > 0]
    neg = [x for x in nums if x < 0]

    result = []
    i = j = 0

    while i < len(pos) and j < len(neg):
        result.append(pos[i])
        result.append(neg[j])
        i += 1
        j += 1

    result.extend(pos[i:])
    result.extend(neg[j:])

    return result
```

### Explanation

The first loop splits `nums` into `pos` and `neg` in a single O(n) pass. Order is preserved automatically because elements are appended in the same order they are visited. The second phase merges the two lists by alternating between them, starting with `pos` as required. As soon as one list is exhausted, the `while` loop stops, and the two trailing `extend` (or pointer) operations append whatever is left of the longer list, in its original order, exactly matching the rule that the larger group's remainder goes to the end unchanged.

Walking through Example 3, `nums = [1, -1, -2, -3, 4, 5]`:

- `pos = [1, 4, 5]`, `neg = [-1, -2, -3]`
- Merge step: `1, -1, 4, -2, 5, -3`
- Both lists are exhausted at the same time, so nothing extra is appended.
- Result: `[1, -1, 4, -2, 5, -3]`, which matches the expected output.

### Complexity

- **Time:** O(n). The array is scanned once to build `pos` and `neg`, and once more to build the result.
- **Space:** O(n) extra space for `pos`, `neg`, and the result array.

<br><br>

## Comparison

| Approach | Time Complexity | Space Complexity | Preserves Order |
|---|---|---|---|
| Approach 1: Brute Force (In-Place Rotation) | O(n^2) | O(1) | Yes |
| Approach 2: Separate and Merge (Optimal) | O(n) | O(n) | Yes |

For the given constraints (`nums.length` up to `10^5`), Approach 2 is the recommended solution. Approach 1 is useful mainly as a starting point in an interview, to show correctness before optimizing, or in situations where extra memory is genuinely unavailable and a slower runtime is acceptable.

### Edge Cases Worth Mentioning

- If `nums` contains only positive numbers, `neg` is empty, the merge loop never runs, and the result is just `pos` (unchanged from the input order).
- If `nums` contains only negative numbers, the same logic applies symmetrically, with `pos` empty.
- Since `nums[i] != 0` is guaranteed, every element is unambiguously positive or negative, so no special handling for zero is needed.