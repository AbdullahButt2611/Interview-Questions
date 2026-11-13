### There is a collection of input strings and a collection of query strings. For each query string, determine how many times it occurs in the list of input strings. Return an array of the results.

`HackerRank`


## Method 01:
Time Complexity = O(n * m):

```python
def matchingStrings(strings, queries):
    return [strings.count(query) for query in queries]
```


## Method 02:
Time Complexity = O(n + m):

```python
def matchingStrings(strings, queries):
    result_count = {}
    
    for string in strings:
        if string in result_count:
            result_count[string] += 1
        else:
            result_count[string] = 1
    
    result = []
    for query in queries:
        result.append(result_count.get(query, 0))
    
    return result
```