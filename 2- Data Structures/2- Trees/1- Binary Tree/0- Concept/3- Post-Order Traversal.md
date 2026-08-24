# Binary Tree Postorder Traversal

`Amazon` • `Microsoft` • `Meta` • `Google` • `Bloomberg` • `Adobe`

## Problem Statement
Given the `root` of a binary tree, return the postorder traversal of its nodes' values.

Postorder traversal means we visit the nodes in this exact order for every node in the tree:

* First go to the **Left** side
* Then go to the **Right** side
* Then take the **Node** itself (its value) last

<mark>The golden rule to remember for life: Left, Right, Root (the node always comes last, only after both its children are fully done).</mark>

## Examples
**Example 1:**
Input: `root = [1,null,2,3]`
Output: `[3,2,1]`

**Example 2:**
Input: `root = [1,2,3,4,5,null,8,null,null,6,7,9]`
Output: `[4,6,7,5,2,9,8,3,1]`

**Example 3:**
Input: `root = []`
Output: `[]`

**Example 4:**
Input: `root = [1]`
Output: `[1]`

## Constraints
* The number of the nodes in the tree is in the range `[0, 100]`.
* `-100 <= Node.val <= 100`

<br><br>

## Approach
The whole idea rests on one simple sentence: **for any node, finish the left side first, then finish the right side, and only then use the node itself.**

We follow that same rule again and again, even for the tiny nodes buried deep in the tree. This "same rule at every node" is exactly why recursion fits so naturally here.

Here is the plan in plain words:

* We keep an empty list called `tree`. This is where our answer will slowly build up.
* We start at the `root` and first dive fully into its **left** side, because in postorder the left must always be finished first.
* When there is nothing there (we hit a `None`), we simply stop and come back. There is nothing to record for an empty spot.
* Once the left side of a node is completely done, we dive fully into its **right** side and finish that too.
* <mark>Only after BOTH the left and the right side are fully finished do we finally record that node's value by adding it into `tree`.</mark>

The key feeling here is patience: a node has to wait for all of its children (and their children) to be handled before it is allowed to be written down.

* This is why the deepest, leftmost leaves show up first in the answer, and the `root` always shows up last.
* Because we always drain the left, then the right, and record the node only at the very end, the values naturally come out in the correct postorder sequence.

* Time Complexity: `O(n)`, because we visit each of the `n` nodes one time.
* Space Complexity: `O(n)`, because of the recursion call stack in the worst case (a skewed tree) plus the output list.

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
    def postOrder(self, node, tree):
        if node == None:
            return
        
        self.postOrder(node.left, tree)
        self.postOrder(node.right, tree)
        tree.append(node.val)

    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        tree = []
        self.postOrder(root, tree)
        return tree
```

<br><br>

## Dry Run
We will use **Example 1**: `root = [1,null,2,3]`

The tree looks like this:

```ini
      1
       \
        2
       /
      3

Node connections:
  1.left  = None      1.right = 2
  2.left  = 3         2.right = None
  3.left  = None      3.right = None

Start: tree = []
We call postOrder(node=1, tree)
```

Now let us trace every single step. Read it top to bottom like a story:

```ini
Step 1 : postOrder(node = 1)
         node is 1, not None, so we continue.
         Go LEFT first  -> call postOrder(node = 1.left = None)

Step 2 : postOrder(node = None)
         node is None, so we just return (nothing to do).
         We come back to node 1.

Step 3 : Back at node 1, left side is finished.
         Now go RIGHT -> call postOrder(node = 1.right = 2)

Step 4 : postOrder(node = 2)
         node is 2, not None, so we continue.
         Go LEFT first  -> call postOrder(node = 2.left = 3)

Step 5 : postOrder(node = 3)
         node is 3, not None, so we continue.
         Go LEFT first  -> call postOrder(node = 3.left = None)

Step 6 : postOrder(node = None)
         node is None, so we just return.
         We come back to node 3.

Step 7 : Back at node 3, left side is finished.
         Now go RIGHT -> call postOrder(node = 3.right = None)

Step 8 : postOrder(node = None)
         node is None, so we just return.
         We come back to node 3.

Step 9 : Node 3 has finished BOTH left and right.
         Now record its value -> tree.append(3)
         tree = [3]
         Node 3 is fully done. We come back to node 2.

Step 10: Back at node 2, left side (which was node 3) is finished.
         Now go RIGHT -> call postOrder(node = 2.right = None)

Step 11: postOrder(node = None)
         node is None, so we just return.
         We come back to node 2.

Step 12: Node 2 has finished BOTH left and right.
         Now record its value -> tree.append(2)
         tree = [3, 2]
         Node 2 is fully done. We come back to node 1.

Step 13: Node 1 has finished BOTH left and right.
         Now record its value -> tree.append(1)
         tree = [3, 2, 1]
         Node 1 is fully done. Recursion ends.

Final answer -> tree = [3, 2, 1]
```

<mark>Notice how every node waits until both of its sides are completely emptied before it is written down, which is why 3 comes first and the root 1 comes last.</mark>

<br><br>

## Related Problems
* [Binary Tree Inorder Traversal (94)](https://leetcode.com/problems/binary-tree-inorder-traversal/)
* [Binary Tree Preorder Traversal (144)](https://leetcode.com/problems/binary-tree-preorder-traversal/)
* [N-ary Tree Postorder Traversal (590)](https://leetcode.com/problems/n-ary-tree-postorder-traversal/)
* [Binary Tree Level Order Traversal (102)](https://leetcode.com/problems/binary-tree-level-order-traversal/)
* [Maximum Depth of Binary Tree (104)](https://leetcode.com/problems/maximum-depth-of-binary-tree/)
* [Construct Binary Tree from Inorder and Postorder Traversal (106)](https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/)