# Find n'th Node from the End of a Linked List
`Educative`

```python
def find_nth_from_last(head, n):
    # Return None if linked list is empty or value of n is less than 1
    if not head or n < 1:
        return None

    # We will use two pointers head and tail
    tail = head

    # Making tail 'n' nodes apart from the head
    while tail and n > 0:
        tail = tail.next
        n -= 1

    # Check out-of-bounds
    if n != 0:
        return None

    # When tail pointer reaches the end of
    # list, head is pointing at nth node.
    while tail:
        tail = tail.next
        head = head.next

    return head
```