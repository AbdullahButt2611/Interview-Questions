# Merge Sort

- Done Recursively
- Divide and Conquer

```psudo
mergeSort(array a)
    if (n == 1)
        return a

    arrayOne = a[0] .. a[n/2]
    arrayTwo = a[n/2 + 1] .. a[n]

    arrayOne = mergeSort(arrayOne)
    arrayTwo = mergeSort(arrayTwo)

    return merge(arrayOne, arrayTwo)

merge(array a, array b)
    array c

    while (a and b has elements)
        if a[0] > b[0]
            add b[0] to the end of c
            remove b[0] from b
        else
            add a[0] to the end of c
            remove a[0] from a
    
    // Till here either a or b will be empty
    // Applying extra loop to check if their is any element in any other array

    while (a has elements)
        add a[0] to the end of c
        remove a[0] from a

    while (b has elements)
        add b[0] to the end of c
        remove b[0] from b

    return c

```


- **Worst Case** Time Complexity is `O(nlogn)`