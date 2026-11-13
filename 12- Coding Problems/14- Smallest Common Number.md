# Find the Smallest Common Number
> Given three integer arrays sorted in ascending order, return the smallest number found in all three arrays.

`Educative`

```python
def findSmallestCommonNumber(arr1, arr2, arr3):
    i, j, k = 0, 0, 0  # Initialize pointers for each array
    
    # Traverse through all arrays
    while i < len(arr1) and j < len(arr2) and k < len(arr3):
        # If elements from all arrays are equal, return the common element
        if arr1[i] == arr2[j] == arr3[k]:
            return arr1[i]
        
        # Move the pointer of the smallest element
        if arr1[i] < arr2[j]:
            i += 1
        elif arr2[j] < arr3[k]:
            j += 1
        else:
            k += 1
    
    # If no common element is found, return -1 or any suitable value
    return -1

# Example usage
arr1 = [1, 5, 10, 20, 40, 80]
arr2 = [6, 7, 20, 80, 100]
arr3 = [3, 4, 15, 20, 30, 70, 80]

result = findSmallestCommonNumber(arr1, arr2, arr3)
print(result)  # Output: 20

```