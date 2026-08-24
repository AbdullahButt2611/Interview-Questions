## Given two arrays num and index, sort both arrays according to the index array.
`Visnext`

Here’s a Python solution with clear explanations

```
# Define the function that sorts 'num' based on the order of 'index'
def sort_by_index(num, index):
    """
    This function sorts the 'num' array according to the sorting order of 'index' array.
    
    Parameters:
    num (list): The list of numbers to be sorted.
    index (list): The list of indices that determines the sorting order.

    Returns:
    list: A new sorted list of numbers based on 'index'.
    """
    
    # Step 1: Pair each element from 'num' with its corresponding index
    paired = list(zip(index, num))
    
    # Step 2: Sort the paired list based on the first element (index values)
    paired.sort()  # By default, sort() arranges tuples by the first value
    
    # Step 3: Extract the sorted numbers from the sorted pairs
    sorted_num = [value for _, value in paired]
    
    return sorted_num

# Example Usage
num = [50, 20, 40, 10, 30]
index = [3, 1, 4, 0, 2]

# Calling the function and printing the sorted numbers
sorted_numbers = sort_by_index(num, index)
print(sorted_numbers)  # Output: [10, 20, 30, 50, 40]
```
<br><br>

### Explanation:

1. **Pairing Elements:**  
   - We use `zip(index, num)` to create pairs where each number is associated with its corresponding index.
   - Example: `[(3, 50), (1, 20), (4, 40), (0, 10), (2, 30)]`

2. **Sorting Pairs:**  
   - We sort the list of pairs based on the index value (first element of the tuple).
   - After sorting: `[(0, 10), (1, 20), (2, 30), (3, 50), (4, 40)]`

3. **Extracting Sorted Values:**  
   - We extract only the numbers (second element of each tuple) to get `[10, 20, 30, 50, 40]`.

This ensures that the `num` array is rearranged based on the order specified in `index`.

<br><br>

### Another Solution

```
# Function to sort 'num' based on 'index' without using zip
def sort_by_index(num, index):
    # Create an empty list of the same size as num
    sorted_num = [0] * len(num)
    
    # Place each element of num at the correct position in sorted_num
    for i in range(len(num)):
        sorted_num[index[i]] = num[i]
    
    return sorted_num

# Example usage
num = [50, 20, 40, 10, 30]
index = [3, 1, 4, 0, 2]

sorted_numbers = sort_by_index(num, index)
print(sorted_numbers)  # Output: [10, 20, 30, 50, 40]
```

