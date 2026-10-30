# Top View of Binary Tree

`Microsoft` • `Amazon` • `Walmart` • `MakeMyTrip` • `OYO` • `SAP Labs`

## Problem Statement

Given the `root` of a binary tree, return the **top view** of the binary tree.

The top view of a binary tree is the set of nodes visible when the tree is observed from above.

- Return the values of these nodes ordered from the leftmost to the rightmost position.
- If multiple nodes share the same horizontal distance from the root, only the node that appears first when traversing from left to right (the topmost one) should be included in the result.

## Examples

**Example 1**

```ini
Input  : root = [1, 2, 3, 4, 5, 6, 7]
Output : [4, 2, 1, 3, 7]
```

**Example 2**

```ini
Input  : root = [10, 20, 30, 40, 60, 90, 100]
Output : [40, 20, 10, 30, 100]
```

## Constraints

- `1 <= Number of Nodes <= 10^4`
- `-10^3 <= Node.val <= 10^3`

<br><br>

## Approach

Picture the tree standing in front of you and imagine you are looking straight down at it from the sky. From up there you can only see the node that sits highest on each vertical line. Every node sitting below it on the same line is blocked from your eyes. Those top-most nodes, read from left to right, are the answer.

To turn this picture into code, we lean on two very simple ideas:

- **Give every node a column number.** The root sits at column `0`. Every time we step into a left child the column goes down by `1`, and every time we step into a right child the column goes up by `1`. Nodes that stack on the same vertical line all share the same column number.

- **On each column, only the first node we meet from the top is visible.** So we walk the tree level by level from top to bottom (this is BFS using a queue). The moment a column is seen for the very first time, that node is the one visible from the top, so we lock it in. If we bump into the same column again later (a node sitting lower down), we simply ignore it.

<mark>The reason BFS is the key here is that it always finishes an upper level before it touches the lower level, so the first node to claim a column is guaranteed to be the highest one on that line.</mark>

The whole thing in plain steps:

- Put the root into a queue along with its column `0`.
- Keep a map that remembers `column : first node value seen on that column`.
- Take a node out of the front of the queue. If its column is new, save its value in the map.
- Push its left child with `column - 1` and its right child with `column + 1`.
- Repeat until the queue is empty.
- At the end, sort the map by column from smallest (leftmost) to largest (rightmost) and read out the values in that order.

That is the entire idea. One clean sweep from top to bottom, and the first visitor to each column wins.

<br><br>

## Code

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.data = val
#         self.left = left
#         self.right = right

class Solution:
    def topView(self, root):
        if not root:
            return []

        que = deque([(root, 0)])
        top_view_map = {}

        while que:
            node, col = que.popleft()
            if col not in top_view_map:
                top_view_map[col] = node.data

            if node.left:
                que.append((node.left, col - 1))
            if node.right:
                que.append((node.right, col + 1))

        top_view_map = dict(sorted(top_view_map.items()))
        return [node for _, node in top_view_map.items()]
```

<br><br>

## Dry Run

```ini
Input : root = [1, 2, 3, 4, 5, 6, 7]

Tree shape (col = column number):

                 1   (col 0)
               /   \
       (col -1) 2     3 (col +1)
             /  \    /  \
      (-2) 4    5  6     7 (+2)
               (0)(0)

We track:
  que          -> queue holding (node, col)
  top_view_map -> column : first node value seen

Start:
  que          = [(1, 0)]
  top_view_map = {}

Iteration 1:
  pop (1, 0)
  col 0 is NEW   -> top_view_map[0] = 1
  push left  2 with col -1
  push right 3 with col +1
  que          = [(2, -1), (3, +1)]
  top_view_map = {0: 1}

Iteration 2:
  pop (2, -1)
  col -1 is NEW  -> top_view_map[-1] = 2
  push left  4 with col -2
  push right 5 with col  0
  que          = [(3, +1), (4, -2), (5, 0)]
  top_view_map = {0: 1, -1: 2}

Iteration 3:
  pop (3, +1)
  col +1 is NEW  -> top_view_map[1] = 3
  push left  6 with col  0
  push right 7 with col +2
  que          = [(4, -2), (5, 0), (6, 0), (7, +2)]
  top_view_map = {0: 1, -1: 2, 1: 3}

Iteration 4:
  pop (4, -2)
  col -2 is NEW  -> top_view_map[-2] = 4
  node 4 has no children
  que          = [(5, 0), (6, 0), (7, +2)]
  top_view_map = {0: 1, -1: 2, 1: 3, -2: 4}

Iteration 5:
  pop (5, 0)
  col 0 already exists -> skip (node 5 is hidden)
  node 5 has no children
  que          = [(6, 0), (7, +2)]
  top_view_map = {0: 1, -1: 2, 1: 3, -2: 4}

Iteration 6:
  pop (6, 0)
  col 0 already exists -> skip (node 6 is hidden)
  node 6 has no children
  que          = [(7, +2)]
  top_view_map = {0: 1, -1: 2, 1: 3, -2: 4}

Iteration 7:
  pop (7, +2)
  col +2 is NEW  -> top_view_map[2] = 7
  node 7 has no children
  que          = []
  top_view_map = {0: 1, -1: 2, 1: 3, -2: 4, 2: 7}

Queue is empty -> stop.

Sort the map by column (small to large):
  {-2: 4, -1: 2, 0: 1, 1: 3, 2: 7}

Read the values from left to right:
  Output = [4, 2, 1, 3, 7]
```

<br><br>

## Complexity Analysis

- **Time:** `O(N log N)`. We visit each node exactly once during BFS (`O(N)`), and at the end we sort the columns (`O(N log N)`).
- **Space:** `O(N)`. The queue and the map can each hold up to `N` entries.

<br><br>

## Related Problems

- [Binary Tree Right Side View (199)](https://leetcode.com/problems/binary-tree-right-side-view/)
- [Binary Tree Level Order Traversal (102)](https://leetcode.com/problems/binary-tree-level-order-traversal/)
- [Binary Tree Vertical Order Traversal (314)](https://leetcode.com/problems/binary-tree-vertical-order-traversal/)
- [Vertical Order Traversal of a Binary Tree (987)](https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree/)