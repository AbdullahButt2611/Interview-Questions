# Kids With the Greatest Number of Candies

`Google` • `Amazon`

## Problem Statement

There are `n` kids with candies. You are given an integer array `candies`, where `candies[i]` is the number of candies the `i`th kid has, and an integer `extraCandies`, the number of extra candies that you have.

For each kid, imagine giving them all of the `extraCandies`. Return a boolean array `result` of length `n`, where:

- `result[i]` is `true` if that kid would then have the greatest number of candies among all kids.
- `result[i]` is `false` otherwise.

Note that multiple kids can share the greatest number of candies.

## Examples

```ini
Input:  candies = [2, 3, 5, 1, 3], extraCandies = 3
Output: [true, true, true, false, true]

Explanation (the current max is 5):
Kid 0: 2 + 3 = 5  ->  5 >= 5  ->  true
Kid 1: 3 + 3 = 6  ->  6 >= 5  ->  true
Kid 2: 5 + 3 = 8  ->  8 >= 5  ->  true
Kid 3: 1 + 3 = 4  ->  4 <  5  ->  false
Kid 4: 3 + 3 = 6  ->  6 >= 5  ->  true
```

```ini
Input:  candies = [4, 2, 1, 1, 2], extraCandies = 1
Output: [true, false, false, false, false]
```

```ini
Input:  candies = [12, 1, 12], extraCandies = 10
Output: [true, false, true]
```

## Constraints

- `n == candies.length`
- `2 <= n <= 100`
- `1 <= candies[i] <= 100`
- `1 <= extraCandies <= 50`

<br><br>

## Approach

This question sounds trickier than it is. The phrase "greatest number of candies among all the kids" makes it feel like we must figure out the winner all over again for every single kid. We do not.

<mark>The bar to beat never changes. It is simply the largest candy count already sitting in the array. If a kid's own candies plus the extra candies can reach that bar, that kid can be a winner.</mark>

Here is the plain idea:

- First, find the maximum candy count in the array. This is the target every kid is trying to reach.
- Then walk through the kids one by one.
- For each kid, add the extra candies to what they already have.
- If that total is greater than or equal to the max, this kid can tie or beat everyone, so the answer is `true`. Otherwise it is `false`.
- Collect all these `true` and `false` answers into a result array and return it.

One small but important point: we check `>=` and not `>`. Since more than one kid is allowed to share the top spot, simply tying the maximum still counts as having the greatest.

Picture the max as a bar drawn on the wall. Every kid gets to stand on the very same booster stool (the extra candies, same height for everyone). We just check whether each kid, standing on that stool, reaches the bar. The bar stays fixed the whole time. We never move it.

<br><br>

## Code

A clear, readable version:

```python
class Solution(object):
    def kidsWithCandies(self, candies, extraCandies):
        max_value = max(candies)          # the bar every kid tries to reach
        result = []

        for candy in candies:
            # can this kid reach or beat the bar with the extra candies?
            result.append(candy + extraCandies >= max_value)

        return result
```

The same logic written as a clean one-liner with list comprehension:

```python
class Solution(object):
    def kidsWithCandies(self, candies, extraCandies):
        max_value = max(candies)
        return [candy + extraCandies >= max_value for candy in candies]
```

<br><br>

## Dry Run

```ini
Input:
candies      = [2, 3, 5, 1, 3]
extraCandies = 3

Step 0: Find the bar (the max of candies)
    max_value = max([2, 3, 5, 1, 3]) = 5

result = []


Iteration 1  ->  kid 0
    candies[0]       = 2
    2 + extraCandies = 2 + 3 = 5
    Is 5 >= 5 (max)? YES
    result = [True]


Iteration 2  ->  kid 1
    candies[1]       = 3
    3 + extraCandies = 3 + 3 = 6
    Is 6 >= 5 (max)? YES
    result = [True, True]


Iteration 3  ->  kid 2
    candies[2]       = 5
    5 + extraCandies = 5 + 3 = 8
    Is 8 >= 5 (max)? YES
    result = [True, True, True]


Iteration 4  ->  kid 3
    candies[3]       = 1
    1 + extraCandies = 1 + 3 = 4
    Is 4 >= 5 (max)? NO
    result = [True, True, True, False]


Iteration 5  ->  kid 4
    candies[4]       = 3
    3 + extraCandies = 3 + 3 = 6
    Is 6 >= 5 (max)? YES
    result = [True, True, True, False, True]


Loop ends

Output:
result = [True, True, True, False, True]
```

<br><br>

## Complexity

- **Time:** O(n). One quick pass to find the max, then one pass to check every kid.
- **Space:** O(n) for the result array we hand back. If the output array is not counted, the extra space used is O(1).

A quick note on the brute force: comparing each kid against every other kid would cost O(n^2). Finding the max once first is what brings it down to a clean O(n).

<br><br>

## Related Problems

- [Richest Customer Wealth (1672)](https://leetcode.com/problems/richest-customer-wealth/)
- [Running Sum of 1d Array (1480)](https://leetcode.com/problems/running-sum-of-1d-array/)
- [How Many Numbers Are Smaller Than the Current Number (1365)](https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/)
- [Find the Highest Altitude (1732)](https://leetcode.com/problems/find-the-highest-altitude/)