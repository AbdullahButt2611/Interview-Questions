# Best Time to Buy and Sell Stock

`Amazon` • `Google` • `Meta` • `Microsoft` • `Apple` • `Bloomberg` • `Adobe` • `Uber` • `Goldman Sachs` • `Yelp`
<br>

## Problem Statement

You are given an array `prices` where `prices[i]` is the price of a given stock on the `i`th day.

You want to maximize your profit by choosing a **single day** to buy one stock and choosing a **different day in the future** to sell that stock.

Return the **maximum profit** you can achieve from this transaction. If you cannot achieve any profit, return `0`.

## Examples

**Example 1:**
```
Input:  prices = [7, 1, 5, 3, 6, 4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6 - 1 = 5.
             Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.
```

**Example 2:**
```
Input:  prices = [7, 6, 4, 3, 1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.
```

## Constraints

- `1 <= prices.length <= 10^5`
- `0 <= prices[i] <= 10^4`

<br><br>

## Approach 1: Brute Force (Nested Loops)

**Intuition:**
The simplest way to solve this is to check every possible pair of buy and sell days. For each day `i`, try selling on every future day `j > i`, compute the profit, and keep track of the maximum.

**Steps:**
1. Iterate over every index `i` as the buy day.
2. For each `i`, iterate over every index `j > i` as the sell day.
3. Compute `profit = prices[j] - prices[i]`.
4. Track the maximum profit seen so far.
5. Return the maximum profit (or `0` if it is never positive).

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_profit = 0

        for i in range(len(prices)):
            for j in range(i + 1, len(prices)):
                profit = prices[j] - prices[i]
                max_profit = max(max_profit, profit)

        return max_profit
```

**Complexity Analysis:**
| | |
|---|---|
| Time Complexity | O(n^2) - Two nested loops, each up to n iterations |
| Space Complexity | O(1) - No extra data structures used |

**Problem with this approach:**

For large inputs (up to `10^5` elements), an O(n^2) solution performs up to 10 billion operations, which will exceed the time limit. The nested loop redundantly recomputes profits for the same pairs. We are not leveraging the fact that the minimum buy price seen so far is all we need to track at any given point.

**Can we do better? Yes.** Instead of comparing every pair, we can make a single pass through the array.

<br><br>

## Approach 2: One Pass / Greedy (Optimal)

**Intuition:**
At any point in the array, the best profit we can make by selling on day `i` is `prices[i] - min_price_so_far`. So we scan left to right, maintaining the minimum price seen so far and updating the maximum profit whenever we find a better selling point.

We never need to look back. If we are at day `i`, the optimal buy day is simply the day with the lowest price in the range `[0, i-1]`.

**Steps:**
1. Initialize `min_price` to the first element and `profit` to `0`.
2. For each price from day 1 onward:
   - Compute `current_profit = prices[i] - min_price`.
   - Update `profit = max(profit, current_profit)`.
   - Update `min_price = min(min_price, prices[i])`.
3. Return `profit`.

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_price = prices[0]
        profit = 0

        for i in range(1, len(prices)):
            ith_profit = prices[i] - min_price
            profit = max(profit, ith_profit)
            min_price = min(min_price, prices[i])

        return profit
```

**Walkthrough on Example 1:** `prices = [7, 1, 5, 3, 6, 4]`

| Day | Price | min_price | Current Profit | Max Profit |
|-----|-------|-----------|----------------|------------|
| 0   | 7     | 7         | -              | 0          |
| 1   | 1     | 1         | 1 - 7 = -6     | 0          |
| 2   | 5     | 1         | 5 - 1 = 4      | 4          |
| 3   | 3     | 1         | 3 - 1 = 2      | 4          |
| 4   | 6     | 1         | 6 - 1 = 5      | 5          |
| 5   | 4     | 1         | 4 - 1 = 3      | 5          |

Final Answer: `5`

**Walkthrough on Example 2:** `prices = [7, 6, 4, 3, 1]`

The price only decreases. `min_price` keeps updating downward and `current_profit` is always negative, so `max_profit` stays `0`.

Final Answer: `0`

**Complexity Analysis:**
| | |
|---|---|
| Time Complexity | O(n) - Single pass through the array |
| Space Complexity | O(1) - Only two variables used regardless of input size |

<br><br>

## Summary

| Approach | Time Complexity | Space Complexity | Notes |
|---|---|---|---|
| Brute Force | O(n^2) | O(1) | TLE on large inputs |
| One Pass / Greedy | O(n) | O(1) | Optimal solution |

The one-pass greedy approach is the accepted optimal solution. The key insight is that to maximize profit on any given sell day, you only need to know the minimum price seen before that day. Tracking this minimum as you iterate eliminates the need for a second loop entirely.

<br><br>

## Why Is This Tagged Under Dynamic Programming?

At first glance, this problem looks like a simple greedy scan and does not involve any DP table, memoization array, or recurrence relation in the classical sense. So why do platforms like LeetCode tag it under Dynamic Programming?

The answer lies in the **core idea behind DP: using previously computed information to make the current decision**, rather than recomputing it from scratch.

In our optimal solution, `min_price` is not just a running variable. It represents the answer to the subproblem:

> "What is the cheapest price I could have bought the stock on any day before today?"

Every time we move to day `i`, we already know the answer to that subproblem from the previous iteration. We do not scan back through the array to find the minimum again. We carry it forward. That is the essence of dynamic programming: **remembering the past to avoid redundant work**.

```python
min_price = min(min_price, prices[i])  # carry forward the best buy price seen so far
```

This single line is the DP state update. `min_price` encodes the optimal decision from all previous days, and we reuse it directly at each step.

**Contrast this with the brute force approach:** it does not remember anything. For every sell day `j`, it re-examines every possible buy day `i < j` from scratch, which is why it costs O(n^2). The DP insight collapses that into O(n) by keeping just one value in memory.

So while this problem does not look like a DP problem in the textbook sense (no 2D table, no recursion), the underlying pattern is absolutely DP: **optimal substructure** (the best buy day for any prefix is independent of what comes after) and **overlapping subproblems** (every sell day needs the same "minimum so far" answer that the previous step already computed).