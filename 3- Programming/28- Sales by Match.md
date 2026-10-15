# Sales by Match
#### There is a large pile of socks that must be paired by color. Given an array of integers representing the color of each sock, determine how many pairs of socks with matching colors there are.
`HackerRank`
<br><br>

```python
def sockMerchant(n, ar):
    count = 0
    combination = set()
    for element  in ar:
        if element in combination:
            combination.remove(element)
            count += 1
        else:
            combination.add(element)
    return count
```