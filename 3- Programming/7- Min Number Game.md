## You are given a 0-indexed integer array nums of even length and there is also an empty array arr. Alice and Bob decided to play a game where in every round Alice and Bob will do one move. The rules of the game are as follows:
> - Every round, first Alice will remove the minimum element from nums, and then Bob does the same.
> - Now, first Bob will append the removed element in the array arr, and then Alice does the same.
> - The game continues until nums becomes empty.

> Return the resulting array arr.

`Educative`

```python
def min_operations(nums):
    arr = []

    while nums:
        # Using slicing to efficiently remove the first two elements
        alice_value, bob_value = nums[:2]
        nums = nums[2:]

        # Appending values to the result array in the desired order
        arr.append(bob_value)
        arr.append(alice_value)

    return arr

nums = [3, 1, 2, 4]
print(min_operations(nums))
```