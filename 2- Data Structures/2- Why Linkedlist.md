# Why Linkedlist?
`Arbisoft`

Linked lists are a data structure used in computer science to organize and store data in a linear fashion. Unlike arrays, linked lists do not require contiguous memory locations, which makes them more flexible and dynamic.

## Reasons for Using Linked Lists

1. **Dynamic Size:** Linked lists can easily grow or shrink in size during program execution. This dynamic allocation of memory is particularly useful when the size of the data structure is not known in advance or can change frequently.

2. **Insertion and Deletion:** Inserting or deleting elements in a linked list is generally more efficient than in an array, especially in the middle of the list. In a linked list, you can simply adjust pointers to add or remove elements, while in an array, elements might need to be shifted to accommodate changes.

3. **Memory Utilization:** Linked lists can be more memory-efficient than arrays in certain situations. With arrays, you often need to allocate a fixed amount of memory, while linked lists allocate memory as needed.

4. **No Pre-allocation:** Unlike arrays, linked lists don't require pre-allocation of memory. This can be advantageous in situations where the exact size of the data structure is unknown or may change frequently.

5. **Ease of Implementation:** Linked lists are relatively easy to implement and understand. They consist of nodes where each node contains a data element and a reference (or link) to the next node in the sequence.

## Drawbacks

However, it's important to note that linked lists also have some drawbacks. They may have higher memory overhead due to the storage of additional pointers, and accessing elements in a linked list is generally slower compared to arrays because elements are not stored in contiguous memory locations. The choice between arrays and linked lists depends on the specific requirements of the problem at hand.
