# Binary Tree Inorder Traversal

`Amazon` • `Microsoft` • `Apple` • `Bloomberg` • `Adobe` • `Meta` • `Google` • `Uber`

## Problem Statement
Given the `root` of a binary tree, return the inorder traversal of its nodes' values.

Inorder traversal means we visit the nodes in this exact order for every node in the tree:

* First go to the **Left** side
* Then take the **Node** itself (its value)
* Then go to the **Right** side

<mark>The golden rule to remember for life: Left, Root, Right (in that order, always).</mark>

## Examples
**Example 1:**
Input: `root = [1,null,2,3]`
Output: `[1,3,2]`

**Example 2:**
Input: `root = [1,2,3,4,5,null,8,null,null,6,7,9]`
Output: `[4,2,6,5,7,1,3,9,8]`

**Example 3:**
Input: `root = []`
Output: `[]`

**Example 4:**
Input: `root = [1]`
Output: `[1]`

## Constraints
* The number of nodes in the tree is in the range `[0, 100]`.
* `-100 <= Node.val <= 100`

<br><br>

## Approach
The whole idea rests on one simple sentence: **for any node, finish the left side first, then use the node, then finish the right side.**

We follow that same rule again and again, even for the small nodes deep inside the tree. This "same rule at every node" is exactly why recursion fits so naturally here.

Here is the plan in plain words:

* We keep an empty list called `tree`. This is where our answer will slowly build up.
* We start at the `root` and try to go as far **left** as we can, because in inorder the left side must always be finished first.
* When there is nothing more on the left (we hit a `None`), we simply stop and come back. There is nothing to record for an empty spot.
* The moment the left side of a node is fully done, we **record that node's value** by adding it into `tree`.
* Only after the node's value is recorded do we turn our attention to its **right** side and repeat the very same steps there.

<mark>The trick is trust: when we call the function on the left child, we trust it to fully handle the entire left subtree before returning. We do not worry about how, we only trust that it will.</mark>

So every node in the tree gets touched exactly once, and because we always drain the left before recording and the right after recording, the values naturally come out in the correct sorted-by-position order.

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
    def inOrder(self, node, tree):
        if node == None:
            return
        
        self.inOrder(node.left, tree)
        tree.append(node.val)
        self.inOrder(node.right, tree)

    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        tree = []
        self.inOrder(root, tree)
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
We call inOrder(node=1, tree)
```

Now let us trace every single step. Read it top to bottom like a story:

```ini
Step 1 : inOrder(node = 1)
         node is 1, not None, so we continue.
         Go LEFT first  -> call inOrder(node = 1.left = None)

Step 2 : inOrder(node = None)
         node is None, so we just return (nothing to do).
         We come back to node 1.

Step 3 : Back at node 1, left side is finished.
         Record the value -> tree.append(1)
         tree = [1]

Step 4 : Now go RIGHT of node 1 -> call inOrder(node = 1.right = 2)

Step 5 : inOrder(node = 2)
         node is 2, not None, so we continue.
         Go LEFT first  -> call inOrder(node = 2.left = 3)

Step 6 : inOrder(node = 3)
         node is 3, not None, so we continue.
         Go LEFT first  -> call inOrder(node = 3.left = None)

Step 7 : inOrder(node = None)
         node is None, so we just return.
         We come back to node 3.

Step 8 : Back at node 3, left side is finished.
         Record the value -> tree.append(3)
         tree = [1, 3]

Step 9 : Now go RIGHT of node 3 -> call inOrder(node = 3.right = None)

Step 10: inOrder(node = None)
         node is None, so we just return.
         Node 3 is now fully done. We come back to node 2.

Step 11: Back at node 2, left side (which was node 3) is finished.
         Record the value -> tree.append(2)
         tree = [1, 3, 2]

Step 12: Now go RIGHT of node 2 -> call inOrder(node = 2.right = None)

Step 13: inOrder(node = None)
         node is None, so we just return.
         Node 2 is now fully done. We come back to node 1.

Step 14: Node 1 is now fully done (left, itself, right all handled).
         Recursion ends.

Final answer -> tree = [1, 3, 2]
```

<mark>Notice how the value is recorded only after the left side is completely emptied, which is why 3 comes before 2, and both come after 1's left (which was empty).</mark>

<br><br>

## Related Problems
* [Binary Tree Preorder Traversal (144)](https://leetcode.com/problems/binary-tree-preorder-traversal/)
* [Binary Tree Postorder Traversal (145)](https://leetcode.com/problems/binary-tree-postorder-traversal/)
* [Binary Search Tree Iterator (173)](https://leetcode.com/problems/binary-search-tree-iterator/)
* [Kth Smallest Element in a BST (230)](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)
* [Validate Binary Search Tree (98)](https://leetcode.com/problems/validate-binary-search-tree/)
* [Construct Binary Tree from Preorder and Inorder Traversal (105)](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)