# Return the triplet whose sum is maximum in the array
`Educative`

### Brute Force Solution

```python
def max_trip(arr):
    n = len(arr)
    max = 0
    triplet = None

    for i in range(n-2):
        for j in range(i+1, n-1):
            for k in range(j+1, n):
                if arr[i] + arr[j] + arr[k] > max:
                    max = arr[i] + arr[j] + arr[k]
                    triplet = (arr[i] , arr[j] , arr[k])
    
    return triplet

height = [1,8,6,2,5,4,8,3,7]
print(max_trip(height))
```

## Optimization


