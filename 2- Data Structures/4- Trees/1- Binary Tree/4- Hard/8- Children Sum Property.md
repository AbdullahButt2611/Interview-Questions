# Convert Binary Tree to Children Sum Property

`Amazon` • `Microsoft` • `Adobe` • `Samsung` • `Qualcomm` • `takeUforward`

## Problem Statement

Given the root of a binary tree, convert it into a tree that satisfies the <mark>Children Sum Property</mark>.

A tree follows the Children Sum Property when:

- Every node's value is equal to the sum of the values of its left child and right child.
- A missing (null) child is treated as having value 0.
- A leaf node automatically satisfies the property since it has no children.

Rules for the conversion:

- You can only **increment** the value of any node. You are not allowed to decrement any value.
- You cannot change the structure of the tree (no adding, removing, or moving nodes).

## Examples

**Example 1**

Input Tree:

```
        50
       /  \
      7    2
     / \  
    3   5 
```

Output Tree:

```
        57
       /  \
     55    2
     / \
    50   5
```

Explanation:

- Leaves stay the same at first: 3, 5, 2.
- The left middle node 7 becomes 55 because its final children are 50 and 5.
- The root 50 becomes 57 because its final children are 55 and 2.
- 55 = 50 + 5 ✓ and 57 = 55 + 2 ✓, so the property holds everywhere.

## Constraints

- 1 ≤ n ≤ 10^4 (n is the number of nodes)
- (-10^5) ≤ Node.val ≤ 10^5

<br><br>

## Approach

The main trick to understand is a simple rule: **we can only make numbers bigger, never smaller.** So whenever a parent is bigger than its children's sum, we cannot shrink the parent, we must grow the children instead.

Keeping that in mind, here is what we do at every node:

**Step 1: Look at the current node and add up its children.**

- Add the left child's value and the right child's value.
- Treat a missing child as 0.
- Call this number `child_sum`.

**Step 2: Compare `child_sum` with the current node's value.**

- **Case A (children are big enough):** If `child_sum` is greater than or equal to the current node, simply set the current node's value equal to `child_sum`. We just grew the parent, which is allowed.
- **Case B (children are too small):** If `child_sum` is smaller than the current node, we cannot shrink the parent. So we **push the parent's value down** into a child. We copy the parent's value into the left child if it exists, otherwise into the right child. This makes that child bigger (which is allowed).

**Step 3: Recurse into the left and right subtrees.**

- We do the exact same fixing process on the left subtree and then the right subtree.
- This matters because in Case B we may have made a child suddenly very large, and now that child might be bigger than its own children. Recursion will push that value further down until it settles.

**Step 4: On the way back, recompute the parent.**

- After both subtrees are done, the children's values may have grown even more during recursion.
- So we add the (possibly new) left and right values one more time and set the parent equal to this fresh sum.
- This final step is what actually locks in the property: every non-leaf node ends up equal to the sum of its children.

Why this always works:

- In Case A we only grow the parent, so nothing above breaks (recursion above will fix it).
- In Case B we grow a child, which may temporarily break things below, but recursion cleans that up.
- The last "update parent to new child sum" step guarantees a perfect match at every level.

**Time Complexity:** O(n), where n is the number of nodes. Each node is touched a constant number of times.

**Space Complexity:** O(h), where h is the height of the tree, due to the recursion stack. In the worst case of a skewed tree this becomes O(n).

<br><br>

## Code

```python
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def changeTree(self, root):
        # Base case: If the current node
        # is None, return and do nothing.
        if root is None:
            return

        # Calculate the sum of the values of
        # the left and right children, if they exist.
        child = 0
        if root.left:
            child += root.left.val
        if root.right:
            child += root.right.val

        # Compare the sum of children with
        # the current node's value and update
        if child >= root.val:
            root.val = child
        else:
            # If the sum is smaller, update the
            # child with the current node's value.
            if root.left:
                root.left.val = root.val
            elif root.right:
                root.right.val = root.val

        # Recursively call the function
        # on the left and right children.
        self.changeTree(root.left)
        self.changeTree(root.right)

        # Calculate the total sum of the
        # values of the left and right
        # children, if they exist.
        tot = 0
        if root.left:
            tot += root.left.val
        if root.right:
            tot += root.right.val

        # If either left or right child
        # exists, update the current node's
        # value with the total sum.
        if root.left or root.right:
            root.val = tot
```

<br><br>

## Dry Run

We will trace the algorithm on the following input tree:

```ini
Initial Tree:
        50
       /  \
      7    2
     / \
    3   5


Iteration 1: changeTree(root = 50)
  Step 1: child_sum = 7 + 2 = 9
  Step 2: Is 9 >= 50 ? No (Case B)
          Push root's value down to left child.
          Node 7 is overwritten to 50.
  Tree state:
        50
       /  \
     50    2
     / \
    3   5
  Now go recurse into left child, then right child.


Iteration 2: changeTree(50)   [this was old node 7]
  Step 1: child_sum = 3 + 5 = 8
  Step 2: Is 8 >= 50 ? No (Case B)
          Push value down to left child.
          Node 3 is overwritten to 50.
  Tree state:
        50
       /  \
     50    2
     / \
    50  5
  Now recurse into left child (50), then right child (5).


Iteration 3: changeTree(50)   [this was old node 3, a leaf now with value 50]
  Step 1: child_sum = 0 (no children)
  Step 2: Is 0 >= 50 ? No (Case B), but there are no children to push into.
          Nothing changes.
  Recurse left (None): returns immediately.
  Recurse right (None): returns immediately.
  Step 4: tot = 0. Node has no children, so we do NOT overwrite.
          Value stays 50.


Iteration 4: changeTree(5)   [leaf]
  Step 1: child_sum = 0
  Step 2: Is 0 >= 5 ? No (Case B), no children to push into.
          Nothing changes.
  Recurse left and right: both None, return immediately.
  Step 4: tot = 0, no children, no overwrite.
          Value stays 5.


Iteration 5: Back in Iteration 2's frame, at the node with value 50
  (the middle-level left node).
  Step 4: Recompute tot from children.
          tot = 50 (left) + 5 (right) = 55
          Node has children, so overwrite value with tot.
          This node's value becomes 55.
  Tree state:
        50
       /  \
     55    2
     / \
    50  5


Iteration 6: changeTree(2)   [right child of the original root, a leaf]
  Step 1: child_sum = 0
  Step 2: Is 0 >= 2 ? No, no children to push into.
          Nothing changes.
  Recurse left and right: both None.
  Step 4: tot = 0, no children, no overwrite.
          Value stays 2.


Iteration 7: Back in Iteration 1's frame, at the root (value 50).
  Step 4: Recompute tot from children.
          tot = 55 (left) + 2 (right) = 57
          Root has children, so overwrite value with tot.
          Root's value becomes 57.


Final Tree:
        57
       /  \
     55    2
     / \
    50  5


Verification of the Children Sum Property:
  Leaves 50, 5, 2  -> auto-satisfy.
  Node 55  -> 50 + 5 = 55  ✓
  Node 57  -> 55 + 2 = 57  ✓
All non-leaf nodes now equal the sum of their children.
```

<br><br>

## Related Problems

- [Path Sum (112)](https://leetcode.com/problems/path-sum/)
- [Path Sum II (113)](https://leetcode.com/problems/path-sum-ii/)
- [Sum Root to Leaf Numbers (129)](https://leetcode.com/problems/sum-root-to-leaf-numbers/)
- [Sum of Left Leaves (404)](https://leetcode.com/problems/sum-of-left-leaves/)
- [Most Frequent Subtree Sum (508)](https://leetcode.com/problems/most-frequent-subtree-sum/)
- [Maximum Product of Splitted Binary Tree (1339)](https://leetcode.com/problems/maximum-product-of-splitted-binary-tree/)