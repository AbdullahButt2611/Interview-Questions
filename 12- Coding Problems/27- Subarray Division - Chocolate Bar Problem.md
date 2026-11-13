## Subarray Division - Chocolate Bar Problem
##### Two children, Lily and Ron, want to share a chocolate bar. Each of the squares has an integer on it. Lily decides to share a contiguous segment of the bar selected such that: The length of the segment matches Ron's birth month, and, The sum of the integers on the squares is equal to his birth day. Determine how many ways she can divide the chocolate.

`HackerRank`
<br><br>

## Brute Force Solution
```python
def birthday(s, d, m):
    no_of_ways = 0
    for i in range(len(s)):
        if i+m <= len(s):
            if sum(s[i: i+m]) == d:
                no_of_ways += 1
    return no_of_ways
```
<br><br>

## Sliding Window Solution
```python
def birthday(s, d, m):
    n = len(s)
    count = 0
    
    window_sum = sum(s[:m])
    if window_sum == d:
        count += 1
        
    for i in range(m, n):
        window_sum += s[i] - s[i - m]
        if window_sum == d:
            count += 1
    return count
```

