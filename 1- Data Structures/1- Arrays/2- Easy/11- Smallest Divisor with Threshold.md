# Find the Smallest Divisor Given a Threshold

`Amazon` • `Google` • `Microsoft` • `Salesforce` • `PayPal` • `ByteDance` • `Visa`

## Problem Statement

You are given an array of integers `nums` and an integer `threshold`.

- Pick a **positive integer** called `divisor`.
- Divide **every** element of `nums` by that divisor.
- Round each division **up** to the nearest integer (ceiling).
- Add all those rounded values together.

Your job is to find the **smallest** divisor for which this total sum is less than or equal to `threshold`.

Rounding examples: `7 / 3` becomes `3` (not 2), and `10 / 2` becomes `5`.

The test cases are designed so that an answer always exists.

## Examples

**Example 1**

```ini
Input:  nums = [1, 2, 5, 9], threshold = 6
Output: 5
```

Explanation:

- Divisor `1` gives `1 + 2 + 5 + 9 = 17` (too big)
- Divisor `4` gives `1 + 1 + 2 + 3 = 7` (still too big)
- Divisor `5` gives `1 + 1 + 1 + 2 = 5` (fits inside 6)

So `5` is the smallest divisor that works.

**Example 2**

```ini
Input:  nums = [44, 22, 33, 11, 1], threshold = 5
Output: 44
```

Explanation: the array has 5 elements, and every element contributes **at least 1** after rounding up. So the sum can never go below 5. We need a divisor big enough that every element rounds down to exactly 1, and that happens only at `44` (the largest element).

## Constraints

- `1 <= nums.length <= 5 * 10^4`
- `1 <= nums[i] <= 10^6`
- `nums.length <= threshold <= 10^6`

<br><br>

## Intuition

Let us think about it in a very simple way.

**Step 1: What happens when the divisor grows?**

- Small divisor means each number stays big, so the total sum is **large**.
- Large divisor means each number shrinks, so the total sum is **small**.

So as the divisor increases, the sum **only decreases** (it never goes up again).

**Step 2: This creates a clean True / False pattern**

If we ask "does this divisor keep the sum within the threshold?" for every divisor from 1 upward, we get something like:

```ini
divisor :  1      2      3      4      5      6      7   ...
works?  : False  False  False  False  True   True   True ...
                                        ^
                                   our answer
```

Once a divisor works, every bigger divisor also works. Once a divisor fails, every smaller divisor also fails.

<mark>This False, False, ..., True, True pattern is exactly what binary search needs. We are not searching inside the array, we are searching on the range of possible answers.</mark>

**Step 3: What is the search range?**

- **Lowest possible divisor** is `1` (the smallest positive integer allowed).
- **Highest useful divisor** is `max(nums)`. At that point every element becomes `1` after rounding up, and the sum is just `len(nums)`. Going any higher changes nothing, because the constraints promise `nums.length <= threshold`, so this always works.

So we binary search on the range `[1, max(nums)]` and look for the **first** `True`.

<br><br>

## Approach

**Step 1: Set up the search boundaries**

- `low = 1`, because the smallest divisor we are allowed to pick is 1.
- `high = max(nums)`, because any divisor at least as big as the largest element turns every value into 1.
- `ans = -1`, a placeholder that will hold the best working divisor we have seen so far.

**Step 2: Keep searching while `low <= high`**

- Pick the middle divisor: `mid = (low + high) // 2`.

**Step 3: Test that middle divisor**

- Start a counter `div_sum = 0`.
- Walk through every number in `nums` one by one.
- For each number, divide it by `mid`, round the result **up**, and add it to `div_sum`.
- After the loop, compare `div_sum` with `threshold`.

**Step 4: Decide which half to keep**

- If `div_sum <= threshold`, this divisor **works**:
  - Save it with `ans = mid`.
  - A smaller divisor might also work, so shrink the range to the left with `high = mid - 1`.
- If `div_sum > threshold`, this divisor is **too small** and the sum overflowed:
  - Everything to its left is also too small, so shrink the range to the right with `low = mid + 1`.

**Step 5: Return the saved answer**

- The loop stops the moment `low` crosses past `high`.
- At that point `ans` is holding the smallest divisor that ever passed the test, so return it.

The key idea: <mark>when a divisor works we do not stop, we save it and keep pushing left to see if an even smaller divisor also works.</mark>

<br><br>

## Code

```python
class Solution:
    def divisionPossible(self, nums, threshold, divisor):
        div_sum = 0

        for num in nums:
            div_sum += math.ceil(num / divisor)
        
        return div_sum <= threshold
        

    def smallestDivisor(self, nums: List[int], threshold: int) -> int:
        low, high = 1, max(nums)
        ans = -1

        while low <= high:
            mid = (low + high) // 2
            
            if self.divisionPossible(nums, threshold, mid):
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        
        return ans
```

<br><br>

## Dry Run

Let us walk through `nums = [1, 2, 5, 9]` and `threshold = 6`, step by step.

```ini
INITIAL SETUP

nums      = [1, 2, 5, 9]
threshold = 6
max(nums) = 9

low  = 1
high = 9
ans  = -1


ITERATION 1

Loop check : low (1) <= high (9)  ->  True, enter loop
mid        = (1 + 9) // 2 = 5

Now test divisor = 5

div_sum = 0

num = 1  ->  ceil(1 / 5) = ceil(0.2) = 1   ->  div_sum = 0 + 1 = 1
num = 2  ->  ceil(2 / 5) = ceil(0.4) = 1   ->  div_sum = 1 + 1 = 2
num = 5  ->  ceil(5 / 5) = ceil(1.0) = 1   ->  div_sum = 2 + 1 = 3
num = 9  ->  ceil(9 / 5) = ceil(1.8) = 2   ->  div_sum = 3 + 2 = 5

Compare : div_sum (5) <= threshold (6)  ->  True

Action  : divisor 5 works, so save it     ->  ans  = 5
          try to find something smaller   ->  high = mid - 1 = 4

State   : low = 1, high = 4, ans = 5


ITERATION 2

Loop check : low (1) <= high (4)  ->  True, enter loop
mid        = (1 + 4) // 2 = 2

Now test divisor = 2

div_sum = 0

num = 1  ->  ceil(1 / 2) = ceil(0.5) = 1   ->  div_sum = 0 + 1 = 1
num = 2  ->  ceil(2 / 2) = ceil(1.0) = 1   ->  div_sum = 1 + 1 = 2
num = 5  ->  ceil(5 / 2) = ceil(2.5) = 3   ->  div_sum = 2 + 3 = 5
num = 9  ->  ceil(9 / 2) = ceil(4.5) = 5   ->  div_sum = 5 + 5 = 10

Compare : div_sum (10) <= threshold (6)  ->  False

Action  : divisor 2 is too small, the sum overflowed
          need a bigger divisor           ->  low = mid + 1 = 3

State   : low = 3, high = 4, ans = 5


ITERATION 3

Loop check : low (3) <= high (4)  ->  True, enter loop
mid        = (3 + 4) // 2 = 3

Now test divisor = 3

div_sum = 0

num = 1  ->  ceil(1 / 3) = ceil(0.33) = 1  ->  div_sum = 0 + 1 = 1
num = 2  ->  ceil(2 / 3) = ceil(0.66) = 1  ->  div_sum = 1 + 1 = 2
num = 5  ->  ceil(5 / 3) = ceil(1.66) = 2  ->  div_sum = 2 + 2 = 4
num = 9  ->  ceil(9 / 3) = ceil(3.0)  = 3  ->  div_sum = 4 + 3 = 7

Compare : div_sum (7) <= threshold (6)  ->  False

Action  : divisor 3 is still too small
          need a bigger divisor           ->  low = mid + 1 = 4

State   : low = 4, high = 4, ans = 5


ITERATION 4

Loop check : low (4) <= high (4)  ->  True, enter loop
mid        = (4 + 4) // 2 = 4

Now test divisor = 4

div_sum = 0

num = 1  ->  ceil(1 / 4) = ceil(0.25) = 1  ->  div_sum = 0 + 1 = 1
num = 2  ->  ceil(2 / 4) = ceil(0.5)  = 1  ->  div_sum = 1 + 1 = 2
num = 5  ->  ceil(5 / 4) = ceil(1.25) = 2  ->  div_sum = 2 + 2 = 4
num = 9  ->  ceil(9 / 4) = ceil(2.25) = 3  ->  div_sum = 4 + 3 = 7

Compare : div_sum (7) <= threshold (6)  ->  False

Action  : divisor 4 misses by just 1
          need a bigger divisor           ->  low = mid + 1 = 5

State   : low = 5, high = 4, ans = 5


LOOP ENDS

Loop check : low (5) <= high (4)  ->  False

Exit the while loop
return ans = 5

Final answer = 5, which matches the expected output


SUMMARY TABLE

Iter | low | high | mid | div_sum | works? | action              | ans
=====|=====|======|=====|=========|========|=====================|=====
  1  |  1  |  9   |  5  |    5    |  True  | ans=5, high=4       |  5
  2  |  1  |  4   |  2  |   10    | False  | low=3               |  5
  3  |  3  |  4   |  3  |    7    | False  | low=4               |  5
  4  |  4  |  4   |  4  |    7    | False  | low=5               |  5
=====|=====|======|=====|=========|========|=====================|=====
  5  |  5  |  4   |  -  |    -    |   -    | loop ends, return 5 |  5

Note: ans gets locked at 5 in the very first iteration,
and every later step only confirms that nothing smaller can work.
```

<br><br>

## Complexity Analysis

**Time Complexity: O(n * log(max(nums)))**

- The binary search runs about `log(max(nums))` times, so at most around 20 iterations when `max(nums)` is `10^6`.
- Each iteration scans the whole array once, which is `O(n)`.

**Space Complexity: O(1)**

- Only a handful of variables are used (`low`, `high`, `mid`, `ans`, `div_sum`).
- No extra arrays or data structures are created.

<br><br>

## Key Points to Remember

- The search space is the **answer range** `[1, max(nums)]`, not the array itself. This pattern is called **binary search on the answer**.
- The `ans` variable is what makes this template safe. Even if the loop shrinks past the correct value, the best working divisor stays saved.
- `high` starts at `max(nums)` because any divisor larger than that gives the exact same sum (every element becomes 1), so searching further is pointless.
- <mark>Rounding must be up, never down. Using plain integer division (//) here is the most common mistake and will give a wrong answer.</mark>
- The constraint `nums.length <= threshold` is the guarantee that an answer always exists, so `ans` will never stay `-1`.

<br><br>

## Related Problems

- [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/)
- [Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)
- [Minimum Number of Days to Make m Bouquets](https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets/)
- [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/)
- [Minimum Speed to Arrive on Time](https://leetcode.com/problems/minimum-speed-to-arrive-on-time/)
- [Minimum Time to Complete Trips](https://leetcode.com/problems/minimum-time-to-complete-trips/)
- [Magnetic Force Between Two Balls](https://leetcode.com/problems/magnetic-force-between-two-balls/)
- [Minimize Max Distance to Gas Station](https://leetcode.com/problems/minimize-max-distance-to-gas-station/)
- [Find the Smallest Divisor Given a Threshold](https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/)