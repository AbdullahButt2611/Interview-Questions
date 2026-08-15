# Maximum Depth of Binary Tree

`Facebook` • `Walmart` • `Red Hat` • `Adobe`

## Problem Statement

Given the `root` of a binary tree, return its **maximum depth**.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

## Examples

**Example 1:**

```
Input: root = [3,9,20,null,null,15,7]
Output: 3
```

**Example 2:**

```
Input: root = [1,null,2]
Output: 2
```

## Constraints

* The number of nodes in the tree is in the range `[0, 10^4]`.
* `-100 <= Node.val <= 100`

<br><br>

## Approach

The whole idea here is very simple once you look at it the right way.

The depth of any tree is just **1 (for the node you are standing on) plus the depth of its deeper side**. That single sentence is the entire solution.

Here is the thinking, step by step:

* First, look at the current node.
* If the current node is empty (`None`), there is nothing here to count, so its depth is `0`. This is our stopping point (the base case).
* If the node exists, we ask the same question to its **left child**: how deep are you?
* Then we ask the same question to its **right child**: how deep are you?
* Both children answer with a number. We pick the **bigger** of the two, because we only care about the longest path.
* Finally, we add `1` to that bigger number to count the current node itself, and we hand that answer back up to whoever asked us.

<mark>Every node trusts its children to do the counting for it, and only adds itself on top.</mark> That trust is what makes recursion feel natural here. You never manually walk the whole tree, you just keep asking the same tiny question until you hit the empty ends.

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
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root == None: return 0

        left = self.maxDepth(root.left)
        right = self.maxDepth(root.right)

        return 1 + max(left, right)
```

<br><br>

## Dry Run

We will use the tree from **Example 1**: `root = [3,9,20,null,null,15,7]`

```ini
Tree shape:

          3
         / \
        9   20
           /  \
          15   7

We call maxDepth(3) and it slowly unfolds. Read from top to bottom.

Iteration 1  -> maxDepth(3)
   root = 3  (not None, so we keep going)
   We need left  = maxDepth(9)   -> paused, go compute it
   We need right = maxDepth(20)  -> will compute after left is done

Iteration 2  -> maxDepth(9)
   root = 9  (not None)
   left  = maxDepth(None) -> root is None, returns 0
   right = maxDepth(None) -> root is None, returns 0
   return 1 + max(0, 0) = 1
   So maxDepth(9) = 1  (this goes back to node 3 as its left)

Iteration 3  -> maxDepth(20)
   root = 20 (not None)
   We need left  = maxDepth(15) -> paused, go compute it
   We need right = maxDepth(7)  -> will compute after left is done

Iteration 4  -> maxDepth(15)
   root = 15 (not None)
   left  = maxDepth(None) -> returns 0
   right = maxDepth(None) -> returns 0
   return 1 + max(0, 0) = 1
   So maxDepth(15) = 1  (this goes back to node 20 as its left)

Iteration 5  -> maxDepth(7)
   root = 7  (not None)
   left  = maxDepth(None) -> returns 0
   right = maxDepth(None) -> returns 0
   return 1 + max(0, 0) = 1
   So maxDepth(7) = 1  (this goes back to node 20 as its right)

Back to Iteration 3  -> finish maxDepth(20)
   left  = 1  (from node 15)
   right = 1  (from node 7)
   return 1 + max(1, 1) = 2
   So maxDepth(20) = 2  (this goes back to node 3 as its right)

Back to Iteration 1  -> finish maxDepth(3)
   left  = 1  (from node 9)
   right = 2  (from node 20)
   return 1 + max(1, 2) = 3

Final Answer = 3
```

<br><br>

## Complexity

* **Time Complexity:** `O(n)`, where `n` is the number of nodes. We visit every node exactly once.
* **Space Complexity:** `O(h)`, where `h` is the height of the tree. This is the space used by the recursion call stack. In the worst case (a skewed tree) it becomes `O(n)`, and in the best case (a balanced tree) it becomes `O(log n)`.

<br><br>

## Related Problems

* [Minimum Depth of Binary Tree (111)](https://leetcode.com/problems/minimum-depth-of-binary-tree/)
* [Balanced Binary Tree (110)](https://leetcode.com/problems/balanced-binary-tree/)
* [Diameter of Binary Tree (543)](https://leetcode.com/problems/diameter-of-binary-tree/)
* [Maximum Depth of N-ary Tree (559)](https://leetcode.com/problems/maximum-depth-of-n-ary-tree/)
* [Same Tree (100)](https://leetcode.com/problems/same-tree/)