# Two Sum

`Arbisoft` • `Amazon` • `Google` • `Microsoft` • `Meta` • `Apple` • `Netflix` • `Adobe` • `Bloomberg` • `Airbnb`
<br>

## Problem Statement

Given an array of integers `nums` and an integer `target`, return the indices of the two numbers such that they add up to `target`. You may assume that each input would have **exactly one solution**, and you may not use the same element twice. You can return the answer in any order.

## Examples

**Example 1:**
```
Input:  nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
Explanation: nums[0] + nums[1] == 9, so we return [0, 1].
```

**Example 2:**
```
Input:  nums = [3, 2, 4], target = 6
Output: [1, 2]
```

**Example 3:**
```
Input:  nums = [3, 3], target = 6
Output: [0, 1]
```

## Constraints

- `2 <= nums.length <= 10^4`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`
- Only one valid answer exists.

## Follow-up

Can you come up with an algorithm that has less than `O(n²)` time complexity?

<br><br>

## Approach 1 - Brute Force

**The idea:** Check every possible pair of numbers in the array and see if they add up to `target`. We do this using two nested loops - the outer loop picks the first number, and the inner loop checks every number that comes after it.

```python
def two_sum(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


# Example usage
print(two_sum([2, 7, 11, 15], 9))   # Output: [0, 1]
print(two_sum([3, 2, 4], 6))        # Output: [1, 2]
```

**Explanation:**
- The outer loop fixes one element at index `i`.
- The inner loop tries every element at index `j` that comes after `i`, ensuring we never reuse the same element.
- If the two elements sum to `target`, we return their indices immediately.

**Complexity:**

| | |
|---|---|
| Time | `O(n²)` - for every element we scan all remaining elements |
| Space | `O(1)` - no extra data structure used |

<br>

**What is the problem?**

For every single element, we are scanning the rest of the array again from scratch. This means if the array has 10,000 elements, we could end up doing close to 100,000,000 comparisons in the worst case. This is far too slow for large inputs. The follow-up explicitly asks us to do better than `O(n²)`.

**Can we do better?** Yes. Instead of re-scanning the array for a complement each time, we can store what we have already seen and look it up instantly.

<br><br>

## Approach 2 - Hash Map (One Pass)

**The idea:** As we iterate through the array, we store each number and its index in a hash map. Before storing a number, we first check if its complement (`target - num`) is already in the map. If it is, we have found our pair and return immediately. This way, we only need a single pass through the array.

```python
def two_sum(nums, target):
    num_indices = {}  # { number: index }

    for i, num in enumerate(nums):
        complement = target - num

        if complement in num_indices:
            return [num_indices[complement], i]

        num_indices[num] = i

    return []


# Example usage
print(two_sum([2, 7, 11, 15], 9))   # Output: [0, 1]
print(two_sum([3, 2, 4], 6))        # Output: [1, 2]
print(two_sum([3, 3], 6))           # Output: [0, 1]
```

**Explanation:**
- We initialize an empty dictionary `num_indices` that maps a number to its index in the array.
- On each iteration, we calculate `complement = target - num`. This is the value we need to have already seen in order to form a valid pair.
- We check if `complement` exists in `num_indices`. If it does, the pair is `(num_indices[complement], i)` and we return immediately.
- If it does not exist, we store `num` with its index `i` in the map and move on.
- Hash map lookups and insertions are both `O(1)` on average, so the entire pass runs in linear time.

**Complexity:**

| | |
|---|---|
| Time | `O(n)` - single pass; each lookup and insert is `O(1)` |
| Space | `O(n)` - hash map stores at most `n` entries |

<br>

**Why is this the optimal solution?**

We cannot do better than `O(n)` time because we must look at every element at least once to guarantee we find the pair. The hash map approach achieves exactly that - one pass, constant-time lookups - making it both time-optimal and straightforward to implement. This is the solution you should reach for in an interview.

**What if the interviewer says no hash map?** If you are explicitly told not to use any extra space or hash-based data structure, the two-pointer technique is the right answer. See Approach 3 below.

<br><br>

## Approach 3 - Two Pointers (No Hash Map)

> **When to use this:** Only bring this up if the interviewer explicitly restricts you from using a hash map or any extra space. This approach requires sorting the array first, which means we lose the original indices. We handle that by saving them before sorting.

**The idea:** Sort the array by value while keeping track of the original indices. Then place one pointer at the start (`left`) and one at the end (`right`) of the sorted array. If the sum of the two pointed values equals `target`, we return their original indices. If the sum is too small, move `left` forward to get a larger value. If the sum is too large, move `right` backward to get a smaller value. Repeat until the pointers meet.

```python
def two_sum(nums, target):
    # Pair each number with its original index, then sort by value
    sorted_nums = sorted(enumerate(nums), key=lambda x: x[1])

    left, right = 0, len(sorted_nums) - 1

    while left < right:
        left_idx, left_val = sorted_nums[left]
        right_idx, right_val = sorted_nums[right]
        current_sum = left_val + right_val

        if current_sum == target:
            return [left_idx, right_idx]
        elif current_sum < target:
            left += 1
        else:
            right -= 1

    return []


# Example usage
print(two_sum([2, 7, 11, 15], 9))   # Output: [0, 1]
print(two_sum([3, 2, 4], 6))        # Output: [1, 2]
print(two_sum([3, 3], 6))           # Output: [0, 1]
```

**Explanation:**
- We use `enumerate(nums)` to pair every value with its original index before sorting, so we do not lose track of where each number came from.
- `sorted_nums` is sorted in ascending order by value. The two pointers start at opposite ends of this sorted array.
- On each step, we compute the sum of the values at `left` and `right`.
- If the sum equals `target`, we return the original indices stored alongside the values.
- If the sum is less than `target`, we need a bigger value, so we move `left` one step right.
- If the sum is greater than `target`, we need a smaller value, so we move `right` one step left.
- Because the array is sorted, this is guaranteed to find the pair without any extra hash-based storage.

**Complexity:**

| | |
|---|---|
| Time | `O(n log n)` - dominated by the sort; the two-pointer scan itself is `O(n)` |
| Space | `O(n)` - we store the `(original_index, value)` pairs in `sorted_nums` |

<br>

**Trade-off vs Approach 2**

This approach is slightly worse in time (`O(n log n)` vs `O(n)`) and does not actually save space since we still need the paired array. Its only advantage is that it avoids a hash map entirely, which is the one scenario where an interviewer would ask for it. If there are no restrictions, always prefer Approach 2.