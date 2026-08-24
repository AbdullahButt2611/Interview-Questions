# Binary Tree Level Order Traversal

`Amazon` • `Microsoft` • `Google` • `Meta` • `Bloomberg` • `LinkedIn` • `Apple` • `Oracle` • `Uber` • `Adobe`

## Problem Statement

Given the `root` of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level).

## Examples

**Example 1:**

```ini
Input: root = [3,9,20,null,null,15,7]
Output: [[3],[9,20],[15,7]]
```

**Example 2:**

```ini
Input: root = [1]
Output: [[1]]
```

**Example 3:**

```ini
Input: root = []
Output: []
```

## Constraints

* The number of nodes in the tree is in the range `[0, 2000]`.
* `-1000 <= Node.val <= 1000`

<br><br>

## Approach

The goal is simple: read the tree one level at a time, from top to bottom, and inside each level go left to right.

To do this we use a **queue**, which is a first in, first out structure. Whatever we put in first is what comes out first. That "first in, first out" behavior is exactly what keeps our left to right order intact.

Here is the plan in plain words:

* Put the `root` inside a queue to begin with. If the tree is empty, there is nothing to do, so just return an empty list right away.
* Now keep repeating the steps below until the queue becomes empty:
  * First, note down how many nodes are sitting in the queue right now. That number is exactly how many nodes live on the current level.
  * Make a fresh empty list to collect the values of this level.
  * Loop that many times. On each turn, pull one node out from the front of the queue, drop its value into the level list, and push its left child and right child (whichever exist) to the back of the queue.
  * Once the loop ends, the level list holds every value of that level in order, so add it to the final answer.
* When the queue finally empties out, every level has been handled, so return the answer.

<mark>The real trick is freezing the count at the start of each round. That frozen number tells us where one level ends and the next begins.</mark> The children we add during a round belong to the next level, but because we only loop the old count of times, they patiently wait their turn and never mix into the current level.

<br><br>

## Code

```python
from collections import deque

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        tree = []
        if not root:
            return tree
        
        que = deque([root])
        while que:
            level = []
    
            for _ in range(len(que)):
                node = que.popleft()
                level.append(node.val)

                if node.left:
                    que.append(node.left)
                
                if node.right:
                    que.append(node.right)
            
            tree.append(level)

        return tree
```

<br><br>

## Dry Run

We will walk through **Example 1** step by step so you can see exactly what happens at every point.

```ini
Tree shape:

        3
       / \
      9   20
         /  \
        15   7

Start:
  tree = []
  root is not empty, so we continue
  que  = deque([3])


=================== ITERATION 1 (outer while) ===================
  que is not empty, so we enter the loop
  level = []
  frozen count = len(que) = 1   (only node 3 is on this level)

  inner loop runs 1 time:
    turn 1:
      node = popleft() -> 3
      level = [3]
      node 3 has left child 9   -> que.append(9)
      node 3 has right child 20 -> que.append(20)
      que = deque([9, 20])

  level [3] is done -> tree.append([3])
  tree = [[3]]


=================== ITERATION 2 (outer while) ===================
  que is not empty, so we enter the loop
  level = []
  frozen count = len(que) = 2   (nodes 9 and 20 are on this level)

  inner loop runs 2 times:
    turn 1:
      node = popleft() -> 9
      level = [9]
      node 9 has no left child
      node 9 has no right child
      que = deque([20])

    turn 2:
      node = popleft() -> 20
      level = [9, 20]
      node 20 has left child 15 -> que.append(15)
      node 20 has right child 7 -> que.append(7)
      que = deque([15, 7])

  level [9, 20] is done -> tree.append([9, 20])
  tree = [[3], [9, 20]]


=================== ITERATION 3 (outer while) ===================
  que is not empty, so we enter the loop
  level = []
  frozen count = len(que) = 2   (nodes 15 and 7 are on this level)

  inner loop runs 2 times:
    turn 1:
      node = popleft() -> 15
      level = [15]
      node 15 has no left child
      node 15 has no right child
      que = deque([7])

    turn 2:
      node = popleft() -> 7
      level = [15, 7]
      node 7 has no left child
      node 7 has no right child
      que = deque([])

  level [15, 7] is done -> tree.append([15, 7])
  tree = [[3], [9, 20], [15, 7]]


=================== EXIT ===================
  que is now empty, so the while loop stops
  return tree

Final Output: [[3], [9, 20], [15, 7]]
```

<br><br>

## Related Problems

* [Binary Tree Level Order Traversal II (107)](https://leetcode.com/problems/binary-tree-level-order-traversal-ii/)
* [Binary Tree Zigzag Level Order Traversal (103)](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/)
* [Average of Levels in Binary Tree (637)](https://leetcode.com/problems/average-of-levels-in-binary-tree/)
* [Binary Tree Right Side View (199)](https://leetcode.com/problems/binary-tree-right-side-view/)
* [Find Largest Value in Each Tree Row (515)](https://leetcode.com/problems/find-largest-value-in-each-tree-row/)
* [N-ary Tree Level Order Traversal (429)](https://leetcode.com/problems/n-ary-tree-level-order-traversal/)
* [Maximum Depth of Binary Tree (104)](https://leetcode.com/problems/maximum-depth-of-binary-tree/)