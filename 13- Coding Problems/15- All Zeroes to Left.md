## We’re given an integer array, nums. Move all zeroes, if any, to the left while maintaining the order of other elements in the array. All changes must be made in nums itself; no return value is expected.

`Educative`

```python
def move_zeros_to_left(nums):
  #TODO: Write - Your - Code
  left = len(nums) - 1
    right = len(nums) - 1

    while right >= 0:
        if nums[right] != 0:
            nums[left],nums[right] = nums[right], nums[left]
            left -= 1
        right -= 1
  pass
```