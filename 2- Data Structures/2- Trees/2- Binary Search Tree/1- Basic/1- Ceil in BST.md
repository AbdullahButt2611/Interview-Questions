# Ceil in BST

`Samsung` • `Viacom18` • `VMware`

## Problem Statement
Given a root binary search tree and an integer `x`, find the Ceil of `x` in the tree.

Ceil(x) is a number that is either equal to `x` or is immediately greater than `x`. If Ceil could not be found, return `-1`.

## Examples
```ini
Input: root = [5, 1, 7, N, 2, N, N, N, 3], x = 3
Output: 3
Explanation: We find 3 in BST, so ceil of 3 is 3.
```

```ini
Input: root = [10, 5, 11, 4, 7, N, N, N, N, N, 8], x = 6
Output: 7
Explanation: We find 7 in BST, so ceil of 6 is 7.
```

## Constraints
- `1 ≤ size of binary tree ≤ 10^5`
- `1 ≤ node.data ≤ 10^5`

<br><br>

## Approach

The whole idea rests on one simple truth about a BST: **everything on the left of a node is smaller, and everything on the right is bigger.** Once you trust that rule, you never have to look at the whole tree. You just walk down one path and let the rule guide each step.

We are looking for the ceil, which is the smallest value that is still greater than or equal to `x`. So as we walk, we keep asking a plain question at every node: *"Can this node be my answer, and where do I look next?"*

Here is the thinking at each node we stand on:

- **If the node's value equals `x`**, we are done. Nothing can beat an exact match, so we return it right away.

- **If the node's value is smaller than `x`**, this node is too small to be the ceil. Anything on its left is even smaller, so we ignore the left side completely and move **right** to look for bigger values.

- **If the node's value is greater than `x`**, this node is a real candidate for the ceil. We quietly remember it as our "best answer so far", but we do not stop, because there might be a smaller value on the **left** that is still greater than `x` and fits even better. So we save this node and move left.

We keep doing this until we fall off the tree (reach an empty spot). At that point, whatever we saved last is the tightest ceil we found. If we never saved anything, it means every value was smaller than `x`, so the ceil does not exist and we return `-1`.

Think of it like shopping for a shirt one size up. Every time you find a size that fits (equal or bigger), you hold onto it, but you keep checking if there is something a little closer to your exact size. The last one you held onto is your best fit.

Because we only ever move down one branch, we touch at most the height of the tree, which makes this fast and light on memory.

<br><br>

## Code

```python
'''
Definition for Node
class Node:
    def __init__(self, val):
        self.right = None
        self.data = val
        self.left = None
'''

class Solution:
    def findCeil(self, root, x):
        ceil = 0
        while root:
            if root.data == x:
                return x

            if root.data < x:
                root = root.right
            else:
                ceil = root.data
                root = root.left

        return ceil
```

<br><br>

## Dry Run

Let us walk through **Example 2** step by step so you can see exactly what happens at every node.

```ini
Tree:
            10
           /  \
          5    11
         / \
        4   7
             \
              8

x = 6   (we want the smallest value >= 6)

Start: root = 10, ceil = 0

Iteration 1:
    Current node = 10
    Is 10 == 6 ? No
    Is 10 < 6 ? No
    Else -> 10 > 6, so 10 is a possible ceil
        Save ceil = 10
        Move LEFT to node 5
    State: ceil = 10, root = 5

Iteration 2:
    Current node = 5
    Is 5 == 6 ? No
    Is 5 < 6 ? Yes -> 5 is too small
        Move RIGHT to node 7
    State: ceil = 10, root = 7

Iteration 3:
    Current node = 7
    Is 7 == 6 ? No
    Is 7 < 6 ? No
    Else -> 7 > 6, so 7 is a possible ceil (better than 10)
        Save ceil = 7
        Move LEFT (node 7 has no left child)
    State: ceil = 7, root = None

Loop ends because root is now None (empty)

Return ceil = 7
```

The answer is `7`, which matches the expected output. Notice how `10` was our first guess, but we kept looking left and found `7`, a tighter and better fit.

<br><br>

## Related Problems

[Search in a Binary Search Tree (700)](https://leetcode.com/problems/search-in-a-binary-search-tree/)

[Closest Binary Search Tree Value (270)](https://leetcode.com/problems/closest-binary-search-tree-value/)

[Insert into a Binary Search Tree (701)](https://leetcode.com/problems/insert-into-a-binary-search-tree/)

[Kth Smallest Element in a BST (230)](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)