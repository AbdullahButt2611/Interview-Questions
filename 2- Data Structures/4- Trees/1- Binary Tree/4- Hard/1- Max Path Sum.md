# Binary Tree Maximum Path Sum

`Google` • `Amazon` • `Microsoft` • `Meta` • `DoorDash` • `Datadog` • `Citadel`

## Problem Statement

A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge connecting them. A node can appear in the path at most once, and the path does **not** need to pass through the root.

The path sum is simply the sum of all node values in that path.

Given the `root` of a binary tree, return the maximum path sum of any non-empty path.

## Examples

**Example 1:**

```ini
Input: root = [1, 2, 3]

        1
       / \
      2   3

Output: 6
Explanation: The best path is 2 -> 1 -> 3, giving 2 + 1 + 3 = 6.
```

**Example 2:**

```ini
Input: root = [-10, 9, 20, null, null, 15, 7]

        -10
       /    \
      9      20
            /  \
          15    7

Output: 42
Explanation: The best path is 15 -> 20 -> 7, giving 15 + 20 + 7 = 42.
It never touches the root at all.
```

## Constraints

* The number of nodes in the tree is in the range `[1, 3 * 10^4]`.
* `-1000 <= Node.val <= 1000`

<br><br>

## Approach

Pick any single node in the tree and look at the world from its point of view. Only two things matter to that node.

**1. What can I pass up to my parent?**

My parent wants to plug me into a longer path that continues above me. But a path is a single straight line, it cannot split into two directions and still travel upward. So I am allowed to hand my parent only **one** branch: myself plus my better child (left or right, whichever adds more).

If a child's total turns out negative, I ignore it and treat it as `0`, because pulling in a negative number would only shrink my sum. Handing up `0` for a branch is my way of saying "just take me alone, my branches are not worth it."

**2. What is the best path that bends right here at me?**

This node is the **only** place allowed to use both children at the same time. Together they form a peak shape: left branch + me + right branch. That is a complete, finished path. It can never grow any further, because a path has only two ends and both are now used up. So this value never gets sent upward. It only gets compared against a single running "best so far" variable that lives outside the recursion.

Every node quietly does both of these. We work from the bottom up (children first, then the parent), because a node cannot know its own best branch until it has heard what each child is offering.

<mark>The one line to remember: Send one, keep two.</mark>

* **Send one:** what goes up to your parent is only a single branch, since one end of the path is already taken by whatever sits above you.
* **Keep two:** what you check against the global best can use both children, because that shape is done and going nowhere.

If you can picture one node, its two children, one number sent up and one number checked against a global max, you can rebuild this whole thing on a whiteboard in any language.

**Time:** `O(n)`, since we visit every node exactly once.

**Space:** `O(h)`, where `h` is the height of the tree (the depth of the recursion stack).

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
    def dfs(self, node):
        if node == None:
            return 0

        leftSum = max(0, self.dfs(node.left))
        rightSum = max(0, self.dfs(node.right))

        self.pathSum = max(
                            self.pathSum,
                            leftSum + node.val + rightSum
                        )

        return max(leftSum, rightSum) + node.val

    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.pathSum = float('-inf')
        self.dfs(root)
        return self.pathSum
```

<br><br>

## Dry Run

```ini
Tree used for this dry run (Example 2):

        -10
       /    \
      9      20
            /  \
          15    7

Start: pathSum = -infinity
The recursion runs bottom up (post-order), so every child is
fully solved before its parent is touched.

Reading guide for each step:
  leftSum   = best branch coming from the left child  (never below 0)
  rightSum  = best branch coming from the right child (never below 0)
  bend-here = leftSum + node.val + rightSum   (path that peaks at this node)
  send up   = max(leftSum, rightSum) + node.val   (single branch given to parent)


Iteration 1: dfs(9)
  left  child is None -> dfs(None) returns 0 -> leftSum  = max(0, 0) = 0
  right child is None -> dfs(None) returns 0 -> rightSum = max(0, 0) = 0
  bend-here = 0 + 9 + 0 = 9
  pathSum   = max(-infinity, 9) = 9
  send up   = max(0, 0) + 9 = 9
  Node 9 hands 9 up to its parent (-10).


Iteration 2: dfs(15)
  left  child is None -> dfs(None) returns 0 -> leftSum  = max(0, 0) = 0
  right child is None -> dfs(None) returns 0 -> rightSum = max(0, 0) = 0
  bend-here = 0 + 15 + 0 = 15
  pathSum   = max(9, 15) = 15
  send up   = max(0, 0) + 15 = 15
  Node 15 hands 15 up to its parent (20).


Iteration 3: dfs(7)
  left  child is None -> dfs(None) returns 0 -> leftSum  = max(0, 0) = 0
  right child is None -> dfs(None) returns 0 -> rightSum = max(0, 0) = 0
  bend-here = 0 + 7 + 0 = 7
  pathSum   = max(15, 7) = 15   (15 was already better, so it stays)
  send up   = max(0, 0) + 7 = 7
  Node 7 hands 7 up to its parent (20).


Iteration 4: dfs(20)
  left  child returned 15 -> leftSum  = max(0, 15) = 15
  right child returned 7  -> rightSum = max(0, 7)  = 7
  bend-here = 15 + 20 + 7 = 42   (this uses BOTH children, a finished path)
  pathSum   = max(15, 42) = 42
  send up   = max(15, 7) + 20 = 15 + 20 = 35
  Node 20 can only pass one branch up, so it keeps 15 (the bigger side)
  and hands 35 up to its parent (-10).


Iteration 5: dfs(-10)  (the root, handled last)
  left  child returned 9  -> leftSum  = max(0, 9)  = 9
  right child returned 35 -> rightSum = max(0, 35) = 35
  bend-here = 9 + (-10) + 35 = 34
  pathSum   = max(42, 34) = 42   (42 was already better, so it stays)
  send up   = max(9, 35) + (-10) = 35 - 10 = 25
  (nobody is above the root, so this returned value is never used)


Recursion is finished.
Final answer: pathSum = 42
```

<br><br>

## Related Problems

* [Diameter of Binary Tree (543)](https://leetcode.com/problems/diameter-of-binary-tree/)
* [Path Sum (112)](https://leetcode.com/problems/path-sum/)
* [Path Sum II (113)](https://leetcode.com/problems/path-sum-ii/)
* [Path Sum III (437)](https://leetcode.com/problems/path-sum-iii/)
* [Longest Univalue Path (687)](https://leetcode.com/problems/longest-univalue-path/)
* [House Robber III (337)](https://leetcode.com/problems/house-robber-iii/)
* [Sum Root to Leaf Numbers (129)](https://leetcode.com/problems/sum-root-to-leaf-numbers/)