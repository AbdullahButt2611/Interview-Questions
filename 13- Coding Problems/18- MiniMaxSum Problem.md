### Given five positive integers, find the minimum and maximum values that can be calculated by summing exactly four of the five integers. Then print the respective minimum and maximum values as a single line of two space-separated long integers.
`HackerRank`


```python

def miniMaxSum(arr):
    min_val = min(arr)
    max_val = max(arr)
    
    min_arr = arr.copy()
    max_arr = arr.copy()
    
    min_arr.remove(max_val)
    max_arr.remove(min_val)
    
    min_sum = sum(min_arr)
    max_sum = sum(max_arr)
    
    
    print(min_sum, max_sum)

```


#### Sample Input
A single line of five space-separated integers.
```
1 2 3 4 5
```

### Sample Output
Print two space-separated long integers denoting the respective minimum and maximum values that can be calculated by summing exactly four of the five integers. (The output can be greater than a 32 bit integer.)
```
10 14
```