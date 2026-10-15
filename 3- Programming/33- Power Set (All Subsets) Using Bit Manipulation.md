# Power Set (All Subsets) Using Bit Manipulation
### Given an array of inetgers, display all subsets.(power set)
`Visnext`
<br><br>

To generate all subsets (the power set) of a given array of integers, we can use the following approach step by step:

### Step-by-Step Explanation:

1. **Understand the Problem**:
   - The power set is the set of all subsets of a given set. 
   - For example, if the array is `[1, 2]`, the power set is `[], [1], [2], [1, 2]`. 
   - An empty set is always a subset of any set, and every set is a subset of itself.

2. **Key Insight**:
   - This gives us two choices per element, meaning if the array has `n` elements, the total number of subsets will be `2^n`.

3. **Approach**:
   - One of the most straightforward methods to generate the power set is to use **binary representation**:
     - For an array of size `n`, represent each subset by a binary number where each bit corresponds to whether an element is included in the subset (1 means included, 0 means excluded).

4. **Steps**:
   1. **Start with the empty subset**.
   2. **Iterate over all numbers from `0` to `2^n - 1`**. Each number represents a binary number, and each bit in this number decides whether to include or exclude the corresponding element in the subset.
   3. **For each number**:
      - Convert the number to binary.
      - Use the bits of this number to decide which elements to include in the current subset.
   4. **Collect and print all subsets**.

### Example Walkthrough:

For an array `arr = [1, 2]` (length `n = 2`):

1. The total number of subsets is `2^2 = 4`.
2. Iterate through numbers from `0` to `3` (binary representation from `00` to `11`).
   - `0` (binary `00`): No elements included → `[]`.
   - `1` (binary `01`): Only the second element (2) included → `[2]`.
   - `2` (binary `10`): Only the first element (1) included → `[1]`.
   - `3` (binary `11`): Both elements (1 and 2) included → `[1, 2]`.

Thus, the power set of `[1, 2]` is `[[], [2], [1], [1, 2]]`.

### Code Example:

```python
def generate_subsets(arr):
    n = len(arr)
    power_set = []
    
    # Total number of subsets = 2^n
    for i in range(2 ** n):
        subset = []
        
        # Check each bit in the binary representation of i
        for j in range(n):
            # If the j-th bit of i is set, include arr[j]
            if (i & (1 << j)) > 0:
                subset.append(arr[j])
        
        power_set.append(subset)
    
    return power_set

# Example usage:
arr = [1, 2]
result = generate_subsets(arr)
print(result)
```

### Explanation of the Code:
1. **Loop through numbers from `0` to `2^n - 1`**:
   - `i` represents the current subset in its binary form.
   
2. **Inner loop**:
   - For each bit in `i`, check if it's set. If the bit is set (`i & (1 << j)`), include `arr[j]` in the current subset.
   
3. **Append the subset to the result** and return the list of all subsets.

### Output for `[1, 2]`:
```
[[], [1], [2], [1, 2]]
```

### Time Complexity:
- **Time Complexity**: `O(n * 2^n)` where `n` is the number of elements in the input array. This is because there are `2^n` subsets, and for each subset, we iterate through `n` elements to construct it.
- **Space Complexity**: `O(2^n)` for storing the power set.

This method ensures that you generate all possible subsets efficiently.