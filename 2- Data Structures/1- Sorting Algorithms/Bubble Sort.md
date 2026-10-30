# Bubble Sort 

- Swap Consecutive Elements if first is less than second
- Worst case is `O(n^2)`

```pseudo
For i from 1 to N:
    For j from 0 to N-1:
        if a[j] > a[j+1]:
            swap(a[j], a[j+1])
```