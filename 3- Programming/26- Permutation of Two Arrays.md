## Permute two arrays such that sum of every pair is greater or equal to K
#### Given two arrays of equal size n and an integer k. The task is to permute both arrays such that sum of their corresponding element is greater than or equal to k i.e a[i] + b[i] >= k. The task is to print “Yes” if any such permutation exists, otherwise print “No”.

`HackerRank`

## Solution

```python
def twoArrays(k, A, B):
    A.sort()
    B.sort(reverse=True)
    
    for i in range(len(A)):
        if A[i] + B[i] < k:
            return "NO" 
    return "YES"
```