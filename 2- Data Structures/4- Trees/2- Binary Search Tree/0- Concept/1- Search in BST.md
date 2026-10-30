# Search in a Binary Search Tree

`Amazon` • `Google` • `Meta` • `Microsoft` • `Salesforce`

## Problem Statement
You are given the `root` of a binary search tree (BST) and an integer `val`.

Find the node in the BST whose value equals `val` and return the subtree rooted at that node. If such a node does not exist, return `null`.

## Examples

```ini
Input: root = [4,2,7,1,3], val = 2
Output: [2,1,3]
```

```ini
Input: root = [4,2,7,1,3], val = 5
Output: []
```

## Constraints

* The number of nodes in the tree is in the range `[1, 5000]`.
* `1 <= Node.val <= 10^7`
* `root` is a binary search tree.
* `1 <= val <= 10^7`

<br><br>

## Approach

The trick here is to use the one property that makes a BST special.

In a BST, every node follows a simple rule:

* Everything on the **left** of a node is **smaller** than it.
* Everything on the **right** of a node is **larger** than it.

This means we never have to look at the whole tree. At every node we can ask one question and instantly throw away half of the remaining nodes.

Here is the thinking, step by step:

* Start at the `root`.
* Look at the current node and compare its value with `val`.
* If they are equal, we found it. Return this node (returning a node automatically brings its entire subtree with it).
* If `val` is **smaller** than the current node's value, the answer can only be on the **left**, so move left.
* If `val` is **bigger**, the answer can only be on the **right**, so move right.
* Keep repeating this until we either land on the matching node or fall off the tree (reach `null`), which means the value simply is not there.

Because we cut the search space in half at every step, this is fast and clean. We do not need recursion or extra memory. A simple loop that keeps walking down the tree is enough.

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
    def searchBST(self, root: TreeNode | None, val: int) -> TreeNode | None:
        while root != None and root.val != val:
            root = root.left if val < root.val else root.right
        
        return root
```

<br><br>

## Dry Run

Let us walk through `root = [4,2,7,1,3]` with `val = 2`.

The tree looks like this:

```ini
        4
       / \
      2   7
     / \
    1   3
```

Now the loop:

```ini
Target val = 2

Iteration 1:
  root = 4
  Is root None?      No
  Is root.val == val? 4 == 2 -> No, keep going
  Compare: is val < root.val? 2 < 4 -> Yes
  So move LEFT
  root now points to node 2

Iteration 2:
  root = 2
  Is root None?      No
  Is root.val == val? 2 == 2 -> Yes! Loop stops here

Loop ends because we found the match.
Return node 2, which brings its subtree [2,1,3]

Final Output: [2,1,3]
```

Now the second case, `val = 5` (a value not in the tree):

```ini
Target val = 5

Iteration 1:
  root = 4
  Is root None?      No
  Is root.val == val? 4 == 5 -> No, keep going
  Compare: is val < root.val? 5 < 4 -> No
  So move RIGHT
  root now points to node 7

Iteration 2:
  root = 7
  Is root None?      No
  Is root.val == val? 7 == 5 -> No, keep going
  Compare: is val < root.val? 5 < 7 -> Yes
  So move LEFT
  root now points to node 7's left child, which is None

Iteration 3:
  root = None
  Is root None?      Yes! Loop stops here

Loop ends because we fell off the tree.
Return None (shown as [])

Final Output: []
```

<br><br>

## Complexity

* **Time:** `O(H)` where `H` is the height of the tree. In a balanced BST this is `O(log n)`, and in the worst case (a tree shaped like a straight line) it becomes `O(n)`.
* **Space:** `O(1)` because we only use a single pointer and no extra data structures or recursion stack.

<mark>The whole idea rests on one habit: at every node, ask "left or right?" and commit. Never look back.</mark>

<br><br>

## Related Problems

* [Insert into a Binary Search Tree (LeetCode 701)](https://leetcode.com/problems/insert-into-a-binary-search-tree/)
* [Delete Node in a BST (LeetCode 450)](https://leetcode.com/problems/delete-node-in-a-bst/)
* [Validate Binary Search Tree (LeetCode 98)](https://leetcode.com/problems/validate-binary-search-tree/)
* [Lowest Common Ancestor of a Binary Search Tree (LeetCode 235)](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/)
* [Closest Binary Search Tree Value (LeetCode 270)](https://leetcode.com/problems/closest-binary-search-tree-value/)