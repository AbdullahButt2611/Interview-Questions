# Same Tree

`Amazon` • `Google` • `Meta` • `Microsoft` • `Bloomberg`

> This question is also referred as **Identical Tree**.

## Problem Statement

Given the roots of two binary trees `p` and `q`, write a function to check if they are the same or not.

Two binary trees are considered the same if:

* They are **structurally identical** (the shape matches exactly).
* The **nodes have the same value** at every matching position.

## Examples

**Example 1:**

```
Input: p = [1,2,3], q = [1,2,3]
Output: true
```

**Example 2:**

```
Input: p = [1,2], q = [1,null,2]
Output: false
```

**Example 3:**

```
Input: p = [1,2,1], q = [1,1,2]
Output: false
```

## Constraints

* The number of nodes in both trees is in the range `[0, 100]`.
* `-10^4 <= Node.val <= 10^4`

<br><br>

## Approach

The whole idea is simple: walk both trees **at the same time**, one pair of nodes at a time, and keep asking the same tiny set of questions until you either find a mismatch or run out of nodes.

At every step you are standing on one node from tree `p` and one node from tree `q` that sit in the **same position**. For that pair, you ask three questions in order:

* **Are both nodes empty?**
  If both are `None`, there is nothing left to compare on this branch, so this part is a match. Return `True`.

* **Is only one of them empty?**
  If one node exists but the other is `None`, the shapes already differ, so the trees cannot be the same. Return `False`.

* **Do both nodes hold the same value?**
  If both nodes exist but their values are different, they fail right here. Return `False`.

If all three checks pass for the current pair, you go **deeper in sync**. You run the exact same comparison on:

* the **left child of `p`** against the **left child of `q`**, and
* the **right child of `p`** against the **right child of `q`**.

The trees are the same only if **every single pair** you visit agrees, so you join these smaller answers with `and`. The moment any pair anywhere disagrees, that `False` travels all the way back up and the final answer becomes `False`.

<mark>The key is that both trees are walked in perfect lockstep, always comparing p's node with q's node in the same spot. That is what checks structure and values together, not just the set of numbers.</mark>

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
    def isSameTree(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
        # Returns true if both trees have null as root (first base case)
        if not root1 and not root2:
            return True

        # Function returns false if one of the roots here is null (second base case)
        if root1 and root2:
            # Returns true if both nodes have the same left sub-tree, right sub-tree
            # and value
            return (root1.val == root2.val and
                    self.isSameTree(root1.left, root2.left) and
                    self.isSameTree(root1.right, root2.right))

        # Returns false if neither of the above cases are satisfied
        return False
```

<br><br>

## Dry Run

We will trace **Example 1**: `p = [1,2,3]`, `q = [1,2,3]` (expected output: `true`).

Both trees look like this:

```
      1
     / \
    2   3
```

Every call below compares one node of `p` with the node of `q` in the same position.

```ini
Trees:
p:  1(left=2, right=3)    q:  1(left=2, right=3)
node 2: left=None, right=None
node 3: left=None, right=None

Call 1 -> isSameTree(p=1, q=1)
    both null?         no  (both exist)
    both exist?        yes
    values 1 == 1?     yes
    now recurse LEFT:  isSameTree(2, 2)  --> go to Call 2

    Call 2 -> isSameTree(p=2, q=2)
        both null?         no
        both exist?        yes
        values 2 == 2?     yes
        recurse LEFT:  isSameTree(None, None)  --> Call 3

        Call 3 -> isSameTree(None, None)
            both null?     yes
            RETURN True

        left result = True
        recurse RIGHT: isSameTree(None, None)  --> Call 4

        Call 4 -> isSameTree(None, None)
            both null?     yes
            RETURN True

        right result = True
        Call 2 returns: (2==2) and True and True = True

    left of Call 1 = True
    now recurse RIGHT: isSameTree(3, 3)  --> Call 5

    Call 5 -> isSameTree(p=3, q=3)
        both null?         no
        both exist?        yes
        values 3 == 3?     yes
        recurse LEFT:  isSameTree(None, None)  --> Call 6

        Call 6 -> isSameTree(None, None)
            both null?     yes
            RETURN True

        left result = True
        recurse RIGHT: isSameTree(None, None)  --> Call 7

        Call 7 -> isSameTree(None, None)
            both null?     yes
            RETURN True

        right result = True
        Call 5 returns: (3==3) and True and True = True

    right of Call 1 = True
    Call 1 returns: (1==1) and True (left) and True (right) = True

FINAL ANSWER = True
```

**What to notice:**

* Every matching pair passed all three checks, so no `False` was ever produced.
* The `None, None` pairs at the leaves are the base cases that stop the recursion cleanly.
* If any single pair had differed (different value or one side `None`), that `False` would have bubbled up and made the final answer `False` (this is exactly what happens in Example 2 and Example 3).

<br><br>

## Complexity

* **Time:** `O(n)`, where `n` is the number of nodes in the smaller tree. In the worst case we visit every matching node once.
* **Space:** `O(h)`, where `h` is the height of the tree. This is the depth of the recursion call stack (up to `O(n)` for a skewed tree, `O(log n)` for a balanced one).

<br><br>

## Related Problems

* [Symmetric Tree (101)](https://leetcode.com/problems/symmetric-tree/)
* [Subtree of Another Tree (572)](https://leetcode.com/problems/subtree-of-another-tree/)
* [Maximum Depth of Binary Tree (104)](https://leetcode.com/problems/maximum-depth-of-binary-tree/)
* [Invert Binary Tree (226)](https://leetcode.com/problems/invert-binary-tree/)
* [Leaf-Similar Trees (872)](https://leetcode.com/problems/leaf-similar-trees/)