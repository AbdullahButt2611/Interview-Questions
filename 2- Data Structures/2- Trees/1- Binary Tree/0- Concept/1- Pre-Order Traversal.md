# Binary Tree Preorder Traversal

`Amazon` • `Microsoft` • `Google` • `Bloomberg` • `Meta`

## Problem Statement

Given the `root` of a binary tree, return the **preorder traversal** of its nodes' values.

## Examples

**Example 1:**
Input: `root = [1,null,2,3]`
Output: `[1,2,3]`

**Example 2:**
Input: `root = [1,2,3,4,5,null,8,null,null,6,7,9]`
Output: `[1,2,4,5,6,7,3,8,9]`

**Example 3:**
Input: `root = []`
Output: `[]`

**Example 4:**
Input: `root = [1]`
Output: `[1]`

## Constraints

- The number of nodes in the tree is in the range `[0, 100]`.
- `-100 <= Node.val <= 100`

<br><br>

## Approach

The word **preorder** simply tells us the order in which we visit things, and that order never changes for any node:

<mark>Root first, then Left, then Right.</mark>

A nice way to remember it: read yourself out loud first, then always look at your left child before your right child.

Here is the plan in plain steps:

- Keep one empty list called `tree`. This will hold the final answer.
- Start at the root node and do these three things for it:
  - Write down (append) the current node's value into `tree`.
  - Move into the **left** child and do the exact same three things there.
  - Once the whole left side is finished, move into the **right** child and do the same three things.
- If you ever land on an empty spot (a node that is `None`), there is nothing to write, so just stop and step back to where you came from.
- Repeat this until every node has been written down.

Because each node quietly repeats the same steps on its own left and right child, the answer builds itself in the correct Root, Left, Right order without us having to track anything by hand.

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
    def preOrder(self, node, tree):
        if node == None:
            return
        
        tree.append(node.val)
        self.preOrder(node.left, tree)
        self.preOrder(node.right, tree)

    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        tree = []
        self.preOrder(root, tree)
        return tree
```

<br><br>

## Dry Run

```ini
Input: root = [1, null, 2, 3]

Tree shape:
        1
         \
          2
         /
        3

We keep one list called "tree" that stores the answer.
Order we always follow for each node: Root -> Left -> Right


Iteration 1: preOrder(node = 1)
  node is not None
  Append 1                 -> tree = [1]
  Go Left to node 1's left child (None)

Iteration 2: preOrder(node = None)      [left child of 1]
  node is None
  Return back (nothing to do)

Iteration 3: preOrder(node = 2)         [right child of 1]
  node is not None
  Append 2                 -> tree = [1, 2]
  Go Left to node 2's left child (3)

Iteration 4: preOrder(node = 3)         [left child of 2]
  node is not None
  Append 3                 -> tree = [1, 2, 3]
  Go Left to node 3's left child (None)

Iteration 5: preOrder(node = None)      [left child of 3]
  node is None
  Return back (nothing to do)

Iteration 6: preOrder(node = None)      [right child of 3]
  node is None
  Return back (nothing to do)
  Node 3 is fully finished, step back up to node 2

Iteration 7: preOrder(node = None)      [right child of 2]
  node is None
  Return back (nothing to do)
  Node 2 is fully finished, step back up to node 1

  Node 1 is fully finished. Every node has been visited.


Final Answer: tree = [1, 2, 3]
```

<br><br>

## Complexity

- **Time Complexity:** `O(n)`, where `n` is the number of nodes. We touch each node exactly once.
- **Space Complexity:** `O(h)`, where `h` is the height of the tree, used by the recursion call stack. In the worst case of a fully skewed tree (like a straight line), this becomes `O(n)`.

<br><br>

## Related Problems

- [Binary Tree Inorder Traversal (94)](https://leetcode.com/problems/binary-tree-inorder-traversal/)
- [Binary Tree Postorder Traversal (145)](https://leetcode.com/problems/binary-tree-postorder-traversal/)
- [N-ary Tree Preorder Traversal (589)](https://leetcode.com/problems/n-ary-tree-preorder-traversal/)
- [Construct Binary Tree from Preorder and Inorder Traversal (105)](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)
- [Binary Tree Level Order Traversal (102)](https://leetcode.com/problems/binary-tree-level-order-traversal/)