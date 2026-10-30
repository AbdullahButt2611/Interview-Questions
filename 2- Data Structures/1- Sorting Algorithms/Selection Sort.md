# Selection Sort

- During each iteration we'll select the smallest item from unsorted partition and move it to the sorted partition

### Pseudo Code

```pseudo
for(j = 0, j < n-1 , j++):
    iMin = j
    for(i = j+1, i < n, i++):
        if A[i] > A[iMin]:
            iMin = i
    
    if iMin != j:
        swap(A[j], A[iMin])
```

### Time Complexity

- O(n<sup>2</sup>)