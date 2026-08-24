# Intersection Point of Two Lists
`Educative`

> **Note:** The linked lists have to physically intersect. This means that their addresses need to be the same. If two nodes have the same data but their addresses are not the same, the lists won’t intersect and the function should return null.


## Algorithm:
The complete algorithm is given below:
```
Find lengths of both linked lists: L1 and L2
Calculate the difference in length of both linked lists: d = |L1 - L2|
Move head pointer of longer list 'd' steps forward
Now traverse both lists, comparing nodes until we find a match or reach the end of the lists
```

## Solution

```python
def getIntersectionNode(self, headA, headB):
        """
        :type head1, head1: ListNode
        :rtype: ListNode
        """

        lencurr = headA
        lenA = 0
        while lencurr:
            lenA += 1
            lencurr = lencurr.next
        
        lencurr = headB
        lenB = 0
        while lencurr:
            lenB += 1
            lencurr = lencurr.next

        currA = headA
        if lenA < lenB or lenB < lenA:
            d = abs(lenA - lenB)
            if lenA > lenB:
                while d>0:
                    headA = headA.next
                    d -= 1
            else:
                while d>0:
                    headB = headB.next
                    d -= 1
        
        while headA and headB:
            # print(headA.val, headB.val)
            if headA == headB:
                return headA
            else:
                headA = headA.next
                headB = headB.next
        
        return None
```