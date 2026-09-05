# Bottom View of Binary Tree

`Microsoft` • `Amazon` • `OYO` • `PayU` • `Policybazaar`

## Problem Statement

Given the `root` of a binary tree, return the bottom view of the binary tree.

The bottom view is the set of nodes you can see when you look at the tree from directly below. Return the nodes from the leftmost position to the rightmost position.

If two nodes fall at the exact same position and both would be visible from the bottom, pick the one that appears later in the level order traversal (the one more towards the right or deeper).

## Examples

**Example 1**

```ini
Input  : root = [20, 8, 22, 5, 3, null, 25, null, null, 10, 14]
Output : [5, 10, 3, 14, 25]
```

Explanation (from left to right):

* First we see node `5`.
* Then we have `8` and `10`, but from the bottom only `10` is visible.
* Next we have `20` and `3`, but from the bottom only `3` is visible.
* Next we have `14` and `22`, but from the bottom only `14` is visible.
* Finally we see node `25`.

**Example 2**

```ini
Input  : root = [20, 8, 22, 5, 3, 4, 25, null, null, 10, 14]
Output : [5, 10, 4, 14, 25]
```

Explanation (from left to right):

* First we see node `5`.
* Then we have `8` and `10`, but from the bottom only `10` is visible.
* Next we have `20`, `3` and `4`. Both `3` and `4` sit at the same position, but `4` comes later in the traversal, so only `4` is kept.
* Next we have `14` and `22`, but from the bottom only `14` is visible.
* Finally we see node `25`.

## Constraints

* `1 <= Number of Nodes <= 10^4`
* `-10^3 <= Node.val <= 10^3`

<br><br>

## Intuition

Imagine standing right under the tree and looking straight up. Nodes that share the same vertical line stack on top of each other, and the one at the very bottom is the only one you can see.

So the whole problem is really about grouping nodes by their vertical line, and for each line keeping the node that ends up at the bottom.

To label each vertical line we give every node a column number:

* The root sits at column `0`.
* Every time we go left, the column goes down by `1`.
* Every time we go right, the column goes up by `1`.

Nodes with the same column number lie on the same vertical line.

<br><br>

## Approach

We walk through the tree level by level (top to bottom, left to right). This is a normal BFS using a queue. Along with each node, we also carry its column number.

While we walk, we keep a map where the key is the column number and the value is the node value sitting on that column.

The trick is simple: every time we reach a node, we just overwrite whatever value was already stored for that column.

Why does overwriting work so nicely?

* Because we move top to bottom, any node we visit later on a column is lower than the one before it.
* And within the same level, we move left to right, so a node visited later on a column is more towards the right.
* So the last value written to a column is exactly the bottom-most, right-most node, which is precisely what the bottom view wants.

Once the traversal is done, the map holds the answer, one value per column. The only thing left is ordering. Columns can be negative (left side) or positive (right side), so we sort the column keys from smallest to largest and read off the values. That gives us the nodes from leftmost to rightmost.

Step by step in plain words:

* If the tree is empty, return an empty list.
* Put the root in the queue with column `0`.
* Keep pulling one node out of the front of the queue:
  * Store (or overwrite) its value in the map under its column.
  * Push its left child with `column - 1`.
  * Push its right child with `column + 1`.
* When the queue is empty, sort the columns and collect the values in that order.

<mark>The one idea to never forget: last write wins per column, because BFS guarantees the last write is always the lowest and rightmost node on that line.</mark>

<br><br>

## Dry Run

We will use Example 1.

```ini
Tree structure:

              20  (col 0)
            /    \
         8 (-1)   22 (+1)
        /   \        \
     5(-2)  3(0)     25(+2)
            /  \
        10(-1) 14(+1)

Start:
  queue = [ (20, 0) ]
  map   = { }

Iteration 1:
  pop (20, 0)
  map[0] = 20              -> map = { 0:20 }
  push left  (8,  -1)
  push right (22, +1)
  queue = [ (8,-1), (22,+1) ]

Iteration 2:
  pop (8, -1)
  map[-1] = 8             -> map = { 0:20, -1:8 }
  push left  (5, -2)
  push right (3,  0)
  queue = [ (22,+1), (5,-2), (3,0) ]

Iteration 3:
  pop (22, +1)
  map[+1] = 22           -> map = { 0:20, -1:8, 1:22 }
  no left child
  push right (25, +2)
  queue = [ (5,-2), (3,0), (25,+2) ]

Iteration 4:
  pop (5, -2)
  map[-2] = 5           -> map = { 0:20, -1:8, 1:22, -2:5 }
  no children
  queue = [ (3,0), (25,+2) ]

Iteration 5:
  pop (3, 0)
  map[0] = 3   (overwrites 20, because 3 is lower on column 0)
                       -> map = { 0:3, -1:8, 1:22, -2:5 }
  push left  (10, -1)
  push right (14, +1)
  queue = [ (25,+2), (10,-1), (14,+1) ]

Iteration 6:
  pop (25, +2)
  map[+2] = 25         -> map = { 0:3, -1:8, 1:22, -2:5, 2:25 }
  no children
  queue = [ (10,-1), (14,+1) ]

Iteration 7:
  pop (10, -1)
  map[-1] = 10  (overwrites 8, because 10 is lower on column -1)
                       -> map = { 0:3, -1:10, 1:22, -2:5, 2:25 }
  no children
  queue = [ (14,+1) ]

Iteration 8:
  pop (14, +1)
  map[+1] = 14  (overwrites 22, because 14 is lower on column +1)
                       -> map = { 0:3, -1:10, 1:14, -2:5, 2:25 }
  no children
  queue = [ ]

Queue is empty. Stop.

Sort columns:   -2,  -1,   0,   1,   2
Read values:     5,  10,   3,  14,  25

Final answer = [5, 10, 3, 14, 25]
```

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
    def bottomView(self, root):
        if root == None:
            return []

        que = deque([(root, 0)])
        bottom_view_map = {}

        while que:
            node, col = que.popleft()
            bottom_view_map[col] = node.data

            if node.left:
                que.append((node.left, col - 1))
            if node.right:
                que.append((node.right, col + 1))

        bottom_view = []
        for col in sorted(bottom_view_map.keys()):
            bottom_view.append(bottom_view_map[col])
        return bottom_view
```

<br><br>

## Complexity

* **Time:** `O(N log N)`, where `N` is the number of nodes. We visit each node once during BFS, and the sorting of columns at the end costs the log factor.
* **Space:** `O(N)`, for the queue and the map that can hold up to `N` entries.

<br><br>

## Related Problems

* [Binary Tree Right Side View (199)](https://leetcode.com/problems/binary-tree-right-side-view/)
* [Binary Tree Level Order Traversal (102)](https://leetcode.com/problems/binary-tree-level-order-traversal/)
* [Vertical Order Traversal of a Binary Tree (987)](https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree/)
* [Binary Tree Vertical Order Traversal (314)](https://leetcode.com/problems/binary-tree-vertical-order-traversal/)