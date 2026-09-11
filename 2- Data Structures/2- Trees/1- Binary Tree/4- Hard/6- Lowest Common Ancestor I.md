# Lowest Common Ancestor of a Binary Tree

`Meta` • `Amazon` • `Google` • `Microsoft` • `Apple` • `LinkedIn` • `Bloomberg`

<br>

## Problem Statement

Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.

According to the [definition of LCA on Wikipedia](https://en.wikipedia.org/wiki/Lowest_common_ancestor): "The lowest common ancestor is defined between two nodes `p` and `q` as the lowest node in `T` that has both `p` and `q` as descendants (where we allow a node to be a descendant of itself)."

## Examples

**Example 1:**

```ini
Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
Output: 3
Explanation: The LCA of nodes 5 and 1 is 3.
```

**Example 2:**

```ini
Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
Output: 5
Explanation: The LCA of nodes 5 and 4 is 5, since a node can be a descendant
             of itself according to the LCA definition.
```

**Example 3:**

```ini
Input: root = [1,2], p = 1, q = 2
Output: 1
```

## Constraints

* The number of nodes in the tree is in the range `[2, 10^5]`
* `-10^9 <= Node.val <= 10^9`
* All `Node.val` are unique
* `p != q`
* `p` and `q` will exist in the tree

<br><br>

## Approach

**The one line idea**

Ask every node a single question: "Did you find `p` or `q` anywhere below you?" The node that hears "yes" from both of its sides is the answer.

<br><br>

**How the search moves**

* We start at the root and go all the way down, first into the left side, then into the right side.
* We do not decide anything on the way down. We only decide on the way back up, once each side has reported what it found.
* Every call sends back one of two things to its parent: a found node, or `None` (nothing found here).

<br><br>

**The four rules every node follows**

* **Empty spot:** if the node is `None`, there is nothing to find here, so report `None`.
* **Direct hit:** if the node is `p` or `q`, report that node right away and stop digging deeper.
* **Both sides reported something:** `p` came from one side and `q` from the other, so the two paths meet exactly here. This node is the answer, so report itself.
* **Only one side reported something:** both nodes must live on that one side, so just pass that report upward unchanged.

<br><br>

**Why we can stop at a direct hit**

Suppose we land on `p`, and `q` is sitting somewhere below `p`. We never search below to find `q`, and we do not need to. Since `p` is already an ancestor of `q`, and a node counts as its own descendant, `p` itself is the answer.

<mark>Stopping early is safe because the answer in that case is the node we just landed on, so digging deeper could never give us a lower valid ancestor.</mark>

<br><br>

**Why the answer never gets lost on the way up**

Once the meeting node reports itself, every node above it sees a report from only one side, so the rule "pass the single report upward" carries that same node all the way to the root untouched. The first node that ever sees reports from both sides is the lowest one, because we are travelling upward from the bottom.

<br><br>

## Code

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if root == None or root.val == p.val or root.val == q.val:
            return root
        
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        
        if left == None:
            return right
        elif right == None:
            return left
        else:
            return root
```

<br><br>

## Dry Run

```ini
Tree used (same tree as the examples):

              3
            /   \
           5     1
          / \   / \
         6   2 0   8
            / \
           7   4

Input : p = 6, q = 4        (chosen so that every rule of the code gets used)
Goal  : find the lowest node that has both 6 and 4 under it

Iteration 1  -> call LCA(3)
   node 3 is not None, 3 != 6, 3 != 4
   so we must ask both sides, we go left first
   status: waiting for left = LCA(5)

Iteration 2  -> call LCA(5)
   node 5 is not None, 5 != 6, 5 != 4
   we go left first
   status: waiting for left = LCA(6)

Iteration 3  -> call LCA(6)
   node 6 matches p
   direct hit, return node 6 immediately (we do not look below)
   RETURN 6  -> this becomes left of node 5

Iteration 4  -> back at node 5
   left  = 6
   now we go right
   status: waiting for right = LCA(2)

Iteration 5  -> call LCA(2)
   node 2 is not None, 2 != 6, 2 != 4
   we go left first
   status: waiting for left = LCA(7)

Iteration 6  -> call LCA(7)
   node 7 is not None, 7 != 6, 7 != 4
   we go left first
   status: waiting for left = LCA(None)

Iteration 7  -> call LCA(None)      (left child of 7)
   node is None
   RETURN None  -> this becomes left of node 7

Iteration 8  -> call LCA(None)      (right child of 7)
   node is None
   RETURN None  -> this becomes right of node 7

Iteration 9  -> back at node 7
   left = None, right = None
   rule used: left is None, so return right
   RETURN None  -> this becomes left of node 2

Iteration 10 -> back at node 2
   left  = None
   now we go right
   status: waiting for right = LCA(4)

Iteration 11 -> call LCA(4)
   node 4 matches q
   direct hit, return node 4 immediately
   RETURN 4  -> this becomes right of node 2

Iteration 12 -> back at node 2
   left = None, right = 4
   rule used: left is None, so pass the single report upward
   RETURN 4  -> this becomes right of node 5

Iteration 13 -> back at node 5
   left = 6, right = 4
   both sides reported something, the two paths meet here
   rule used: neither side is None, so return the node itself
   RETURN 5  -> this becomes left of node 3

Iteration 14 -> back at node 3
   left  = 5
   now we go right
   status: waiting for right = LCA(1)

Iteration 15 -> call LCA(1)
   node 1 is not None, 1 != 6, 1 != 4
   we go left first
   status: waiting for left = LCA(0)

Iteration 16 -> call LCA(0)
   node 0 is not None, 0 != 6, 0 != 4
   its left child is None  -> returns None
   its right child is None -> returns None
   left is None, so return right
   RETURN None  -> this becomes left of node 1

Iteration 17 -> call LCA(8)
   node 8 is not None, 8 != 6, 8 != 4
   its left child is None  -> returns None
   its right child is None -> returns None
   left is None, so return right
   RETURN None  -> this becomes right of node 1

Iteration 18 -> back at node 1
   left = None, right = None
   left is None, so return right
   RETURN None  -> this becomes right of node 3

Iteration 19 -> back at node 3
   left = 5, right = None
   rule used: right is None, so pass the single report upward
   RETURN 5

Final answer: node 5
Check: node 5 has 6 on its left side and 4 under its right side, and no node
       lower than 5 holds both, so 5 is the lowest common ancestor.
```

<br><br>

## Complexity Analysis

* **Time:** `O(n)`, because in the worst case we touch every node once.
* **Space:** `O(h)` for the recursion stack, where `h` is the height of the tree. This becomes `O(n)` for a completely skewed tree and `O(log n)` for a balanced one.

<br><br>

## Related Problems

* [Lowest Common Ancestor of a Binary Tree II (1644)](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-ii/)
* [Lowest Common Ancestor of a Binary Tree III (1650)](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-iii/)
* [Lowest Common Ancestor of a Binary Tree IV (1676)](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-iv/)
* [Lowest Common Ancestor of Deepest Leaves (1123)](https://leetcode.com/problems/lowest-common-ancestor-of-deepest-leaves/)
* [Smallest Subtree with all the Deepest Nodes (865)](https://leetcode.com/problems/smallest-subtree-with-all-the-deepest-nodes/)
* [Step-By-Step Directions From a Binary Tree Node to Another (2096)](https://leetcode.com/problems/step-by-step-directions-from-a-binary-tree-node-to-another/)
* [Binary Tree Maximum Path Sum (124)](https://leetcode.com/problems/binary-tree-maximum-path-sum/)
* [Path Sum II (113)](https://leetcode.com/problems/path-sum-ii/)
* [Maximum Difference Between Node and Ancestor (1026)](https://leetcode.com/problems/maximum-difference-between-node-and-ancestor/)