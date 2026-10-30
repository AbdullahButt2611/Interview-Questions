## Clone a LinkedList with Next and Random Pointers
`Educative`

Cloning a linked list with both next and random pointers involves creating a deep copy of each node in the original list while maintaining the connections between them. Here's a Python implementation of how you can achieve this:

```python
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.random = None

def clone_linked_list(head):
    if not head:
        return None
    
    # Step 1: Create a copy of each node and insert it next to the original node
    current = head
    while current:
        new_node = Node(current.val)
        new_node.next = current.next
        current.next = new_node
        current = new_node.next
    
    # Step 2: Update the random pointers of the copied nodes
    current = head
    while current:
        if current.random:
            current.next.random = current.random.next
        current = current.next.next
    
    # Step 3: Separate the original and copied nodes
    original_head = head
    new_head = head.next
    current = new_head
    while original_head:
        original_head.next = original_head.next.next
        if current.next:
            current.next = current.next.next
        original_head = original_head.next
        current = current.next
    
    return new_head

# Example usage:
# Create a linked list with next and random pointers
head = Node(1)
head.next = Node(2)
head.next.next = Node(3)
head.next.next.next = Node(4)
head.random = head.next.next
head.next.random = head.next.next.next
head.next.next.random = head
head.next.next.next.random = head.next

# Clone the linked list
cloned_head = clone_linked_list(head)

# Print the cloned linked list
current = cloned_head
while current:
    print("Value:", current.val, "Random:", current.random.val if current.random else None)
    current = current.next
```

This code first creates a copy of each node and inserts it next to the original node. Then it updates the random pointers of the copied nodes. Finally, it separates the original and copied nodes to obtain the cloned linked list.