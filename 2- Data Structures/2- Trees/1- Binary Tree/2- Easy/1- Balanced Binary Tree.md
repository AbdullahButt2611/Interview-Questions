# Balanced Binary Tree

`Amazon` • `Google` • `Microsoft` • `Facebook` • `Adobe` • `Bloomberg` • `Cisco`

## Problem Statement
Given a binary tree, determine if it is height-balanced.

A binary tree is called **height-balanced** when, for every single node in it, the heights of its left subtree and right subtree never differ by more than `1`.

## Examples

**Example 1:**

```
Input: root = [3,9,20,null,null,15,7]
Output: true
```

**Example 2:**

```
Input: root = [1,2,2,3,3,null,null,4,4]
Output: false
```

**Example 3:**

```
Input: root = []
Output: true
```

## Constraints

* The number of nodes in the tree is in the range `[0, 5000]`.
* `-10^4 <= Node.val <= 10^4`

<br><br>

## Approach

The whole problem comes down to one simple question we ask at **every** node:

> Do the left side and the right side have heights that are close enough (differ by at most 1)?

A slow way to do this would be to first find the height of a node, and then separately check if that node is balanced. That means we would walk the same nodes again and again just to measure heights, which is wasteful.

So we use a smarter idea. We measure the height and check the balance **at the same time**, in a single bottom-up walk. Here is the thinking in plain words:

* We go all the way down to the bottom of the tree first, then come back up.
* For every node, we ask its left child "what is your height?" and its right child "what is your height?"
* Once we know both heights, we do two things together:
  * We check if the two heights differ by more than 1. If yes, this node is **not** balanced.
  * If it is fine, we return this node's own height, which is `1 + the taller of the two children`.

Now comes the clever trick. We need a way to shout "something below me is already broken, stop wasting time" up the tree. We do this using a special signal value: **`-1`**.

* A real height can never be `-1` (the smallest real height is `0` for an empty spot).
* So the moment any node finds an imbalance, it returns `-1` instead of a height.
* Every parent above, before doing anything, first checks: "Did my left child return `-1`? Did my right child return `-1`?" If either did, it does not even bother checking further. It just passes `-1` upward again.

<mark>The value -1 is not a height. It is a flag that means "unbalanced was already found below, carry the bad news up."</mark>

In the end, we look at what the root gives us:

* If the root returns `-1`, the tree is **not** balanced, so the answer is `false`.
* If the root returns any real height, the tree **is** balanced, so the answer is `true`.

Because each node is visited only once and does a tiny bit of constant work, this runs in `O(n)` time, which is as fast as it can get.

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
    def dfsHeight(self, root):
        if root == None:
            return 0

        lh = self.dfsHeight(root.left)
        if lh == -1:
            return -1

        rh = self.dfsHeight(root.right)
        if rh == -1:
            return -1

        if abs(lh - rh) > 1:
            return -1

        return 1 + max(lh, rh)


    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        return self.dfsHeight(root) != -1
```

<br><br>

## Dry Run

We will use the tree from Example 1: `[3,9,20,null,null,15,7]`.

```ini
The tree looks like this:

          3
         / \
        9   20
            / \
           15  7

We call dfsHeight(3). It goes down before it comes up.

Iteration 1: dfsHeight(9)
    dfsHeight(9.left = None)  -> returns 0   (empty spot, height 0)
    lh = 0   (not -1, so keep going)
    dfsHeight(9.right = None) -> returns 0
    rh = 0   (not -1, so keep going)
    abs(0 - 0) = 0, which is not > 1  -> node 9 is fine
    return 1 + max(0, 0) = 1
    So height of node 9 = 1

Iteration 2: dfsHeight(15)
    dfsHeight(15.left = None)  -> returns 0
    lh = 0
    dfsHeight(15.right = None) -> returns 0
    rh = 0
    abs(0 - 0) = 0, not > 1  -> node 15 is fine
    return 1 + max(0, 0) = 1
    So height of node 15 = 1

Iteration 3: dfsHeight(7)
    dfsHeight(7.left = None)  -> returns 0
    lh = 0
    dfsHeight(7.right = None) -> returns 0
    rh = 0
    abs(0 - 0) = 0, not > 1  -> node 7 is fine
    return 1 + max(0, 0) = 1
    So height of node 7 = 1

Iteration 4: dfsHeight(20)
    left child was node 15, which returned 1
    lh = 1   (not -1, so keep going)
    right child was node 7, which returned 1
    rh = 1   (not -1, so keep going)
    abs(1 - 1) = 0, not > 1  -> node 20 is fine
    return 1 + max(1, 1) = 2
    So height of node 20 = 2

Iteration 5: dfsHeight(3)  (the root)
    left child was node 9, which returned 1
    lh = 1   (not -1, so keep going)
    right child was node 20, which returned 2
    rh = 2   (not -1, so keep going)
    abs(1 - 2) = 1, which is not > 1  -> node 3 is fine
    return 1 + max(1, 2) = 3
    So height of the root = 3

Final step: isBalanced
    dfsHeight(root) returned 3
    3 != -1  ->  True

Answer: true
```

<br><br>

## Complexity

* **Time:** `O(n)`, because every node is visited exactly once.
* **Space:** `O(h)`, where `h` is the height of the tree. This comes from the recursion stack. In the worst case (a completely skewed tree) it becomes `O(n)`.

<br><br>

## Related Problems

* [Maximum Depth of Binary Tree (104)](https://leetcode.com/problems/maximum-depth-of-binary-tree/)
* [Diameter of Binary Tree (543)](https://leetcode.com/problems/diameter-of-binary-tree/)
* [Same Tree (100)](https://leetcode.com/problems/same-tree/)
* [Minimum Depth of Binary Tree (111)](https://leetcode.com/problems/minimum-depth-of-binary-tree/)
* [Balance a Binary Search Tree (1382)](https://leetcode.com/problems/balance-a-binary-search-tree/)