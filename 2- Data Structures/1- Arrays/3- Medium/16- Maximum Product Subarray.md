# Maximum Product Subarray

`Amazon` • `Microsoft` • `Google`

## Problem Statement

Given an integer array `nums`, find a subarray that has the largest product, and return the product.

The test cases are generated so that the answer will fit in a 32-bit integer.

Note that the product of an array with a single element is the value of that element.

## Examples

**Example 1**

```
Input: nums = [2,3,-2,4]
Output: 6
Explanation: [2,3] has the largest product 6.
```

**Example 2**

```
Input: nums = [-2,0,-1]
Output: 0
Explanation: The result cannot be 2, because [-2,-1] is not a subarray.
```

## Constraints

- `1 <= nums.length <= 2 * 10^4`
- `-10 <= nums[i] <= 10`
- The product of any subarray of `nums` is guaranteed to fit in a 32-bit integer.

<br><br>

## Approach 1: Brute Force (Three Nested Loops)

**Idea**

The simplest way is to check every subarray directly.

- Pick a start index `i` and an end index `j` to mark a subarray.
- Use a third loop to multiply every element from `i` to `j`.
- Compare each product with the best value so far and keep the maximum.

**Solution**

```python
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        n = len(nums)
        maxi = float('-inf')

        for i in range(n):
            for j in range(i, n):
                prod = 1
                for k in range(i, j + 1):
                    prod *= nums[k]
                maxi = max(maxi, prod)

        return maxi
```

**Explanation**

- The two outer loops (`i` and `j`) fix the left and right boundary of a subarray.
- The inner loop (`k`) walks that range and multiplies the elements to get its product.
- Since we try every `(i, j)` pair, no subarray is missed, so the result is always correct.
- The downside is that the product for each subarray is built again from scratch.

**Dry Run** (nums = [2, 3, -2, 4])

```
i=0:
  j=0 -> product of [2]         = 2      maxi = 2
  j=1 -> product of [2,3]       = 6      maxi = 6
  j=2 -> product of [2,3,-2]    = -12    maxi = 6
  j=3 -> product of [2,3,-2,4]  = -48    maxi = 6
i=1:
  j=1 -> product of [3]         = 3      maxi = 6
  j=2 -> product of [3,-2]      = -6     maxi = 6
  j=3 -> product of [3,-2,4]    = -24    maxi = 6
i=2:
  j=2 -> product of [-2]        = -2     maxi = 6
  j=3 -> product of [-2,4]      = -8     maxi = 6
i=3:
  j=3 -> product of [4]         = 4      maxi = 6

Answer = 6
```

**Complexity**

- Time: O(n^3). There are about n^2 subarrays, and each one takes up to n multiplications.
- Space: O(1). Only a couple of variables are used.

**What is the problem here and what can we do better**

- The inner loop repeats work we already did.
- The subarray from `i` to `j + 1` is simply the subarray from `i` to `j` times one more element.
- So we can carry the running product forward instead of rebuilding it.
- That removes the inner loop and gives us Approach 2.

<br><br>

## Approach 2: Better (Two Nested Loops)

**Idea**

Keep a running product while extending the subarray, so no recomputation is needed.

- Fix a start index `i`.
- Walk `j` from `i` to the end, extending the subarray one element at a time.
- Multiply each new element into the running product, so every step costs a single multiply.

**Solution**

```python
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        n = len(nums)
        maxi = float('-inf')

        for i in range(n):
            prod = 1
            for j in range(i, n):
                prod *= nums[j]
                maxi = max(maxi, prod)

        return maxi
```

**Explanation**

- `prod` always holds the product of the subarray from `i` up to the current `j`.
- Each step multiplies `prod` by `nums[j]`, the element we just added.
- After each step we compare `prod` with `maxi` and keep the larger one.
- Reusing the running product removes the innermost loop from Approach 1.

**Dry Run** (nums = [2, 3, -2, 4])

```
i=0, prod=1:
  j=0 -> prod = 1 * 2   = 2     maxi = 2
  j=1 -> prod = 2 * 3   = 6     maxi = 6
  j=2 -> prod = 6 * -2  = -12   maxi = 6
  j=3 -> prod = -12 * 4 = -48   maxi = 6
i=1, prod=1:
  j=1 -> prod = 1 * 3   = 3     maxi = 6
  j=2 -> prod = 3 * -2  = -6    maxi = 6
  j=3 -> prod = -6 * 4  = -24   maxi = 6
i=2, prod=1:
  j=2 -> prod = 1 * -2  = -2    maxi = 6
  j=3 -> prod = -2 * 4  = -8    maxi = 6
i=3, prod=1:
  j=3 -> prod = 1 * 4   = 4     maxi = 6

Answer = 6
```

**Complexity**

- Time: O(n^2). For each of the n start indices we scan the rest of the array once.
- Space: O(1).

**What is the problem here and what can we do better**

- We still begin a fresh scan for every start index, so elements get revisited many times.
- But a product only changes in a few meaningful ways: it grows with positives, flips sign with negatives, and dies at zeros.
- If we handle sign and zeros directly, one pass from the left and one pass from the right are enough.
- That reasoning leads to the optimal Approach 3.

<br><br>

## Approach 3: Optimal (Prefix and Suffix Products)

**Intuition**

Instead of checking subarrays, look at what makes a product large or small. The behaviour depends only on the signs of the numbers and on zeros, which splits into four cases.

**Case 1: All positive**

- Every element is positive.
- Multiplying in one more positive always makes the product bigger.
- So the best subarray is the whole array, and a plain running product finds it.

**Case 2: Even count of negatives (rest positive)**

- A negative times a negative gives a positive.
- With an even number of negatives, they pair up and their signs cancel.
- The product of the entire array is therefore positive, and that full product is the largest.

**Case 3: Odd count of negatives (rest positive)**

This is the tricky case, and it is the reason we need two directions.

- An odd number of negatives makes the sign of the whole product negative.
- To turn it positive, we must remove exactly one negative.
- A subarray has to be contiguous, so we can only cut from an end, never from the middle.
- Cutting the front up to and including the first negative leaves a subarray that ends at the right side (a suffix).
- Cutting the back from the last negative onward leaves a subarray that starts at the left side (a prefix).
- We cannot tell in advance which cut gives the bigger product.
- So we grow one product from the left (the prefix option) and one from the right (the suffix option), and one of them will drop the unwanted negative.

**Case 4: Zeroes**

- Any subarray that contains a zero has product 0.
- A zero therefore acts like a wall, splitting the array into independent segments.
- Whenever the running product becomes 0, we reset it to 1.
- That restart begins a fresh subarray right after the zero.
- Each segment between zeros is then just one of the cases above.

**Putting it together**

- Grow a prefix product from the left and a suffix product from the right in the same loop.
- Reset either one to 1 as soon as it hits a zero.
- Track the best value seen across both, and that value is the answer.

**Solution**

```python
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        pre, suf = 1, 1
        maxi = float('-inf')

        n = len(nums)

        for i in range(n):
            if pre == 0: pre = 1
            if suf == 0: suf = 1

            pre = pre * nums[i]
            suf = suf * nums[n - i - 1]

            maxi = max(maxi, pre, suf)

        return maxi
```

**Explanation**

- `pre` is the running product from the left, so it represents subarrays that start at the left of the current segment.
- `suf` is the running product from the right, so it represents subarrays that end at the right of the current segment.
- Before multiplying, any value of 0 is reset to 1, which cleanly separates one segment from the next (Case 4).
- Taking `max(maxi, pre, suf)` at each step means the side that avoids the leftover negative (Case 3), or sits on the best segment, is always captured.
- Everything happens in a single loop over the array, so the work is linear.

**Dry Run A** (nums = [2, 3, -2, 4], one negative, so the odd case)

```
n = 4, pre = 1, suf = 1, maxi = -inf

i=0:
  pre not 0, suf not 0
  pre = 1 * nums[0]  = 1 * 2   = 2
  suf = 1 * nums[3]  = 1 * 4   = 4
  maxi = max(-inf, 2, 4)       = 4
i=1:
  pre = 2 * nums[1]  = 2 * 3   = 6
  suf = 4 * nums[2]  = 4 * -2  = -8
  maxi = max(4, 6, -8)         = 6
i=2:
  pre = 6 * nums[2]  = 6 * -2  = -12
  suf = -8 * nums[1] = -8 * 3  = -24
  maxi = max(6, -12, -24)      = 6
i=3:
  pre = -12 * nums[3]= -12 * 4 = -48
  suf = -24 * nums[0]= -24 * 2 = -48
  maxi = max(6, -48, -48)      = 6

Answer = 6   (the prefix [2,3] wins, which matches Case 3)
```

**Dry Run B** (nums = [-2, 0, -1], shows the zero reset)

```
n = 3, pre = 1, suf = 1, maxi = -inf

i=0:
  pre not 0, suf not 0
  pre = 1 * nums[0]  = 1 * -2  = -2
  suf = 1 * nums[2]  = 1 * -1  = -1
  maxi = max(-inf, -2, -1)     = -1
i=1:
  pre not 0, suf not 0
  pre = -2 * nums[1] = -2 * 0  = 0
  suf = -1 * nums[1] = -1 * 0  = 0
  maxi = max(-1, 0, 0)         = 0
i=2:
  pre == 0 -> reset pre = 1
  suf == 0 -> reset suf = 1
  pre = 1 * nums[2]  = 1 * -1  = -1
  suf = 1 * nums[0]  = 1 * -2  = -2
  maxi = max(0, -1, -2)        = 0

Answer = 0   (the zero resets both products, which matches Case 4)
```

**Complexity**

- Time: O(n). A single pass updates both the prefix and suffix products together.
- Space: O(1). Only a handful of variables are used.

<br><br>

## Related Problems

- Maximum Subarray (Kadane's Algorithm)
- Maximum Sum Circular Subarray
- Subarray Product Less Than K
- Maximum Subarray Min-Product
- Product of Array Except Self