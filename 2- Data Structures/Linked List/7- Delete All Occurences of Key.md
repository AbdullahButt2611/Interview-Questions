## We’re given the head of a linked list and a key. Delete all the nodes that contain the given key.
`Educative`

```python
def delete_node(head, key):
    #TODO: Write - Your - Code
    while head is not None and head.data == key:
        head = head.next
    
    keep_head = head
    prev = None

    if keep_head is not None:
        head = head.next

        while head is not None:
            if head.data == key:
                prev.next = head.next
            else:
                prev = head
            head = head.next

    return keep_head
```