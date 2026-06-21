# Kadane's Algorithm

A simple and fast way to find the group of numbers sitting next to each other that adds up to the biggest total. It walks through the list only once and uses almost no extra memory.

## What It Is

You have a list of numbers. Some are positive and some can be negative. You want to find a group of numbers that sit next to each other (with no gaps) whose total is as large as possible. Kadane's algorithm finds that biggest total.

```
Input:   [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output:  6          # the run [4, -1, 2, 1] adds up to 6
```

The word **subarray** just means numbers in a row, with no skipping. You cannot jump around and pick numbers from different spots.

The slow way is to try every possible run, add each one up, and keep the biggest. That works, but it is slow because there are too many runs to check. Kadane's is fast because it goes through the list only one time.

## Core Idea

Think of a road trip. Each number is a town. A positive number means you earn money there, and a negative number means you lose money. You want the best stretch of the trip, the part where you came out ahead the most.

Walk through the numbers one at a time and keep a **running total** for your current stretch. At each new number, ask one simple question: *is my running total still helping me?*

- If the running total is still positive, keep it and add the new number to it.
- If the running total has dropped below zero, throw it away and start fresh from the new number. A negative total can only drag you down.

In code, that one decision looks like this:

```
current = max(x, current + x)
```

It means: either start a new run at `x`, or continue the old run by adding `x`, and just keep whichever is bigger.

While you do this, also remember the **best total** you have reached at any point. That best total is your answer. You keep checking it because the winning stretch can end anywhere in the list, not only at the very end.

<br>

## Be Careful With the Starting Value

Start both your current total and your best total at the **first number**, then begin checking from the second number onward.

Do not start the best total at `0`. Here is why. If every number is negative, like `[-3, -1, -2]`, the best you can do is pick the number closest to zero, which is `-1`. If you started at `0`, the code would wrongly say the answer is `0` (an empty pick). Starting at the first number avoids this. This is the mistake people make most often.

## When To Use It

- You want the biggest total from numbers that sit next to each other
- The list has negative numbers, so you cannot simply add everything up
- You want it fast (one pass) and with almost no extra memory
- The question sounds like "best run", "largest total in a row", or "most profit over a stretch"

Do not use it when you are allowed to skip numbers (that is a different kind of problem), or when you multiply numbers instead of adding them (see Variations).

<br>

## Template Code (Python)

```python
def max_subarray(nums):
    best = current = nums[0]          # start both at the first number
    for x in nums[1:]:                # then go through the rest, one by one
        current = max(x, current + x) # extend the run, or start fresh
        best = max(best, current)     # remember the biggest total so far
    return best
```

## Step-by-Step Walkthrough

Let us go through `[-2, 1, -3, 4, -1, 2, 1, -5, 4]` slowly.

| Number | current = max(number, current + number) | current | best |
|---|---|---|---|
| `-2` | start here | -2 | -2 |
| `1` | bigger of 1 and -1 | 1 | 1 |
| `-3` | bigger of -3 and -2 | -2 | 1 |
| `4` | bigger of 4 and 2 | 4 | 4 |
| `-1` | bigger of -1 and 3 | 3 | 4 |
| `2` | bigger of 2 and 5 | 5 | 5 |
| `1` | bigger of 1 and 6 | 6 | 6 |
| `-5` | bigger of -5 and 1 | 1 | 6 |
| `4` | bigger of 4 and 5 | 5 | 6 |

In plain words: the early negative numbers drag the total down, so we reset and start fresh at `4`. From there the run grows up to `6`, dips a little, but `6` stays the best total we ever saw. So the answer is `6`.

## Complexity

Big-O is just a short way to describe how the speed and memory grow as the list gets bigger.

| Approach | Time | Space |
|---|---|---|
| Kadane (one pass) | `O(n)` | `O(1)` |
| Brute force (check every run) | `O(n^2)` | `O(1)` |

We look at each number exactly once, so the time is `O(n)`, meaning the work grows in step with the size of the list. We only keep two values (current and best), so the extra memory is `O(1)`, meaning it stays the same no matter how big the list gets. The brute force way rechecks every possible run, which is much slower.

<br>

## Variations

### Get the actual numbers, not just the total

Sometimes you also want to know **which** numbers made the best run. To do that, remember where the current run started, and write down the start and end whenever you beat your best total.

```python
def max_subarray_with_indices(nums):
    best = current = nums[0]
    start = end = temp_start = 0
    for i in range(1, len(nums)):
        if nums[i] > current + nums[i]:   # starting fresh is better
            current = nums[i]
            temp_start = i
        else:                             # extending is better
            current += nums[i]
        if current > best:                # new best, save the spot
            best = current
            start, end = temp_start, i
    return best, nums[start:end + 1]
```

<br>

### When you multiply instead of add (biggest product)

If the goal is the biggest **product** (numbers multiplied together), the simple version breaks. Why? Two negatives multiply into a positive, so a very negative total can suddenly turn into the biggest one. The fix is to track both the biggest and the smallest running product, and swap them whenever you hit a negative number (LeetCode 152).

```python
def max_product(nums):
    best = cur_max = cur_min = nums[0]
    for x in nums[1:]:
        if x < 0:                       # a negative flips big and small
            cur_max, cur_min = cur_min, cur_max
        cur_max = max(x, cur_max * x)
        cur_min = min(x, cur_min * x)
        best = max(best, cur_max)
    return best
```

<br>

### When the list wraps around in a circle

Some problems let the run wrap from the end of the list back to the start. The trick: the answer is either a normal best run, or the whole total minus the **worst** run in the middle (which leaves the wrapped-around part). Be careful when every number is negative (LeetCode 918).

<br>

### Finding the best rectangle in a grid (2D)

You can stretch the same idea to a grid of numbers. Pick a left column and a right column, squash the rows between them into a single column of sums, then run Kadane's on that column. Doing this for every pair of columns finds the rectangle with the biggest total (LeetCode 363).

<br>

## Variations at a Glance

| Variation | Best For | Time |
|---|---|---|
| Kadane (biggest sum) | Largest total in a row | `O(n)` |
| Kadane with positions | Getting the actual numbers back | `O(n)` |
| Biggest product | Numbers multiplied, with negatives | `O(n)` |
| Circular version | Lists that wrap around | `O(n)` |
| 2D grid version | Biggest-total rectangle in a grid | `O(rows * cols^2)` |

<br>

## Common Pitfalls (Easy Mistakes)

- Starting the best total at `0`. This breaks when every number is negative. Start at the first number instead.
- Mixing up "in a row" with "skipping allowed". Kadane's only works for numbers that sit next to each other.
- Using the plain version for multiplication. For products you must also track the smallest running value.
- Forgetting the all-negative case in the circular version.
- Getting the start position wrong when you try to return the actual numbers, not just the total.

<br>

## Practice Problems (LeetCode)

The key skill is spotting that a problem is really a "best run of numbers in a row" question. No solutions here, just the list, ordered Easy to Hard.

### Easy

- Maximum Subarray (LeetCode 53)

### Medium

- Maximum Product Subarray (LeetCode 152)
- Maximum Sum Circular Subarray (LeetCode 918)
- Maximum Absolute Sum of Any Subarray (LeetCode 1749)

### Hard

- Max Sum of Rectangle No Larger Than K (LeetCode 363)