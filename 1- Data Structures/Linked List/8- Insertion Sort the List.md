## Sort Linked List Using Insertion Sort

`Educative`

```python
class Solution(object):
    def insertionSortList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        def sortUsingInsertion(head, node): 
            if not node:
                return head
            
            if not head or node.val <= head.val:
                node.next = head
                return node
            
            curr = head
            
            while curr.next and curr.next.val < node.val:
                curr = curr.next
            
            node.next = curr.next
            curr.next = node

            return head
        
        sortedList = None
        curr = head

        while curr:
            temp = curr.next
            sortedList = sortUsingInsertion(sortedList, curr)
            curr = temp
        
        return sortedList
```