# Upper Bound of an Element in Sorted Array

`Amazon` • `Google` • `Microsoft` • `Adobe` • `Apple` • `Bloomberg` • `Meta` • `Uber` • `LinkedIn` • `Oracle`

<br>

## Question

What is the **upper bound** of an element in a sorted array, and how do you find it efficiently?

<br><br>

## Answer

### 1. What Upper Bound Means

**Upper bound is the index of the first element that is strictly greater than the target.**

<mark>The word "strictly" is the whole point. Equal elements do NOT count, only elements bigger than the target do.</mark>

Look at one example and the idea becomes clear.

```
Index :   0   1   2   3    4
Array :   3   5   8   15   19

Target = 8
First element > 8 is 15, sitting at index 3

Upper bound = 3
```

<br><br>

### 2. The Only Three Cases You Need to Remember

- **Target is present** → returns the index **just after its last occurrence**
- **Target is absent** → returns the index of the **next greater element**
- **No element is greater** → returns **n**, the size of the array

```ini
arr = [1, 3, 3, 5, 8]

upper_bound(3)  -> 3   (present, last 3 is at index 2, so first element > 3 is 5 at index 3)
upper_bound(4)  -> 3   (absent, next greater is 5 at index 3)
upper_bound(8)  -> 5   (nothing is greater than 8, so answer is n = 5)
```

<br><br>

### 3. The Idea Behind the Solution

The array is **sorted**, and that gives us one rule at any middle index `mid`:

- If `arr[mid] > x` → `mid` is a **valid answer**, but a smaller index might also work, so **look left**
- If `arr[mid] <= x` → `mid` is **too small or equal**, and so is everything before it, so **look right**

This lets us throw away half the array in every step, which is just **binary search**.

<mark>Notice the second case carefully. When arr[mid] is EQUAL to the target, we move right, because an equal element can never be the upper bound.</mark>

<br><br>

### 4. Code

```python
class UpperBoundFinder:
    # Function to find the upper bound index using binary search
    def upper_bound(self, arr, x):
        low, high = 0, len(arr) - 1     # Search range
        ans = len(arr)                  # Default value if not found
        while low <= high:
            mid = (low + high) // 2     # Find middle index
            if arr[mid] > x:
                ans = mid               # Store possible answer
                high = mid - 1          # Move to the left
            else:
                low = mid + 1           # Move to the right
        return ans                      # Return result

# Driver code
arr = [3, 5, 8, 15, 19]                # Sorted input array
x = 8                                  # Target value
finder = UpperBoundFinder()            # Create object
ind = finder.upper_bound(arr, x)       # Call method
print("The upper bound is the index:", ind)  # Output result
```

`ans` starts at `len(arr)` on purpose. If no element is ever found to be `> x`, that default is already the correct answer.

<br><br>

### 5. Dry Run

Input: `arr = [3, 5, 8, 15, 19]`, `x = 8`

```ini
Start: low = 0, high = 4, ans = 5

Step 1:
  mid = (0 + 4) // 2 = 2
  arr[2] = 8  ->  Is 8 > 8 ?  NO   (equal is not allowed)
  Not valid, so move right
  low = 3        (low = 3, high = 4, ans = 5)

Step 2:
  mid = (3 + 4) // 2 = 3
  arr[3] = 15 ->  Is 15 > 8 ?  YES
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