## Given a linked list of integers, remove all the duplicate nodes from the linked list while retaining only the first occurrence of each duplicate.

`Educative`

```python
def remove_duplicates(head):
    #TODO: Write - Your - Code
    occurence = []
    prev = None
    start_head = head
    while head is not None:
        if head.data in occurence:
            prev.next = head.next
        else:
            occurence.append(head.data)
            prev = head
        head = head.next

    head = start_head 

    return head
```