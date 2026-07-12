# Lower Bound of an Element in Sorted Array

`Amazon` • `Google` • `Microsoft` • `Adobe` • `Apple` • `Bloomberg` • `Meta` • `Uber` • `LinkedIn` • `TCS`

<br>

## Question

What is the **lower bound** of an element in a sorted array, and how do you find it efficiently?

<br><br>

## Answer

### 1. What Lower Bound Means

**Lower bound is the index of the first element that is greater than or equal to the target.**

<mark>Lower bound gives you a POSITION, not a value. It answers "where does this number belong?", not "does this number exist?".</mark>

Look at one example and the idea becomes clear.

```
Index :   0   1   2   3    4
Array :   3   5   8   15   19

Target = 9
First element >= 9 is 15, sitting at index 3

Lower bound = 3
```

<br><br>

### 2. The Only Three Cases You Need to Remember

- **Target is present** → returns the index of its **first occurrence**
- **Target is absent** → returns the index of the **next greater element** (the spot where it would be inserted)
- **All elements are smaller** → returns **n**, the size of the array (it belongs at the very end)

```ini
arr = [1, 3, 3, 5, 8]

lower_bound(3)  -> 1   (present, first occurrence)
lower_bound(4)  -> 3   (absent, next greater is 5 at index 3)
lower_bound(9)  -> 5   (all smaller, so answer is n = 5)
```

<br><br>

### 3. The Idea Behind the Solution

The array is **sorted**, and that gives us one powerful rule at any middle index `mid`:

- If `arr[mid] >= x` → `mid` is a **valid answer**, but a smaller index might also work, so **look left**
- If `arr[mid] < x` → `mid` and everything before it are **too small**, so **look right**

This lets us throw away half the array in every step, which is just **binary search**.

<mark>The one trick: when we find a valid element, we do NOT stop. We save it and keep searching left, because we want the FIRST valid index, not just any valid index.</mark>

<br><br>

### 4. Code

```python
class LowerBoundFinder:
    # Function to find the lower bound index using binary search
    def lower_bound(self, arr, x):
        low, high = 0, len(arr) - 1     # Search range
        ans = len(arr)                  # Default value if not found
        while low <= high:
            mid = (low + high) // 2     # Find middle index
            if arr[mid] >= x:
                ans = mid               # Store possible answer
                high = mid - 1          # Move to the left
            else:
                low = mid + 1           # Move to the right
        return ans                      # Return result

# Driver code
arr = [3, 5, 8, 15, 19]                # Sorted input array
x = 9                                  # Target value
finder = LowerBoundFinder()            # Create object
ind = finder.lower_bound(arr, x)       # Call method
print("The lower bound is the index:", ind)  # Output result
```

`ans` starts at `len(arr)` on purpose. If no element is ever found to be `>= x`, that default is already the correct answer.

<br><br>

### 5. Dry Run

Input: `arr = [3, 5, 8, 15, 19]`, `x = 9`

```ini
Start: low = 0, high = 4, ans = 5

Step 1:
  mid = (0 + 4) // 2 = 2
  arr[2] = 8  ->  Is 8 >= 9 ?  NO
  Too small, so move right
  low = 3        (low = 3, high = 4, ans = 5)

Step 2:
  mid = (3 + 4) // 2 = 3
  arr[3] = 15 ->  Is 15 >= 9 ?  YES
  Valid, so save it and keep looking left
  ans = 3
  high = 2       (low = 3, high = 2, ans = 3)

Step 3:
  low (3) > high (2)  ->  loop ends

Answer = 3
```

<br><br>

### 6. Complexity

- **Time:** `O(log n)`, the search space halves every step
- **Space:** `O(1)`, only a few variables are used