# Odd Even Linked List

`Amazon` • `Google` • `Meta` • `Bloomberg` • `Apple` • `Adobe`

## Problem Statement

Given the `head` of a **singly linked list**, group all the nodes with **odd indices** together, followed by the nodes with **even indices**, and return the reordered list.

- The **first** node is odd, the **second** node is even, the third is odd, and so on.
- "Odd" and "even" are about the node's **position**. The value inside the node does not matter.
- The relative order inside the odd group and inside the even group must stay the same as the input.
- You must solve it in `O(1)` extra space and `O(n)` time.

## Examples

**Example 1:**

```ini
Input: head = [1,2,3,4,5]
Output: [1,3,5,2,4]
Explanation: Positions 1, 3, 5 hold 1, 3, 5. Positions 2, 4 hold 2, 4.
```

**Example 2:**

```ini
Input: head = [2,1,3,5,6,4,7]
Output: [2,3,6,7,1,5,4]
Explanation: Positions 1, 3, 5, 7 hold 2, 3, 6, 7. Positions 2, 4, 6 hold 1, 5, 4.
```

## Constraints

- The number of nodes in the linked list is in the range `[0, 10^4]`.
- `-10^6 <= Node.val <= 10^6`

<br><br>

## Approach

### The Picture to Keep in Your Head

Think of people standing in one line, counting off "1, 2, 1, 2, 1, 2...".

- Everyone who says **1** forms one line (the odd line).
- Everyone who says **2** forms another line (the even line).
- At the end, the even line walks over and stands **behind** the odd line.

We do the same thing with the nodes. We don't create any new nodes. We only change where each `next` arrow points.

> Memory hook: <mark>"Split into two chains by skipping one. Then glue the even chain to the end of the odd chain."</mark>

### Why Skipping Works

In the list, odd and even nodes always take turns.

- The node **after the next one** of an odd node is always the next odd node.
- The node after the next one of an even node is always the next even node.

So if every node points two steps ahead (`node.next = node.next.next`), the list falls apart into two clean chains.

### Step by Step

1. **Handle tiny lists.**
   - If the list is empty or has only one node, there is nothing to move. Return `head`.

2. **Set up three pointers.**
   - `odd` starts at the 1st node. It walks along the odd chain.
   - `even` starts at the 2nd node. It walks along the even chain.
   - `evenHead` also points at the 2nd node, and it **never moves**.

3. **Remember why `evenHead` exists.**
   - At the end we must attach the even chain behind the odd chain.
   - By then, `even` has walked to the end. We would lose the start of the even chain.
   - <mark>Save the start of the even chain before you break anything.</mark>

4. **Loop while `even` and `even.next` both exist.**
   - `even.next` is the next odd node. If it is missing, there is no more odd node to link, so we are done.
   - Inside the loop, do four small moves:
     - `odd.next = odd.next.next` makes the odd node skip over the even node and point to the next odd node.
     - `even.next = even.next.next` makes the even node skip over that odd node and point to the next even node.
     - `odd = odd.next` moves `odd` forward on its chain.
     - `even = even.next` moves `even` forward on its chain.

5. **Glue the two chains.**
   - `odd` is now sitting on the last odd node.
   - Set `odd.next = evenHead`. The even chain now hangs off the end of the odd chain.

6. **Return `head`.**
   - The first node is odd, so it is still the first node of the answer.

### Why the Even Chain Ends Cleanly

- If the list length is **odd**, the last skip sets the last even node's `next` to `None`.
- If the list length is **even**, the last node is already an even node, and its `next` was `None` from the start.
- Either way the even chain ends with `None`, so the final list has no loop.

<br><br>

## Solution

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def oddEvenList(self, head: ListNode | None) -> ListNode | None:
        if not head or not head.next:
            return head

        odd = head
        even = head.next
        evenHead = head.next

        while even and even.next:
            odd.next = odd.next.next
            even.next = even.next.next

            odd = odd.next
            even = even.next

        odd.next = evenHead

        return head
```

<br><br>

## Dry Run

```ini
=====================================================
SCENARIO A: head = [1,2,3,4,5]  (Example 1, odd length)
=====================================================

Starting List:

  1 → 2 → 3 → 4 → 5 → None

Check: Is head None or head.next None? NO. Continue.

Setup:
  odd      = 1
  even     = 2
  evenHead = 2   (this stays on node 2 forever)

  1 → 2 → 3 → 4 → 5 → None
  ↑   ↑
  O   E

Iteration 1:
  Loop check: even = 2 exists, even.next = 3 exists. Enter loop.

  odd.next = odd.next.next
    odd.next is 2, and 2.next is 3
    So 1.next = 3        (1 now skips over 2)

  even.next = even.next.next
    even.next is 3, and 3.next is 4
    So 2.next = 4        (2 now skips over 3)

  odd  = odd.next  = 3
  even = even.next = 4

  Odd chain so far:   1 → 3
  Even chain so far:  2 → 4
  odd is on 3, even is on 4

  (Node 3 still points to 4 right now. The next round fixes that.)

Iteration 2:
  Loop check: even = 4 exists, even.next = 5 exists. Enter loop.

  odd.next = odd.next.next
    odd.next is 4, and 4.next is 5
    So 3.next = 5        (3 now skips over 4)

  even.next = even.next.next
    even.next is 5, and 5.next is None
    So 4.next = None     (4 is now the end of the even chain)

  odd  = odd.next  = 5
  even = even.next = None

  Odd chain so far:   1 → 3 → 5
  Even chain so far:  2 → 4 → None

Iteration 3:
  Loop check: even = None. Exit loop.

Glue the chains:
  odd is on 5, the last odd node.
  odd.next = evenHead
  So 5.next = 2

Final List:

  1 → 3 → 5 → 2 → 4 → None

Return head (node 1)
Output: [1,3,5,2,4]  ✓


=====================================================
SCENARIO B: head = [2,1,3,5,6,4,7]  (Example 2, odd length)
=====================================================

Starting List:

  2 → 1 → 3 → 5 → 6 → 4 → 7 → None

Check: Is head None or head.next None? NO. Continue.

Setup:
  odd      = 2
  even     = 1
  evenHead = 1   (this stays on node 1 forever)

  2 → 1 → 3 → 5 → 6 → 4 → 7 → None
  ↑   ↑
  O   E

Iteration 1:
  Loop check: even = 1 exists, even.next = 3 exists. Enter loop.

  odd.next = odd.next.next
    odd.next is 1, and 1.next is 3
    So 2.next = 3

  even.next = even.next.next
    even.next is 3, and 3.next is 5
    So 1.next = 5

  odd  = 3
  even = 5

  Odd chain so far:   2 → 3
  Even chain so far:  1 → 5

Iteration 2:
  Loop check: even = 5 exists, even.next = 6 exists. Enter loop.

  odd.next = odd.next.next
    odd.next is 5, and 5.next is 6
    So 3.next = 6

  even.next = even.next.next
    even.next is 6, and 6.next is 4
    So 5.next = 4

  odd  = 6
  even = 4

  Odd chain so far:   2 → 3 → 6
  Even chain so far:  1 → 5 → 4

Iteration 3:
  Loop check: even = 4 exists, even.next = 7 exists. Enter loop.

  odd.next = odd.next.next
    odd.next is 4, and 4.next is 7
    So 6.next = 7

  even.next = even.next.next
    even.next is 7, and 7.next is None
    So 4.next = None

  odd  = 7
  even = None

  Odd chain so far:   2 → 3 → 6 → 7
  Even chain so far:  1 → 5 → 4 → None

Iteration 4:
  Loop check: even = None. Exit loop.

Glue the chains:
  odd is on 7, the last odd node.
  odd.next = evenHead
  So 7.next = 1

Final List:

  2 → 3 → 6 → 7 → 1 → 5 → 4 → None

Return head (node 2)
Output: [2,3,6,7,1,5,4]  ✓


=====================================================
SCENARIO C: head = [1,2,3,4]  (even length, loop stops a different way)
=====================================================

Starting List:

  1 → 2 → 3 → 4 → None

Check: Is head None or head.next None? NO. Continue.

Setup:
  odd      = 1
  even     = 2
  evenHead = 2

Iteration 1:
  Loop check: even = 2 exists, even.next = 3 exists. Enter loop.

  odd.next = odd.next.next
    odd.next is 2, and 2.next is 3
    So 1.next = 3

  even.next = even.next.next
    even.next is 3, and 3.next is 4
    So 2.next = 4

  odd  = 3
  even = 4

  Odd chain so far:   1 → 3
  Even chain so far:  2 → 4

Iteration 2:
  Loop check: even = 4 exists, but even.next = None. Exit loop.
  There is no odd node after 4, so nothing is left to link.

  Node 4 already points to None, so the even chain ends cleanly.

Glue the chains:
  odd is on 3, the last odd node.
  odd.next = evenHead
  So 3.next = 2

Final List:

  1 → 3 → 2 → 4 → None

Return head (node 1)
Output: [1,3,2,4]  ✓


=====================================================
SCENARIO D: head = [7]  (single node)
=====================================================

Check: Is head None or head.next None? YES, head.next is None.
  One node is already "odd group first, even group after".
  Return head right away.

Output: [7]  ✓
```

<br><br>

## Complexity Analysis

- **Time Complexity:** `O(n)`, where `n` is the number of nodes.
  - Each loop round moves both `odd` and `even` forward by one node of their chain.
  - Every node is visited once.
- **Space Complexity:** `O(1)`.
  - Only three pointers are used: `odd`, `even`, `evenHead`.
  - No new nodes, no extra list, no recursion.

<br><br>

## Related Problems

- [Swap Nodes in Pairs (24)](https://leetcode.com/problems/swap-nodes-in-pairs/)
- [Rotate List (61)](https://leetcode.com/problems/rotate-list/)
- [Partition List (86)](https://leetcode.com/problems/partition-list/)
- [Reorder List (143)](https://leetcode.com/problems/reorder-list/)
- [Split Linked List in Parts (725)](https://leetcode.com/problems/split-linked-list-in-parts/)
- [Middle of the Linked List (876)](https://leetcode.com/problems/middle-of-the-linked-list/)
- [Sort Array By Parity (905)](https://leetcode.com/problems/sort-array-by-parity/)
- [Sort Array By Parity II (922)](https://leetcode.com/problems/sort-array-by-parity-ii/)
- [Reverse Nodes in Even Length Groups (2074)](https://leetcode.com/problems/reverse-nodes-in-even-length-groups/)
- [Rearrange Array Elements by Sign (2149)](https://leetcode.com/problems/rearrange-array-elements-by-sign/)
