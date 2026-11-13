# Diagonal Difference Problem
### Given a square matrix, calculate the absolute difference between the sums of its diagonals.

`HackerRank`

<br>

```python
def diagonalDifference(arr):
    rows = len(arr)
    left_diagonal = 0
    right_diagonal = 0
    
    for i in range(0, rows):
        left_diagonal += arr[i][i]
        right_diagonal += arr[i][rows - i - 1]
    
    return abs(left_diagonal - right_diagonal)
```