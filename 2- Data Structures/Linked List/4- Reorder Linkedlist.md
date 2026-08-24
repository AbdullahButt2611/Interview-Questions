## Update singly linkedlist such that output is:  First->last->second->second_last->third->third_last.....
`Educative`

To update a singly linked list such that the output follows the pattern "First->last->second->second_last->third->third_last...", you'll need to reorder the nodes accordingly. Here's a Python implementation to achieve this:

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reorder_linked_list(head):
    # Edge case: if the linked list is empty or has only one node
    if not head or not head.next:
        return head

    # Split the linked list into two halves
    slow, fast = head, head
    while fast and fast.next:
        slow_prev = slow
        slow = slow.next
        fast = fast.next.next

    slow_prev.next = None  # disconnect the first half from the second half

    # Reverse the second half of the linked list
    prev = None
    curr = slow
    while curr:
        temp = curr.next
        curr.next = prev
        prev = curr
        curr = temp

    # Merge the two halves following the specified pattern
    first = head
    second = prev
    while second:
        first_next = first.next
        second_next = second.next

        first.next = second
        second.next = first_next

        first = first_next
        second = second_next

    return head

def print_linked_list(head):
    while head:
        print(head.val, end="->")
        head = head.next
    print("None")

# Example usage:
# Create a sample linked list: 1->2->3->4->5
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
head.next.next.next = ListNode(4)
head.next.next.next.next = ListNode(5)

print("Original Linked List:")
print_linked_list(head)

# Update the linked list as per the specified pattern
head = reorder_linked_list(head)

print("Updated Linked List:")
print_linked_list(head)
```

