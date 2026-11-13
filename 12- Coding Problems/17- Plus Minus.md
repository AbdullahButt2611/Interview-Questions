### Given an array of integers, calculate the ratios of its elements that are positive, negative, and zero. Print the decimal value of each fraction on a new line with  places after the decimal.

```python

def plusMinus(arr):
    if len(arr) == 0:
        print(0)
        print(0)
        print(0)
        return None
        
    positive, negative, zero = 0, 0, 0
    
    for num in arr:
        if num < 0:
            negative += 1
        elif num > 0:
            positive += 1
        else:
            zero += 1
    
    total = len(arr)
    print(positive/total)
    print(negative/total)
    print(zero/total)

```

### Input

```stdin
0 0 -1 1 1
```

### Output

```stdin
0.400000
0.200000
0.400000
```