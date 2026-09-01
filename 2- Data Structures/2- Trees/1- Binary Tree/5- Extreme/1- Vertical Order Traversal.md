# Vertical Order Traversal of a Binary Tree

`Meta` • `Amazon` • `Google` • `Microsoft`

## Problem Statement

Given the `root` of a binary tree, return its **vertical order traversal**.

* Every node sits at a position `(row, col)`.
* The root starts at `(0, 0)`.
* For a node at `(row, col)`:
  * its left child goes to `(row + 1, col - 1)`
  * its right child goes to `(row + 1, col + 1)`

We read the tree **column by column, from the leftmost column to the rightmost column**. Inside one column we read **top to bottom**. If two nodes land on the exact same spot (same row and same column), the one with the **smaller value** comes first.

## Examples

**Example 1**

```
Input: root = [3,9,20,null,null,15,7]
Output: [[9],[3,15],[20],[7]]

Column -1: only node 9.
Column  0: node 3 (top) then node 15.
Column  1: only node 20.
Column  2: only node 7.
```

**Example 2**

```
Input: root = [1,2,3,4,5,6,7]
Output: [[4],[2],[1,5,6],[3],[7]]

Column  0: nodes 1, 5, and 6. Node 1 is higher up, so it is first.
           5 and 6 share the same spot, so they are ordered by value.
```

**Example 3**

```
Input: root = [1,2,3,4,6,5,7]
Output: [[4],[2],[1,5,6],[3],[7]]

Same answer as Example 2. Nodes 5 and 6 are in the same location,
so they get sorted by value no matter what order they appear in the input.
```

## Constraints

* The number of nodes in the tree is in the range `[1, 1000]`.
* `0 <= Node.val <= 1000`

<br><br>

## Approach

The whole idea is simple: **give every node an address, then read the addresses in order.**

Think of the tree as sitting on a grid. Each node gets two numbers, a `row` (how deep it is) and a `col` (how far left or right it is). We want to group all nodes that share the same `col`, then print those groups from the leftmost column to the rightmost.

Here is the plan in plain steps:

* Start at the root and give it the address `(row = 0, col = 0)`.
* Walk the tree **level by level** using a queue (this is BFS). Going level by level means we naturally meet nodes from **top to bottom**.
* When we visit a node, drop its `(row, value)` into a bucket labelled with its `col`.
  * Going **left** means `row + 1` and `col - 1`.
  * Going **right** means `row + 1` and `col + 1`.
* Once every node is placed, walk through the buckets from the **smallest col to the largest col**.
* Inside each bucket, **sort** the entries. Then pull out just the values.

<mark>The clever bit is storing each entry as `(row, value)` instead of just the value. When we sort a bucket, Python first compares the `row` (giving us top to bottom), and if two rows are equal it compares the `value` (giving us smaller value first). One sort quietly handles both rules at once.</mark>

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
    def verticalTraversal(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        
        que = deque([(root, 0, 0)]) # (node, row, col)
        cols = defaultdict(list) # Default Value is list

        while que:
            node, row, col = que.popleft()

            cols[col].append((row, node.val))

            if node.left:
                que.append((node.left, row + 1, col - 1))
            if node.right:
                que.append((node.right, row + 1, col + 1))
        
        result = []
        for col in range(min(cols), max(cols) + 1):
            cols[col].sort()
            result.append([val for row, val in cols[col]])
            
        return result
```

<br><br>

## Dry Run

Using `root = [3,9,20,null,null,15,7]` from Example 1.

```ini
Tree shape with (row, col) written next to each node:

              3  (0, 0)
             / \
   (1,-1)  9    20  (1, 1)
               /  \
      (2, 0) 15    7  (2, 2)

Start:
que  = [(3, 0, 0)]
cols = {}

Iteration 1  -> pop (node=3, row=0, col=0)
  put (0, 3) into cols[0]
  3 has left 9  -> push (9, row=1, col=-1)
  3 has right 20 -> push (20, row=1, col=1)
  cols = { 0: [(0,3)] }
  que  = [(9,1,-1), (20,1,1)]

Iteration 2  -> pop (node=9, row=1, col=-1)
  put (1, 9) into cols[-1]
  9 has no children
  cols = { 0: [(0,3)], -1: [(1,9)] }
  que  = [(20,1,1)]

Iteration 3  -> pop (node=20, row=1, col=1)
  put (1, 20) into cols[1]
  20 has left 15 -> push (15, row=2, col=0)
  20 has right 7 -> push (7,  row=2, col=2)
  cols = { 0: [(0,3)], -1: [(1,9)], 1: [(1,20)] }
  que  = [(15,2,0), (7,2,2)]

Iteration 4  -> pop (node=15, row=2, col=0)
  put (2, 15) into cols[0]
  15 has no children
  cols = { 0: [(0,3),(2,15)], -1: [(1,9)], 1: [(1,20)] }
  que  = [(7,2,2)]

Iteration 5  -> pop (node=7, row=2, col=2)
  put (2, 7) into cols[2]
  7 has no children
  cols = { 0: [(0,3),(2,15)], -1: [(1,9)], 1: [(1,20)], 2: [(2,7)] }
  que  = []   (queue empty, BFS done)

Now build the result from smallest col to largest col.
min(cols) = -1 , max(cols) = 2

col = -1 : sort [(1,9)]          -> [(1,9)]           take values -> [9]
col =  0 : sort [(0,3),(2,15)]   -> [(0,3),(2,15)]    take values -> [3,15]
col =  1 : sort [(1,20)]         -> [(1,20)]          take values -> [20]
col =  2 : sort [(2,7)]          -> [(2,7)]           take values -> [7]

Final result = [[9], [3,15], [20], [7]]
```

<br><br>

## Complexity

* **Time:** `O(N log N)`. We visit every node once during BFS, which is `O(N)`. The sorting of the buckets costs `O(N log N)` in total across all columns.
* **Space:** `O(N)`. The queue and the `cols` map together hold all the nodes.

(Here `N` is the number of nodes in the tree.)

<br><br>

## Related Problems

* [Binary Tree Vertical Order Traversal (314)](https://leetcode.com/problems/binary-tree-vertical-order-traversal/)
* [Binary Tree Level Order Traversal (102)](https://leetcode.com/problems/binary-tree-level-order-traversal/)
* [Binary Tree Zigzag Level Order Traversal (103)](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/)
* [Binary Tree Right Side View (199)](https://leetcode.com/problems/binary-tree-right-side-view/)