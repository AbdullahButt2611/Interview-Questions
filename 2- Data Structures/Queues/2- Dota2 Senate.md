# Dota2 Senate
`LeetCode 75`

## Problem Statement

In the world of Dota2, there are two parties:

* **Radiant** (`R`)
* **Dire** (`D`)

The Dota2 senate consists of senators from these two parties. The senate votes on a game change using a **round-based** process.

### Rules of Voting

In each round, a senator who still has voting rights can perform **one** of the following actions:

1. **Ban a senator**: Remove another senator’s voting rights for the current and all future rounds.
2. **Announce victory**: If all remaining senators with voting rights belong to the same party, that party wins.

### Process Details

* Senators act from **left to right** based on the given order.
* Senators who have lost their rights are skipped.
* All senators play optimally to help their own party win.

### Input

* A string `senate` of length `n`
* Each character is either `R` (Radiant) or `D` (Dire)

### Output

* Return **"Radiant"** or **"Dire"**, depending on which party wins.

### Example 1

```
Input:  "RD"
Output: "Radiant"
```

### Example 2

```
Input:  "RDD"
Output: "Dire"
```

<br><br>

## Approach 1: Direct Simulation (Inefficient)

### Idea

Simulate the rounds exactly as described:

* Track which senators are banned
* For each active senator, ban the next available opponent
* Repeat rounds until only one party remains

### Problem with This Approach

* Finding the next valid opponent is costly
* Many repeated scans of the list
* Time grows very fast for large inputs

### Complexity

* **Time:** O(n²)
* **Space:** O(n)

This approach works for small cases but fails for large ones.

<br><br>

## Approach 2: Queue-Based Solution (Optimal)

### Key Insight

Instead of simulating bans directly, track **when** each senator gets a turn.

* Store the positions of Radiant senators in one queue
* Store the positions of Dire senators in another queue
* Compare the front of both queues

The senator with the smaller index acts first and bans the other.

The winner returns to the queue with position increased by `n`, meaning they act again in the next round.

This models the rounds without extra scans.

## Algorithm Steps

1. Create two queues: `radiant`, `dire`
2. Store indices of `R` and `D` senators
3. While both queues are not empty:

   * Pop one index from each queue
   * The smaller index bans the other
   * The winner goes back with index + `n`
4. The party with remaining senators wins

## Python Solution

```python
from collections import deque

class Solution:
    def predictPartyVictory(self, senate: str) -> str:
        n = len(senate)
        radiant = deque()
        dire = deque()

        for i, s in enumerate(senate):
            if s == 'R':
                radiant.append(i)
            else:
                dire.append(i)

        while radiant and dire:
            r = radiant.popleft()
            d = dire.popleft()

            if r < d:
                radiant.append(r + n)
            else:
                dire.append(d + n)

        return "Radiant" if radiant else "Dire"
```

## Why This Works

* Order of turns is preserved
* Banned senators never re-enter
* Each senator is processed once per round

## Complexity Analysis

* **Time Complexity:** O(n)
* **Space Complexity:** O(n)

This is the best possible solution for this problem and works within all limits.

<br><br>

## Summary

* Direct simulation is slow and not scalable
* Queue-based indexing solves the problem cleanly
* This method matches optimal play automatically

This solution is suitable for interviews and competitive coding.
