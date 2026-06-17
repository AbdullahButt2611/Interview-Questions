## We’re given an array of interval pairs as input where each interval has a start and end timestamp. The input array is sorted by starting timestamps. Merge the overlapping intervals and return a new output array.
`Educative`

```python
class Interval:
  def __init__(self, first, second):
    self.first = first
    self.second = second

def merge_intervals(v):
  # write your code here
  if not v: return None
  result = []

  result.append(v[0])

  for i in range(1, len(v)):
      if v[i].first <= result[len(result) - 1].second:
          result[len(result) - 1].second = max(result[len(result) - 1].second, v[i].second)
      else:
          result.append(v[i])

  return result

def print_interval_list(lst):
    result_str = ""
    for i in range(len(lst)):
        result_str += "[" + str(lst[i].first) + \
            ", " + str(lst[i].second) + "], "
    return result_str[:-2]

v1 = [Interval(1, 5), Interval(4, 6), Interval(6, 8), Interval(11, 15)]
print(print_interval_list(merge_intervals(v1))) 
# Output: [1, 8], [11, 15]
```