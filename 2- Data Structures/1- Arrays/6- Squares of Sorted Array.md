# Squares of Sorted Array
`Educative`

```python
def sorted_squares(nums):
    result = [None] * len(nums)  
    # TODO: Write your code here

    left = 0
    right = len(nums) - 1

    for i in range(len(result) - 1, -1, -1):
        if abs(nums[left]) < abs(nums[right]):
            result[i] = nums[right] * nums[right]
            right -= 1
        else: 
            result[i] = nums[left] * nums[left]
            left += 1
    return result

nums = [-4, -1, 0, 3, 10]
result = sorted_squares(nums)
print(result) # Output: [0, 1, 9, 16, 100]
```