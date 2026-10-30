# Product of Array Except Self

`Meta` • `Amazon` • `Microsoft` • `Google` • `Apple` • `Netflix` • `Adobe` • `Quantcast`

## Problem Statement

Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the **product of all the elements** of `nums` **except** `nums[i]`.

- The product of any prefix or suffix of `nums` is guaranteed to fit in a **32-bit integer**.
- You must write an algorithm that runs in **O(n)** time.
- You are **not allowed to use the division** operation.

**Follow up:** Can you solve it in **O(1) extra space**? (The output array does not count as extra space.)

## Examples

**Example 1:**

```ini
Input:  nums = [1, 2, 3, 4]
Output: [24, 12, 8, 6]
```

**Explanation:**

- For index `0`: 2 × 3 × 4 = 24
- For index `1`: 1 × 3 × 4 = 12
- For index `2`: 1 × 2 × 4 = 8
- For index `3`: 1 × 2 × 3 = 6

**Example 2:**

```ini
Input:  nums = [-1, 1, 0, -3, 3]
Output: [0, 0, 9, 0, 0]
```

**Explanation:**

- Every position except index `2` includes the `0` in its product, so it becomes `0`.
- For index `2`: (-1) × 1 × (-3) × 3 = 9

## Constraints

- `2 <= nums.length <= 10^5`
- `-30 <= nums[i] <= 30`
- The product of any prefix or suffix of `nums` fits in a 32-bit integer.

<br><br>

## The Key Idea (Remember This Forever)

Pick any position `i` in the array. Everything except `nums[i]` is made of two parts:

- Everything on its **left**
- Everything on its **right**

So the answer is simply:

<mark>answer[i] = (product of everything on the left) × (product of everything on the right)</mark>

Think of it like this: **stand at index `i`, look left, look right, multiply what you see.** You never touch `nums[i]` itself.

For `nums = [1, 2, 3, 4]` at index `2` (value `3`):

```ini
Left side  = [1, 2]  → 1 × 2 = 2
Right side = [4]     → 4
Answer     = 2 × 4   = 8
```

If there is nothing on one side (the first or last index), that side counts as `1`, because multiplying by `1` changes nothing.

<br><br>

## Approach 1: Brute Force

### Idea

- For every index `i`, loop through the whole array again.
- Multiply every number except the one at `i`.
- Save that product as `answer[i]`.

### Code

```python
class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)
        answer = []

        for i in range(n):
            product = 1
            for j in range(n):
                if i != j:
                    product *= nums[j]
            answer.append(product)

        return answer
```

### Complexity Analysis

- **Time Complexity:** O(n²), because of the two nested loops.
- **Space Complexity:** O(1), ignoring the output array.

### Why This Is Not Enough

- With `n = 10^5`, this does about **10 billion** multiplications. Way too slow.
- We keep multiplying the **same numbers again and again** for every index. That repeated work is what we need to remove.

<br><br>

## Approach 2: Prefix and Suffix Arrays

### Idea

Instead of recomputing the left and right products for every index, we **build them once and reuse them**.

- **Step 1: Build a `prefix` array.**
  - `prefix[i]` = product of everything **to the left** of `i`.
  - Start with `prefix[0] = 1` (nothing on the left).
  - Walk left to right: each new value is the previous left product times the previous number.
  - `prefix[i] = prefix[i - 1] × nums[i - 1]`
- **Step 2: Build a `suffix` array.**
  - `suffix[i]` = product of everything **to the right** of `i`.
  - Start with `suffix[n - 1] = 1` (nothing on the right).
  - Walk right to left: each new value is the next right product times the next number.
  - `suffix[i] = suffix[i + 1] × nums[i + 1]`
- **Step 3: Combine them.**
  - `answer[i] = prefix[i] × suffix[i]`

The trick is that each product is built from the one next to it, so every step is just **one multiplication**.

### Code

```python
class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)
        prefix = [1] * n
        suffix = [1] * n
        answer = [1] * n

        # Step 1: product of everything to the LEFT of each index
        for i in range(1, n):
            prefix[i] = prefix[i - 1] * nums[i - 1]

        # Step 2: product of everything to the RIGHT of each index
        for i in range(n - 2, -1, -1):
            suffix[i] = suffix[i + 1] * nums[i + 1]

        # Step 3: left product × right product
        for i in range(n):
            answer[i] = prefix[i] * suffix[i]

        return answer
```

### Dry Run

```ini
nums = [1, 2, 3, 4]
n    = 4

Start:
prefix = [1, 1, 1, 1]
suffix = [1, 1, 1, 1]
answer = [1, 1, 1, 1]

Step 1: Build prefix (left to right, i = 1 to 3)

Iteration 1 (i = 1):
    prefix[1] = prefix[0] × nums[0] = 1 × 1 = 1
    prefix    = [1, 1, 1, 1]

Iteration 2 (i = 2):
    prefix[2] = prefix[1] × nums[1] = 1 × 2 = 2
    prefix    = [1, 1, 2, 1]

Iteration 3 (i = 3):
    prefix[3] = prefix[2] × nums[2] = 2 × 3 = 6
    prefix    = [1, 1, 2, 6]

Step 2: Build suffix (right to left, i = 2 down to 0)

Iteration 1 (i = 2):
    suffix[2] = suffix[3] × nums[3] = 1 × 4 = 4
    suffix    = [1, 1, 4, 1]

Iteration 2 (i = 1):
    suffix[1] = suffix[2] × nums[2] = 4 × 3 = 12
    suffix    = [1, 12, 4, 1]

Iteration 3 (i = 0):
    suffix[0] = suffix[1] × nums[1] = 12 × 2 = 24
    suffix    = [24, 12, 4, 1]

Step 3: Combine (i = 0 to 3)

Iteration 1 (i = 0):  answer[0] = prefix[0] × suffix[0] = 1 × 24 = 24
Iteration 2 (i = 1):  answer[1] = prefix[1] × suffix[1] = 1 × 12 = 12
Iteration 3 (i = 2):  answer[2] = prefix[2] × suffix[2] = 2 × 4  = 8
Iteration 4 (i = 3):  answer[3] = prefix[3] × suffix[3] = 6 × 1  = 6

Final answer = [24, 12, 8, 6]
```

### Complexity Analysis

- **Time Complexity:** O(n), three separate passes over the array.
- **Space Complexity:** O(n), for the extra `prefix` and `suffix` arrays.
- **No division used.**

### What Can Still Be Improved

- We are using **two extra arrays** (`prefix` and `suffix`) just to hold in-between values.
- We are using **three loops**, when the third loop only multiplies two values we already have.
- The follow up asks for **O(1) extra space**. So let's make it even better.

<br><br>

## Approach 3: Optimal (Output Array + One Running Variable)

### Idea

Two simple observations remove all the extra space:

- **Observation 1: The output array can hold the prefix.**
  - We have to return `answer` anyway, and it does not count as extra space.
  - So we store the left products **directly inside `answer`**. No `prefix` array needed.
- **Observation 2: The suffix only needs one number at a time.**
  - When walking right to left, we only ever use the **current** right product.
  - So a single variable `suffix` is enough. No `suffix` array needed.
  - At each step, we multiply it into `answer[j]` right away. No third loop needed.

So the plan becomes:

- **Pass 1 (left to right):** fill `answer[i]` with the product of everything to the left of `i`.
- **Pass 2 (right to left):** keep a running `suffix` (product of everything to the right) and multiply it into `answer[j]`.

After pass 2, every `answer[j]` holds <mark>left product × right product</mark>, which is exactly what we want.

### Code

```python
class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)
        answer = [1] * n

        # Pass 1: answer[i] = product of everything to the LEFT of i
        for i in range(1, n):
            answer[i] = answer[i - 1] * nums[i - 1]

        # Pass 2: multiply in the product of everything to the RIGHT of j
        suffix = 1
        for j in range(n - 2, -1, -1):
            suffix = suffix * nums[j + 1]
            answer[j] = answer[j] * suffix

        return answer
```

### Dry Run

```ini
nums = [1, 2, 3, 4]
n    = 4

Start:
answer = [1, 1, 1, 1]

Pass 1: Store LEFT products in answer (i = 1 to 3)

Iteration 1 (i = 1):
    Left of index 1 is [1]
    answer[1] = answer[0] × nums[0] = 1 × 1 = 1
    answer    = [1, 1, 1, 1]

Iteration 2 (i = 2):
    Left of index 2 is [1, 2]
    answer[2] = answer[1] × nums[1] = 1 × 2 = 2
    answer    = [1, 1, 2, 1]

Iteration 3 (i = 3):
    Left of index 3 is [1, 2, 3]
    answer[3] = answer[2] × nums[2] = 2 × 3 = 6
    answer    = [1, 1, 2, 6]

After Pass 1:
    answer = [1, 1, 2, 6]   (each slot = product of everything on its left)

Pass 2: Multiply in RIGHT products (j = 2 down to 0)

Set suffix = 1
    Index 3 has nothing on its right, so its right product is 1.
    answer[3] = 6 × 1 = 6 stays as it is. That is why the loop starts at n - 2.

Iteration 1 (j = 2):
    Right of index 2 is [4]
    suffix    = suffix × nums[3] = 1 × 4 = 4
    answer[2] = answer[2] × suffix = 2 × 4 = 8
    answer    = [1, 1, 8, 6]

Iteration 2 (j = 1):
    Right of index 1 is [3, 4]
    suffix    = suffix × nums[2] = 4 × 3 = 12
    answer[1] = answer[1] × suffix = 1 × 12 = 12
    answer    = [1, 12, 8, 6]

Iteration 3 (j = 0):
    Right of index 0 is [2, 3, 4]
    suffix    = suffix × nums[1] = 12 × 2 = 24
    answer[0] = answer[0] × suffix = 1 × 24 = 24
    answer    = [24, 12, 8, 6]

Final answer = [24, 12, 8, 6]
```

### Complexity Analysis

- **Time Complexity:** O(n), just two passes over the array.
- **Space Complexity:** O(1) extra space, since only the `suffix` variable is used (the output array does not count).
- **No division used.**

### Why This Is the Best

- Same O(n) time as Approach 2, but with **one less loop**.
- Drops the two extra arrays, bringing space from **O(n) down to O(1)**.
- Fully satisfies the follow up.

<br><br>

## Summary of Approaches

| Approach               | Idea                                                     | Time  | Extra Space | Division Used |
| :--------------------- | :------------------------------------------------------- | :---: | :---------: | :-----------: |
| Brute Force            | Nested loops for each index                              | O(n²) |    O(1)     |      ❌       |
| Prefix + Suffix Arrays | Build left and right products once, then combine         | O(n)  |    O(n)     |      ❌       |
| Optimal                | Left products in `answer`, right product in one variable | O(n)  |    O(1)     |      ❌       |

<br><br>

## Related Problems

- [Trapping Rain Water (42)](https://leetcode.com/problems/trapping-rain-water/)
- [Maximum Product Subarray (152)](https://leetcode.com/problems/maximum-product-subarray/)
- [Range Sum Query - Immutable (303)](https://leetcode.com/problems/range-sum-query-immutable/)
- [Find Pivot Index (724)](https://leetcode.com/problems/find-pivot-index/)
- [Product of the Last K Numbers (1352)](https://leetcode.com/problems/product-of-the-last-k-numbers/)
- [Construct Product Matrix (2906)](https://leetcode.com/problems/construct-product-matrix/)
