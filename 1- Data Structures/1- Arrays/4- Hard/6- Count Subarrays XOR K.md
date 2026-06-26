# Count Subarrays with Given XOR K

`Amazon` • `InterviewBit` • `GeeksforGeeks`
<br>

## Problem Statement

Given an array of integers `nums` and an integer `k`, return the total number of subarrays whose XOR equals `k`.

## Examples

**Example 1**
```
Input:  nums = [4, 2, 2, 6, 4], k = 6
Output: 4
```
**Explanation:** The subarrays with XOR equal to 6 are `[4, 2]`, `[4, 2, 2, 6, 4]`, `[2, 2, 6]`, and `[6]`.

**Example 2**
```
Input:  nums = [5, 6, 7, 8, 9], k = 5
Output: 2
```
**Explanation:** The subarrays with XOR equal to 5 are `[5]` and `[5, 6, 7, 8, 9]`.

## Constraints

- `1 <= nums.length <= 10^5`
- `0 <= nums[i] <= 10^5`
- `0 <= k <= 10^5`

<br><br>

## Approach 1: Brute Force (Triple Loop)

**Intuition**

For every pair of indices `(i, j)`, compute the XOR of the subarray `nums[i...j]` from scratch using a third inner loop. If the XOR equals `k`, increment the count.

This is the most naive approach and does redundant work by recomputing XOR from scratch for every subarray instead of building on previous results.

```python
def subarraysWithXorK(nums, k):
    count = 0
    n = len(nums)
    for i in range(n):
        for j in range(i, n):
            xor = 0
            for l in range(i, j + 1):
                xor ^= nums[l]
            if xor == k:
                count += 1
    return count
```

- **Time Complexity:** O(n³)
- **Space Complexity:** O(1)

<br><br>

## Approach 2: Optimized Brute Force (Double Loop)

**Intuition**

Instead of recomputing XOR from scratch for each `(i, j)` pair, maintain a running XOR as we extend the subarray from a fixed start index `i`. Each new element is simply XOR-ed into the running value, eliminating the innermost loop entirely.

```python
def subarraysWithXorK(nums, k):
    count = 0
    n = len(nums)
    for i in range(n):
        xor = 0
        for j in range(i, n):
            xor ^= nums[j]
            if xor == k:
                count += 1
    return count
```

- **Time Complexity:** O(n²)
- **Space Complexity:** O(1)

<br><br>

## Approach 3: Prefix XOR + HashMap

**Intuition**

Define `prefXOR[i]` as the XOR of all elements from index `0` to `i`. The XOR of any subarray `[l+1 ... r]` can be expressed as:

```
XOR(l+1, r) = prefXOR[r] ^ prefXOR[l]
```

We want this to equal `k`, so:

```
prefXOR[r] ^ prefXOR[l] = k
=> prefXOR[l] = prefXOR[r] ^ k
```

This means at each index `r`, we need to count how many previous prefix XOR values equal `currentXOR ^ k`. A frequency map makes this lookup O(1), reducing the entire solution to a single pass.

**Why seed with `{0: 1}`?**

If a valid subarray starts at index 0, then `prefXOR[r] == k`, which means `target = k ^ k = 0`. Without pre-seeding `0` in the map, this case would be missed. The value `1` represents the one "empty prefix" that exists before the array begins.

```python
class Solution:
    def subarraysWithXorK(self, nums, k):
        freq = {0: 1}
        xor = 0
        count = 0

        for num in nums:
            xor ^= num
            target = xor ^ k

            if target in freq:
                count += freq[target]

            freq[xor] = freq.get(xor, 0) + 1

        return count
```

- **Time Complexity:** O(n)
- **Space Complexity:** O(n)

<br><br>

## Approach 4: O(n) Time, O(1) Space

**Why this is not achievable for the general case**

Unlike subarray sum problems where a sliding window works because addition has a monotonic property, XOR does not. Adding an element to a window can both increase or decrease the XOR unpredictably, and removing an element from the left of the window requires knowing its contribution, which cannot be recovered without extra state.

There is no known general O(n) time, O(1) space solution for counting subarrays with XOR equal to an arbitrary `k`. The HashMap in Approach 3 is fundamentally necessary to avoid quadratic time, and it grows linearly with the number of distinct prefix XOR values seen.

**Exception: when `k = 0`**

If `k = 0`, the problem reduces to counting subarrays where XOR of all elements is 0, which means `prefXOR[r] == prefXOR[l]`. This is still best handled with a HashMap in the general case, so O(1) space does not apply here either.

**Conclusion**

Approach 3 (Prefix XOR + HashMap) is the optimal solution for this problem. O(n) time with O(n) space is the best achievable complexity for the general case.

<br><br>

## Walkthrough: `nums = [4, 2, 2, 6, 4]`, `k = 6`

| Step | num | xor | target (`xor ^ k`) | freq (before update)   | count |
|:----:|:---:|:---:|:------------------:|:----------------------:|:-----:|
| init | -   | 0   | -                  | `{0:1}`                | 0     |
| 1    | 4   | 4   | 2                  | `{0:1}`                | 0     |
| 2    | 2   | 6   | 0                  | `{0:1, 4:1}`           | 1     |
| 3    | 2   | 4   | 2                  | `{0:1, 4:1, 6:1}`      | 1     |
| 4    | 6   | 2   | 4                  | `{0:1, 4:2, 6:1}`      | 3     |
| 5    | 4   | 6   | 0                  | `{0:1, 4:2, 6:1, 2:1}` | 4     |

**Output: `4`**

<br><br>

## Related Problems

| Problem | Key Similarity |
|:--------|:---------------|
| [Subarray Sum Equals K](https://github.com/AbdullahButt2611/Interview-Questions/blob/main/1-%20Data%20Structures/1-%20Arrays/3-%20Medium/7-%20Sub-Array%20Sum%20Equals%20K.md) | Same prefix + HashMap pattern, but uses addition instead of XOR. If you can solve one, the other follows directly. |