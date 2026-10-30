# Binary Tree Zigzag Level Order Traversal

`Amazon` • `Microsoft` • `Facebook` • `Google` • `LinkedIn` • `Apple` • `Samsung` • `Walmart`

## Problem Statement
Given the `root` of a binary tree, return the zigzag level order traversal of its nodes' values.

This means we read the tree one level at a time, but we keep flipping the direction:

* Level 1: left to right
* Level 2: right to left
* Level 3: left to right
* and so on, alternating each time.

## Examples

```ini
Input:  root = [3,9,20,null,null,15,7]
Output: [[3],[20,9],[15,7]]
```

```ini
Input:  root = [1]
Output: [[1]]
```

```ini
Input:  root = []
Output: []
```

## Constraints

* The number of nodes in the tree is in the range `[0, 2000]`.
* `-100 <= Node.val <= 100`

<br><br>

## Approach

The core idea is simple: this is just a normal level by level walk (BFS) of the tree, and the only extra thing we do is decide the order in which we place the values of each level.

Here is the thinking, step by step:

* We visit the tree level by level. To do this, we keep a queue. We start by putting the `root` inside it.

* At the start of every level, we check how many nodes are currently waiting in the queue. That count is exactly the number of nodes on this level, so we save it in `size`.

* We create a fixed size list called `level` with `size` empty slots. We will fill these slots one by one.

* Now the small trick that makes this clean. Instead of collecting values normally and reversing them later, we directly place each value in its correct final slot:
  * When the direction is left to right, the first node goes to slot `0`, the next to slot `1`, and so on. So the slot is simply `i`.
  * When the direction is right to left, the first node should land at the last slot, the next at the second last, and so on. So the slot becomes `size - i - 1`.

* This way we never reverse anything. We just write each value into the right place from the beginning, which keeps the code fast and neat.

* While we take out each node from the front of the queue, we also push its children (left first, then right) to the back of the queue. This keeps the queue ready with the next level for later.

* Once a level is fully processed, we flip the direction flag so the next level goes the opposite way, and we add the finished `level` list to our answer.

* We repeat until the queue is empty, then return the answer.

In one line: do a plain BFS, and for each level choose the write position based on the current direction so no reversing is ever needed.

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
    def levelOrderTraversalVariant(self, root):
        tree = []
        if not root: return tree

        que = deque([root])
        isDirectionLeftToRight = True

        while que:
            size = len(que)
            level = [0] * size

            for i in range(size):
                index = i if isDirectionLeftToRight else size - i - 1

                node = que.popleft()
                level[index] = node.val

                if node.left:
                    que.append(node.left)

                if node.right:
                    que.append(node.right)

            isDirectionLeftToRight = not isDirectionLeftToRight
            tree.append(level)

        return tree

    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        return self.levelOrderTraversalVariant(root)
```

<br><br>

## Dry Run

We will use `root = [3,9,20,null,null,15,7]`, which looks like this:

```ini
        3
       / \
      9   20
         /  \
        15   7
```

```ini
START
tree = []
que  = [3]
isDirectionLeftToRight = True


ITERATION 1  (processing level of node 3)
size  = len(que) = 1
level = [0]          (one empty slot)

  i = 0
    isDirectionLeftToRight is True  -> index = i = 0
    node = que.popleft() = 3        -> que = []
    level[0] = 3                    -> level = [3]
    3 has left child 9   -> que.append(9)   -> que = [9]
    3 has right child 20 -> que.append(20)  -> que = [9, 20]

  flip direction -> isDirectionLeftToRight = False
  tree.append([3])                 -> tree = [[3]]


ITERATION 2  (processing level of nodes 9 and 20)
size  = len(que) = 2
level = [0, 0]       (two empty slots)

  i = 0
    isDirectionLeftToRight is False -> index = size - i - 1 = 2 - 0 - 1 = 1
    node = que.popleft() = 9        -> que = [20]
    level[1] = 9                    -> level = [0, 9]
    9 has no left child
    9 has no right child

  i = 1
    isDirectionLeftToRight is False -> index = size - i - 1 = 2 - 1 - 1 = 0
    node = que.popleft() = 20       -> que = []
    level[0] = 20                   -> level = [20, 9]
    20 has left child 15  -> que.append(15) -> que = [15]
    20 has right child 7  -> que.append(7)  -> que = [15, 7]

  flip direction -> isDirectionLeftToRight = True
  tree.append([20, 9])             -> tree = [[3], [20, 9]]


ITERATION 3  (processing level of nodes 15 and 7)
size  = len(que) = 2
level = [0, 0]       (two empty slots)

  i = 0
    isDirectionLeftToRight is True  -> index = i = 0
    node = que.popleft() = 15       -> que = [7]
    level[0] = 15                   -> level = [15, 0]
    15 has no left child
    15 has no right child

  i = 1
    isDirectionLeftToRight is True  -> index = i = 1
    node = que.popleft() = 7        -> que = []
    level[1] = 7                    -> level = [15, 7]
    7 has no left child
    7 has no right child

  flip direction -> isDirectionLeftToRight = False
  tree.append([15, 7])             -> tree = [[3], [20, 9], [15, 7]]


END
que is empty, so the while loop stops.
return tree = [[3], [20, 9], [15, 7]]
```

<br><br>

## Complexity

* **Time:** `O(n)`, where `n` is the number of nodes. We touch every node exactly once.
* **Space:** `O(n)` for the queue and the output. In the worst case the queue holds one full level of the tree.

<br><br>

## Related Problems

* [Binary Tree Level Order Traversal (102)](https://leetcode.com/problems/binary-tree-level-order-traversal/)
* [Binary Tree Level Order Traversal II (107)](https://leetcode.com/problems/binary-tree-level-order-traversal-ii/)
* [Average of Levels in Binary Tree (637)](https://leetcode.com/problems/average-of-levels-in-binary-tree/)
* [Binary Tree Right Side View (199)](https://leetcode.com/problems/binary-tree-right-side-view/)
* [N-ary Tree Level Order Traversal (429)](https://leetcode.com/problems/n-ary-tree-level-order-traversal/)