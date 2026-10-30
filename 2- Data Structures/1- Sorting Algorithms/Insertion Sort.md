# Insertion Sort

### Working

- Works from left to right
- Examine each item and comapre items to the left
- Insert the item in the correct position

### Pseudo Code

```pseudo
for i => 1 - len(A) - 1:
    j = i
    while j > 0 and A[j-1] > A[j]:
        swap A[j] and A[j-1]
        j = j - 1
```

### Time Complexity

- O(n<sup>2</sup>)