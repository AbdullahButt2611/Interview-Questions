# Delete the Middle Node of a Linked List
`LeetCode 75`

## Problem Statement

You are given the head of a singly linked list. Your task is to delete the **middle node** of the linked list and return the head of the modified list.

The middle node is defined using **0-based indexing**:

* For a list of size `n`, the middle node is at index `⌊n / 2⌋`.

### Examples

**Example 1**

Input:

```
head = [1,3,4,7,1,2,6]
```

Output:

```
[1,3,4,1,2,6]
```

Explanation:
The linked list has 7 nodes. Using 0-based indexing, the middle index is `⌊7 / 2⌋ = 3`.
The node at index 3 has value `7`, which is removed.

**Example 2**

Input:

```
head = [1,2,3,4]
```

Output:

```
[1,2,4]
```

Explanation:
The linked list has 4 nodes. The middle index is `⌊4 / 2⌋ = 2`.
The node at index 2 has value `3`, which is removed.

### Notes

* If the list has only **one node**, deleting the middle node results in an empty list.

## Input

* `head`: The head node of a singly linked list

## Output

* The head of the linked list after deleting the middle node

<br><br>

## Approach 1: Convert to Array (Brute Force)

### Idea

1. Traverse the linked list and store all nodes in an array.
2. Find the middle index using `n // 2`.
3. Remove the node at that index.
4. Rebuild the linked list from the remaining nodes.

### Code

```python
class Solution:
    def deleteMiddle(self, head):
        if not head:
            return None
        
        nodes = []
        curr = head
        
        while curr:
            nodes.append(curr)
            curr = curr.next
        
        if len(nodes) == 1:
            return None
        
        mid = len(nodes) // 2
        nodes[mid - 1].next = nodes[mid].next
        
        return head
```

### Problems with this Approach

* Uses extra memory to store all nodes
* Two passes over the data
* Not efficient for large lists

### Time and Space Complexity

* Time: `O(n)`
* Space: `O(n)`

<br><br>

## Approach 2: Count Length First

### Idea

1. Traverse the list once to find its length.
2. Compute the middle index.
3. Traverse again to reach the node before the middle.
4. Remove the middle node.

### Code

```python
class Solution:
    def deleteMiddle(self, head):
        if not head or not head.next:
            return None
        
        length = 0
        curr = head
        
        while curr:
            length += 1
            curr = curr.next
        
        mid = length // 2
        curr = head
        
        for _ in range(mid - 1):
            curr = curr.next
        
        curr.next = curr.next.next
        return head
```

### Problems with this Approach

* Requires two full passes
* Can be done in a single pass

### Time and Space Complexity

* Time: `O(n)`
* Space: `O(1)`

<br><br>

## Approach 3: Fast and Slow Pointers (Optimal)

### Idea

Use two pointers:

* `slow` moves one step at a time
* `fast` moves two steps at a time

When `fast` reaches the end, `slow` will be at the middle node. A third pointer `prev` keeps track of the node before `slow` so the middle node can be removed.

### Code

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def deleteMiddle(self, head: ListNode) -> ListNode:
        if not head or not head.next:
            return None
        
        slow = head
        fast = head
        prev = None
        
        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next
        
        prev.next = slow.next
        return head
```

### Why This Is the Best Solution

* Only one pass through the list
* No extra memory used
* Clean and simple logic

### Time and Space Complexity

* Time: `O(n)`
* Space: `O(1)`

<br><br>

## Final Notes

* This problem is commonly asked in interviews
* The fast and slow pointer method is the expected answer
* Always handle edge cases like a single-node list
