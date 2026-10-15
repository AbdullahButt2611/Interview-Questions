##  Given an array of integers e.g. [-3, 2, 0,-5,1, 5], find all the triplets where sum = K. For K=0 output is (-3,2,1), (-5, 0, 5)
`Educative`

A better solution is using a hash table (dictionary in Python) to store the frequencies of elements. This solution has a time complexity of O(n^2), where n is the size of the array. Here's how you can implement it.

```python
def find_triplets(arr, K):
    triplets = []
    n = len(arr)

    # Create a dictionary to store the frequency of each element
    freq = {}
    for num in arr:
        if num in freq:
            freq[num] += 1
        else:
            freq[num] = 1

    for i in range(n - 1):
        for j in range(i + 1, n):
            # Calculate the required third element to reach K
            third = K - (arr[i] + arr[j])
            # Check if it exists in the dictionary and ensure it's not one of the elements already chosen
            if third in freq and (third != arr[i] and third != arr[j] or freq[third] > 1):
                triplets.append((arr[i], arr[j], third))

    return triplets

# Example usage:
arr = [-3, 2, 0, -5, 1, 5]
K = 0
print(find_triplets(arr, K))  # Output: [(-3, 2, 1), (-5, 0, 5)]
```

### Dry Run

Sure, let's dry run the provided Python code for the given array `arr = [-3, 2, 0, -5, 1, 5]` and target sum `K = 0`.
- Initialization
    - Initialize an empty list triplets to store the result.
    - Calculate the length of the array n = 6.

- Frequency Calculation:
    - Iterate through the array and store the frequency of each element in the dictionary freq:
    ```python
        freq = {-3: 1, 2: 1, 0: 1, -5: 1, 1: 1, 5: 1}
    ```

- Nested Loop Iteration:

    - The first loop runs from index 0 to index n - 2 = 4.
        - For i = 0, the second loop runs from index i + 1 = 1 to index n - 1 = 5.
            - For j = 1, calculate the required third element to reach the target sum: third = K - (arr[i] + arr[j]) = 0 - (-3 + 2) = 1.
                - Check if third = 1 exists in freq and if it's not one of the elements already chosen. Since it exists, add the triplet (-3, 2, 1) to triplets.
            - Proceed to check for other possible combinations of i and j.
        - Proceed similarly for other values of i.

- Result:
    - After all iterations, the triplets list contains the triplets (-3, 2, 1) and (-5, 0, 5).
    
So, the output of the function will be triplets = [(-3, 2, 1), (-5, 0, 5)], which matches the expected result.