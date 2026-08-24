# Reverse a singly list in O(N) time and O(1) space.

To reverse a singly linked list in O(N) time and O(1) space, you can use an iterative approach. Here's a simple algorithm to achieve this:

`Educative`

```python
class ListNode:
    def __init__(self, value=0, next=None):
        self.value = value
        self.next = next

def reverse_linked_list(head):
    prev = None
    current = head

    while current is not None:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node

    return prev
```

This algorithm uses three pointers (prev, current, and next_node) to reverse the links in the list. It iterates through the list, updating the next pointers to reverse the direction of the links. The time complexity is O(N) since it visits each node once, and the space complexity is O(1) because it uses a constant amount of extra space, regardless of the size of the input list.