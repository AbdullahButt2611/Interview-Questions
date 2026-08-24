# Diameter of Binary Tree

`Meta` • `Amazon` • `Google` • `Microsoft` • `Adobe` • `PhonePe`

## Problem Statement

Given the `root` of a binary tree, return the length of the **diameter** of the tree.

- The diameter of a binary tree is the length of the longest path between any two nodes in the tree.
- This path may or may not pass through the root.
- The length of a path is measured by the **number of edges** between the two nodes (not the number of nodes).

## Examples

**Example 1:**

```ini
Input: root = [1,2,3,4,5]
Output: 3
Explanation: 3 is the length of the path [4,2,1,3] or [5,2,1,3].
```

**Example 2:**

```ini
Input: root = [1,2]
Output: 1
```

## Constraints

- The number of nodes in the tree is in the range `[1, 10^4]`.
- `-100 <= Node.val <= 100`

<br><br>

## Intuition

Think about the longest path in the tree. That path always "bends" at exactly one node (its highest point). At that bending node, the path goes down into the left side as far as it can, and down into the right side as far as it can.

So here is the whole idea in one line:

<mark>For any node, the longest path that bends at it = (how deep the left side goes) + (how deep the right side goes).</mark>

- "How deep a side goes" is just the **height** of that side, counted in edges.
- If we do this check at **every** node and remember the biggest value, that biggest value is our answer.

The path may bend at the root, or deep inside a subtree. That is fine. Since we check every single node, whichever node the true longest path bends at will be caught.

<br><br>

## Approach

We solve two things at the same time in one pass through the tree:

1. **The height of each node** (how far down it can reach), and
2. **The best diameter we have seen so far** (stored in a shared box so all calls can update it).

We go from the bottom of the tree upward (post-order). At each node we do the following in plain steps:

- If the node is empty (`None`), its height is `0`. An empty branch adds no edges, so we simply return `0`.
- Otherwise, first find the height of the **left child**, call it `lh`.
- Then find the height of the **right child**, call it `rh`.
- The longest path bending at this node is `lh + rh` edges. Compare it with our stored best diameter and keep the larger one.
- Finally, tell the parent how tall **this** node is. Its height is `1 + max(lh, rh)`, because we take the taller of the two sides and add one edge for the step up to this node.

Why the shared box (`diameter = [0]`)? Each call has to **return the height** to its parent, but the answer we actually want is the diameter. These are two different numbers. So instead of returning the diameter, we keep updating it inside a shared list that every call can reach. A list is used because it can be changed in place from inside the recursion.

When the top call finishes, every node has been visited once, every possible bend has been checked, and the box holds the biggest path we found. That is the diameter.

- **Time Complexity:** `O(n)`, since we visit each of the `n` nodes exactly once.
- **Space Complexity:** `O(h)`, where `h` is the height of the tree, used by the recursion call stack. In the worst case (a skewed tree) this becomes `O(n)`.

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
    def heightOfBinaryTree(self, node, diameter):
        if node == None:
            return 0
        
        lh = self.heightOfBinaryTree(node.left, diameter)
        rh = self.heightOfBinaryTree(node.right, diameter)

        diameter[0] = max(diameter[0], lh + rh)

        return 1 + max(lh, rh)
    
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        diameter = [0]
        self.heightOfBinaryTree(root, diameter)
        return diameter[0]
```

<br><br>

## Dry Run

We use the tree from Example 1: `root = [1,2,3,4,5]`

```ini
Tree shape:

          1
         / \
        2   3
       / \
      4   5

We call heightOfBinaryTree on each node from the bottom up (post-order).
"diameter" starts as [0] (a shared box every call can update).

Iteration 1  -> visit node 4
  left child  = None  -> height 0
  right child = None  -> height 0
  path bending here = lh + rh = 0 + 0 = 0
  diameter[0] = max(0, 0) = 0
  return height = 1 + max(0, 0) = 1        (node 4 is 1 tall)

Iteration 2  -> visit node 5
  left child  = None  -> height 0
  right child = None  -> height 0
  path bending here = lh + rh = 0 + 0 = 0
  diameter[0] = max(0, 0) = 0
  return height = 1 + max(0, 0) = 1        (node 5 is 1 tall)

Iteration 3  -> visit node 2
  lh = height of node 4 = 1
  rh = height of node 5 = 1
  path bending here = lh + rh = 1 + 1 = 2
  diameter[0] = max(0, 2) = 2
  return height = 1 + max(1, 1) = 2        (node 2 is 2 tall)

Iteration 4  -> visit node 3
  left child  = None  -> height 0
  right child = None  -> height 0
  path bending here = lh + rh = 0 + 0 = 0
  diameter[0] = max(2, 0) = 2
  return height = 1 + max(0, 0) = 1        (node 3 is 1 tall)

Iteration 5  -> visit node 1 (root)
  lh = height of node 2 = 2
  rh = height of node 3 = 1
  path bending here = lh + rh = 2 + 1 = 3
  diameter[0] = max(2, 3) = 3
  return height = 1 + max(2, 1) = 3        (node 1 is 3 tall)

All nodes visited. Final answer = diameter[0] = 3

The winning path bends at node 1: it goes 4 -> 2 -> 1 -> 3 (3 edges).
```

<br><br>

## Related Problems

- [Maximum Depth of Binary Tree (104)](https://leetcode.com/problems/maximum-depth-of-binary-tree/)
- [Balanced Binary Tree (110)](https://leetcode.com/problems/balanced-binary-tree/)
- [Binary Tree Maximum Path Sum (124)](https://leetcode.com/problems/binary-tree-maximum-path-sum/)
- [Longest Univalue Path (687)](https://leetcode.com/problems/longest-univalue-path/)