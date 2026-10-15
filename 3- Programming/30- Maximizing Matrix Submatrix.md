## Maximizing Matrix Submatrix
#### Sean invented a game involving 2n x 2n matrix where each cell of the matrix contains an integer. He can reverse any of it's row and  columns any number of times. The Goal of the game is to maximize the sum of elements in n x n submatrix located in the upper left quadrant of the matrix.
#### Given initial configurations for q matrices, help Sean reverse the rows and columns of each matrix in the best possible way so that the sum of the elements in the matrix's upper left quadrant is maximal

`HackerRank`
<br><br>

```python
def maximize_upper_left_sum(matrix):
    n = len(matrix) // 2  # Since the matrix is 2n x 2n
    max_sum = 0
    
    for i in range(n):
        for j in range(n):
            # Get the values from the four quadrants
            val1 = matrix[i][j]                # Q1
            val2 = matrix[i][2 * n - j - 1]    # Q2
            val3 = matrix[2 * n - i - 1][j]    # Q3
            val4 = matrix[2 * n - i - 1][2 * n - j - 1]  # Q4
            
            # Take the maximum value
            max_sum += max(val1, val2, val3, val4)

    return max_sum

# Example usage
matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]

maximize_upper_left_sum(matrix)
```
