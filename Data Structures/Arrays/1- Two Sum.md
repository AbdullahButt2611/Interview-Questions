### Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target. You may assume that each input would have *exactly one solution*, and you may not use the same element twice. You can return the answer in any order.

`LeetCode` `Arbisoft`

### Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

### Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

### Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]

### Constraints:
- 2 <= nums.length <= 104
- -109 <= nums[i] <= 109
- -109 <= target <= 109
- Only one valid answer exists.

### Follow up:
Can you come up with an algorithm that is less than `O(n2)` time complexity?

____

You can solve this problem using a hash table (dictionary in Python) to store the indices of the numbers as you iterate through the array. Here's the Python code to achieve this:

```python
def two_sum(nums, target):
    num_indices = {}  # Dictionary to store the indices of numbers

    # Iterate through the array
    for i, num in enumerate(nums):
        complement = target - num

        # Check if the complement exists in the dictionary
        if complement in num_indices:
            # Return the indices of the current number and its complement
            return [num_indices[complement], i]

        # Store the index of the current number in the dictionary
        num_indices[num] = i

    # If no solution is found, return an empty list
    return []

# Example usage:
nums1 = [2, 7, 11, 15]
target1 = 9
print(two_sum(nums1, target1))  # Output: [0, 1]

nums2 = [3, 2, 4]
target2 = 6
print(two_sum(nums2, target2))  # Output: [1, 2]
```
This solution has a time complexity of O(n) because the lookup time for an element in a dictionary is O(1), making the overall algorithm much more efficient than O(n^2).

### Explanation

- We define a function `two_sum(nums, target)` which takes in an array of integers `nums` and an integer `target`. This function will find and return the indices of the two numbers in the array that add up to the target.
- We initialize an empty dictionary called `num_indices`. This dictionary will be used to store the indices of the numbers as we iterate through the array.
- We use a `for` loop to iterate through the array `nums`. The `enumerate()` function is used to iterate through both the values and indices of the array simultaneously.
- Inside the loop, for each number `num` in the array, we calculate its complement by subtracting `num` from the `target`. The complement is the value that, when added to `num`, equals the `target`.
- We check if the complement exists in the `num_indices` dictionary. If it does, it means we have found the two numbers that add up to the target. In this case, we return the indices of the current number `num` (stored in `i`) and its complement (stored in `num_indices[complement]`).
- If the complement doesn't exist in the dictionary, we add the current number `num` to the `num_indices` dictionary with its index `i`. This allows us to look up the index of the complement in constant time during subsequent iterations.
- If no solution is found after iterating through the entire array, we return an empty list `[]`.
- Outside the function definition, we provide example usage of the `two_sum` function with two different arrays `nums1` and `nums2`, along with their respective target values `target1` and `target2`.
