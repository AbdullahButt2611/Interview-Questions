# Number of Recent Calls
`LeetCode 75`

## Problem Statement

You are given a class named `RecentCounter` that counts how many requests happened in a recent time window.

Implement the `RecentCounter` class with the following rules:

* `RecentCounter()` starts with zero requests.
* `ping(t)` records a new request at time `t` (in milliseconds) and returns how many requests happened in the **last 3000 milliseconds**, including the current one.
* The time range to check is **[t - 3000, t]** (both ends included).
* Every call to `ping` has a **strictly increasing** value of `t`.

## Example

**Input**

```
["RecentCounter", "ping", "ping", "ping", "ping"]
[[], [1], [100], [3001], [3002]]
```

**Output**

```
[null, 1, 2, 3, 3]
```

**Explanation**

```
ping(1)     -> [1]                     -> range [-2999, 1]   -> 1
ping(100)   -> [1, 100]                -> range [-2900, 100] -> 2
ping(3001)  -> [1, 100, 3001]           -> range [1, 3001]   -> 3
ping(3002)  -> [1, 100, 3001, 3002]     -> range [2, 3002]   -> 3
```

<br><br>

## Approach 1: Simple List Check

### Idea

* Store all request times in a list.
* Every time `ping` is called:

  * Add the new time to the list.
  * Loop over the list and count times within `[t - 3000, t]`.

### Code

```python
class RecentCounter:

    def __init__(self):
        self.times = []

    def ping(self, t: int) -> int:
        self.times.append(t)
        count = 0
        for time in self.times:
            if time >= t - 3000:
                count += 1
        return count
```

### Explanation

This works because we directly check every stored request time and count valid ones.

### Problem with this approach

* Each `ping` may scan the full list.
* If there are many requests, this becomes slow.
* Time cost can grow to **O(n)** per call.

<br><br>

## Approach 2: Queue Based Sliding Window (Better)

### Idea

* Keep request times in a queue.
* When a new request comes:

  * Add it to the queue.
  * Remove requests from the front that are older than `t - 3000`.
* The queue size is the answer.

Because times always increase, old values stay at the front and can be removed easily.

### Code

```python
from collections import deque

class RecentCounter:

    def __init__(self):
        self.q = deque()

    def ping(self, t: int) -> int:
        self.q.append(t)
        while self.q[0] < t - 3000:
            self.q.popleft()
        return len(self.q)
```

### Explanation

* Each request time is added once.
* Each request time is removed once.
* No extra scanning is needed.

### Why this is better

* Each `ping` runs in **O(1)** average time.
* Works well even with a large number of requests.

<br><br>

## Final Notes

* The queue method is the best choice for interviews.
* It is simple, fast, and easy to explain.
* The increasing order of `t` makes this method possible and safe.
