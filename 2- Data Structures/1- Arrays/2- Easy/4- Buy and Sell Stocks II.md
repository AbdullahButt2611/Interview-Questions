# Best Time to Buy and Sell Stock (With Buy and Sell Day)

`Educative`
<br>

## Problem Statement

You are given an array `prices` where `prices[i]` is the price of a given stock on the `i`th day.

You want to maximize your profit by choosing a **single day** to buy one stock and choosing a **different day in the future** to sell that stock.

Return the **maximum profit**, along with the **index of the day to buy** and the **index of the day to sell**. If no profit can be achieved, return `0, None, None`.

> This is a follow-up variant of the classic [Best Time to Buy and Sell Stock](./best_time_to_buy_and_sell_stock.md) problem. The core logic is identical; the only addition is tracking and returning the indices of the optimal buy and sell days.

## Examples

**Example 1:**
```
Input:  prices = [7, 1, 5, 3, 6, 4]
Output: profit = 5, buy_day = 1, sell_day = 4
Explanation: Buy on day index 1 (price = 1) and sell on day index 4 (price = 6), profit = 6 - 1 = 5.
```

**Example 2:**
```
Input:  prices = [7, 6, 4, 3, 1]
Output: profit = 0, buy_day = None, sell_day = None
Explanation: Prices only decrease. No profitable transaction exists.
```

## Constraints

- `1 <= prices.length <= 10^5`
- `0 <= prices[i] <= 10^4`
- You must buy before you sell (buy index < sell index)

<br><br>

## Approach 1: Brute Force (Nested Loops)

**Intuition:**
Try every possible buy and sell pair. For each day `i` as the buy day, try selling on every future day `j > i`. Track the pair that yields the highest profit.

**Steps:**
1. Iterate over every index `i` as the buy day.
2. For each `i`, iterate over every `j > i` as the sell day.
3. Compute `profit = prices[j] - prices[i]`.
4. If this profit exceeds the current maximum, update `max_profit`, `buy_day`, and `sell_day`.
5. Return all three values.

```python
def max_profit(prices):
    if len(prices) < 2:
        return 0, None, None

    max_profit = 0
    buy_day = None
    sell_day = None

    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            profit = prices[j] - prices[i]
            if profit > max_profit:
                max_profit = profit
                buy_day = i
                sell_day = j

    return max_profit, buy_day, sell_day
```

**Complexity Analysis:**
| | |
|---|---|
| Time Complexity | O(n^2) - Two nested loops over the prices array |
| Space Complexity | O(1) - Only a fixed number of variables used |

**Problem with this approach:**

Every pair `(i, j)` is evaluated independently, even though the minimum price seen before day `j` never changes between inner iterations. We are redoing work that could be carried forward from the previous step. For `10^5` elements this means up to 5 billion comparisons, which will exceed time limits.

**Can we do better? Yes.** A single pass is enough if we track the minimum price and its index as we go.

<br><br>

## Approach 2: One Pass / Greedy (Optimal)

**Intuition:**
At any day `i`, the best profit we can make by selling that day is `prices[i] - min_price_so_far`. We scan left to right, keeping track of the minimum price seen and the index it occurred on. Whenever we find a better profit, we record the current index as the new sell day. The buy day is whichever index held the minimum price at that moment.

There is one subtlety worth noting: when we update `min_price` to a new lower value, we must also update `candidate_buy_day` to that new index. We only commit `candidate_buy_day` to the actual `buy_day` when we find a profit that beats the current best.

**Steps:**
1. Initialize `min_price = prices[0]`, `candidate_buy_day = 0`, `profit = 0`, `buy_day = None`, `sell_day = None`.
2. For each price from index `1` onward:
   - If `prices[i] < min_price`, update `min_price` and `candidate_buy_day = i`.
   - Else if `prices[i] - min_price > profit`, update `profit`, `buy_day = candidate_buy_day`, `sell_day = i`.
3. Return `profit, buy_day, sell_day`.

```python
def max_profit(prices):
    if len(prices) < 2:
        return 0, None, None

    min_price = prices[0]
    candidate_buy_day = 0
    profit = 0
    buy_day = None
    sell_day = None

    for i in range(1, len(prices)):
        if prices[i] < min_price:
            min_price = prices[i]
            candidate_buy_day = i
        elif prices[i] - min_price > profit:
            profit = prices[i] - min_price
            buy_day = candidate_buy_day
            sell_day = i

    return profit, buy_day, sell_day


# Example usage
prices = [7, 1, 5, 3, 6, 4]
profit, buy_day, sell_day = max_profit(prices)
print("Max profit:", profit)    # 5
print("Buy on day:", buy_day)   # 1
print("Sell on day:", sell_day) # 4
```

**Why `candidate_buy_day` and not just `buy_day` directly?**

When we spot a new minimum price, we do not yet know if a better sell day will come after it. We cannot commit to calling it the buy day until we actually find a profitable transaction that uses it. `candidate_buy_day` holds the "potential" buy day, and it gets promoted to `buy_day` only when a new best profit is confirmed.

**Walkthrough on Example 1:** `prices = [7, 1, 5, 3, 6, 4]`

| Day | Price | min_price | candidate_buy | Current Profit | Max Profit | buy_day | sell_day |
|-----|-------|-----------|---------------|----------------|------------|---------|----------|
| 0   | 7     | 7         | 0             | -              | 0          | None    | None     |
| 1   | 1     | 1         | 1             | -              | 0          | None    | None     |
| 2   | 5     | 1         | 1             | 5 - 1 = 4      | 4          | 1       | 2        |
| 3   | 3     | 1         | 1             | 3 - 1 = 2      | 4          | 1       | 2        |
| 4   | 6     | 1         | 1             | 6 - 1 = 5      | 5          | 1       | 4        |
| 5   | 4     | 1         | 1             | 4 - 1 = 3      | 5          | 1       | 4        |

Final Answer: `profit = 5, buy_day = 1, sell_day = 4`

**Walkthrough on Example 2:** `prices = [7, 6, 4, 3, 1]`

Prices only decrease. `min_price` keeps updating but `prices[i] - min_price` is always `0`, so the `elif` branch never fires. `buy_day` and `sell_day` remain `None`.

Final Answer: `profit = 0, buy_day = None, sell_day = None`

**Complexity Analysis:**
| | |
|---|---|
| Time Complexity | O(n) - Single pass through the array |
| Space Complexity | O(1) - Fixed number of variables regardless of input size |

<br><br>

## Summary

| Approach | Time Complexity | Space Complexity | Notes |
|---|---|---|---|
| Brute Force | O(n^2) | O(1) | TLE on large inputs |
| One Pass / Greedy | O(n) | O(1) | Optimal solution |

The one-pass greedy approach is the accepted optimal solution. The key addition over the base problem is maintaining a `candidate_buy_day` that tracks which index held the current minimum, and only promoting it to the confirmed `buy_day` when a better profit is found. This keeps the entire solution at O(n) time and O(1) space with no extra bookkeeping overhead.

<br><br>

## Why Is This Tagged Under Dynamic Programming?

At first glance this looks like a greedy scan, not a DP problem. But the same reasoning from the base problem applies here, and it is worth restating with the index-tracking twist in mind.

In our optimal solution, `min_price` and `candidate_buy_day` together represent the answer to a subproblem:

> "What is the cheapest price seen before today, and on which day did it occur?"

Every time we move to day `i`, we already know the answer to that subproblem from the previous iteration. We do not scan back through the array. We carry the answer forward. That is the essence of dynamic programming: **remembering past state to avoid redundant recomputation**.

```python
if prices[i] < min_price:
    min_price = prices[i]
    candidate_buy_day = i   # carry forward both the value and the index
```

Both variables together form the DP state. `min_price` encodes the optimal cost, and `candidate_buy_day` encodes where that cost was seen. Reusing this state at every step collapses the O(n^2) brute force into an O(n) solution.

The index-tracking version makes this even clearer than the base problem: we are not just remembering a number, we are remembering a decision (which day to buy) across iterations, which is precisely what DP does.