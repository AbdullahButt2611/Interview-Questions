## We’re given a sorted integer array, nums and an integer value, target. The array is rotated by some arbitrary number. Search the target in this array. If the target does not exist then return -1.
`Educative`

## Sample input
```
nums = [6, 7, 1, 2, 3, 4, 5]
target = 3
```
## Expected output
```
4
```

## Solution
```python
def binary_search_rotated(nums, target):
    #TODO: Write - Your - Code
    low = 0
    high = len(nums) - 1

    if low > high:
        return -1
    
    while low <= high:
        mid = low + (high - low) // 2

        if nums[mid] == target : return mid

        if nums[low] <= nums[mid]:
            if nums[low] <= target and target < nums[mid]:
                high = mid - 1
            else:
                low = mid + 1
        else:
            if nums[mid] < target and target <= nums[high]:
                low = mid + 1
            else:
                high = mid - 1

    return -1


nums = [6, 7, 1, 2, 3, 4, 5]
target = 3
print(binary_search_rotated(nums, target))
```
