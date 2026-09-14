# Maximum Width of Binary Tree

`Amazon` • `Microsoft` • `Google` • `Meta` • `Bloomberg` • `Adobe` • `Flipkart`

## Problem Statement

Given the `root` of a binary tree, return the **maximum width** of the given tree.

* The maximum width of a tree is the maximum width among all levels.
* The width of one level is the distance between the **leftmost** and the **rightmost** non-null node of that level.
* The null nodes sitting **between** those two end nodes are also counted, as if the tree were a complete binary tree down to that level.

<mark>Null nodes before the leftmost node and after the rightmost node are NOT counted. Only the gaps in between matter.</mark>

It is guaranteed that the answer will be in the range of a 32-bit signed integer.

## Examples

**Example 1**

```ini
Input: root = [1,3,2,5,3,null,9]
Output: 4
Explanation: The maximum width exists in the third level with length 4 (5,3,null,9).
```

**Example 2**

```ini
Input: root = [1,3,2,5,null,null,9,6,null,7]
Output: 7
Explanation: The maximum width exists in the fourth level with length 7 (6,null,null,null,null,null,7).
```

**Example 3**

```ini
Input: root = [1,3,2,5]
Output: 2
Explanation: The maximum width exists in the second level with length 2 (3,2).
```

## Constraints

* The number of nodes in the tree is in the range `[1, 3000]`.
* `-100 <= Node.val <= 100`

<br><br>

## Approach

**The core problem**

Counting how many nodes are present on a level is not enough, because the empty spaces in the middle also count. So instead of counting nodes, we need to know **where** each node sits on its level.

<br><br>

**The trick: give every node a seat number**

Pretend the tree is a perfect (complete) binary tree where every possible seat exists, and number the seats:

* The root gets seat number `0`.
* If a node sits at seat `i`, then its left child sits at `2 * i + 1` and its right child sits at `2 * i + 2`.

This is the same numbering used for a heap stored inside an array. The beauty of it is that the seat number is fixed by the shape of the tree, so even if the middle nodes are missing, the surviving nodes still keep their correct positions.

<br><br>

**Getting the width from seat numbers**

Once every node on a level knows its seat number:

```ini
width of a level = (seat of rightmost node) - (seat of leftmost node) + 1
```

The `+ 1` is there because both end nodes are part of the width themselves.

<br><br>

**Walking the tree level by level**

We use BFS (a queue) so that we always handle one full level at a time:

* Push `(root, 0)` into the queue, that is the node along with its seat number.
* At the start of every level, note down `level_size = len(queue)`. This tells us exactly how many nodes belong to this level, so we never mix two levels together.
* Pop those many nodes one by one. The **first** one popped is the leftmost node of the level and the **last** one popped is the rightmost node.
* While popping a node, push its children with their seat numbers `2 * i + 1` and `2 * i + 2`.
* After finishing the level, compute `last - first + 1` and update the answer if it is bigger.

<br><br>

**Why we subtract the smallest seat number**

Seat numbers double at every level, so for a deep and skewed tree they can grow into huge values. To keep them small, we take the seat number of the first node in the level (`min_index`) and shift the whole level so that it starts from `0`:

```ini
curr_index = idx - min_index
```

Since we subtract the **same** amount from every node on the level, the distance between the two end nodes does not change, so the width stays correct. The children are then pushed using this shifted value, which keeps the numbers small forever.

<br><br>

## Code

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def widthOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        
        max_width = 0

        q = deque()
        q.append((root, 0))

        while q:
            level_size = len(q)

            min_index = q[0][1]

            first = 0
            last = 0

            for i in range(level_size):
                node, idx =  q.popleft()
                curr_index = idx - min_index

                if i == 0:
                    first = curr_index
                
                if i == level_size - 1:
                    last = curr_index
                
                if node.left:
                    q.append((node.left, 2 * curr_index + 1))
                if node.right:
                    q.append((node.right, 2 * curr_index + 2))
                
            max_width = max(max_width, last - first + 1)
        
        return max_width
```

<br><br>

## Dry Run

```ini
Input: root = [1,3,2,5,3,null,9]

Tree shape:

          1
        /   \
       3     2
      / \     \
     5   3     9

Initial state:
    max_width = 0
    q = [(1, 0)]          # (node, seat number), root sits at seat 0


============================================================
LEVEL 0
============================================================

level_size = len(q) = 1
min_index  = q[0][1] = 0
first = 0, last = 0

Iteration 1  (i = 0)
    popped        -> node = 1, idx = 0
    curr_index    =  0 - 0 = 0
    i == 0        -> first = 0
    i == size - 1 -> last  = 0
    node.left = 3 -> push (3, 2*0 + 1 = 1)
    node.right = 2 -> push (2, 2*0 + 2 = 2)
    q = [(3, 1), (2, 2)]

End of level 0:
    width      = last - first + 1 = 0 - 0 + 1 = 1
    max_width  = max(0, 1) = 1


============================================================
LEVEL 1
============================================================

level_size = len(q) = 2
min_index  = q[0][1] = 1       # leftmost node of this level sits at seat 1
first = 0, last = 0

Iteration 1  (i = 0)
    popped        -> node = 3, idx = 1
    curr_index    =  1 - 1 = 0      # shifted so the level starts at 0
    i == 0        -> first = 0
    node.left = 5 -> push (5, 2*0 + 1 = 1)
    node.right = 3 -> push (3, 2*0 + 2 = 2)
    q = [(2, 2), (5, 1), (3, 2)]

Iteration 2  (i = 1)
    popped        -> node = 2, idx = 2
    curr_index    =  2 - 1 = 1
    i == size - 1 -> last = 1
    node.left  = None -> nothing pushed
    node.right = 9    -> push (9, 2*1 + 2 = 4)
    q = [(5, 1), (3, 2), (9, 4)]

End of level 1:
    width      = last - first + 1 = 1 - 0 + 1 = 2
    max_width  = max(1, 2) = 2


============================================================
LEVEL 2
============================================================

level_size = len(q) = 3
min_index  = q[0][1] = 1
first = 0, last = 0

Iteration 1  (i = 0)
    popped        -> node = 5, idx = 1
    curr_index    =  1 - 1 = 0
    i == 0        -> first = 0
    no children   -> nothing pushed
    q = [(3, 2), (9, 4)]

Iteration 2  (i = 1)
    popped        -> node = 3, idx = 2
    curr_index    =  2 - 1 = 1
    not first, not last -> only used for pushing children
    no children   -> nothing pushed
    q = [(9, 4)]

Iteration 3  (i = 2)
    popped        -> node = 9, idx = 4
    curr_index    =  4 - 1 = 3      # seat 2 is the empty spot between 3 and 9
    i == size - 1 -> last = 3
    no children   -> nothing pushed
    q = []

End of level 2:
    width      = last - first + 1 = 3 - 0 + 1 = 4
    max_width  = max(2, 4) = 4

    Seats on this level:  0 -> 5,  1 -> 3,  2 -> null,  3 -> 9
    That null in the middle is exactly why the width is 4 and not 3.


============================================================
QUEUE IS EMPTY, LOOP ENDS
============================================================

Answer returned: max_width = 4
```

<br><br>

## Complexity

* **Time:** `O(n)`, every node is pushed into the queue once and popped once.
* **Space:** `O(w)`, where `w` is the largest number of nodes held in the queue at any moment (the widest level). In the worst case this is `O(n)`.

<br><br>

## Related Problems

* [Binary Tree Level Order Traversal (102)](https://leetcode.com/problems/binary-tree-level-order-traversal/)
* [Binary Tree Zigzag Level Order Traversal (103)](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/)
* [Binary Tree Right Side View (199)](https://leetcode.com/problems/binary-tree-right-side-view/)
* [Find Largest Value in Each Tree Row (515)](https://leetcode.com/problems/find-largest-value-in-each-tree-row/)
* [Average of Levels in Binary Tree (637)](https://leetcode.com/problems/average-of-levels-in-binary-tree/)
* [Maximum Level Sum of a Binary Tree (1161)](https://leetcode.com/problems/maximum-level-sum-of-a-binary-tree/)
* [Maximum Depth of Binary Tree (104)](https://leetcode.com/problems/maximum-depth-of-binary-tree/)
* [Vertical Order Traversal of a Binary Tree (987)](https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree/)
* [Check Completeness of a Binary Tree (958)](https://leetcode.com/problems/check-completeness-of-a-binary-tree/)