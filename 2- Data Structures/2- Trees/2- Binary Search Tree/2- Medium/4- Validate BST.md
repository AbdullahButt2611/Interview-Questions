# Validate Binary Search Tree

`Amazon` • `Bloomberg` • `MongoDB` • `Nutanix` • `SpaceX` • `Hudson River Trading` • `Educative`

## Problem Statement

Given the `root` of a binary tree, determine if it is a **valid binary search tree (BST)**.

A valid BST is defined as follows:

- The left subtree of a node contains only nodes with values **strictly less** than the node's value.
- The right subtree of a node contains only nodes with values **strictly greater** than the node's value.
- Both the left and right subtrees must also be binary search trees.

## Examples

**Example 1:**

```ini
Input: root = [2,1,3]
Output: true
Explanation: 1 is on the left of 2 and smaller. 3 is on the right of 2 and bigger.
```

**Example 2:**

```ini
Input: root = [5,1,4,null,null,3,6]
Output: false
Explanation: The root is 5, but its right child is 4. 4 is smaller than 5, so it cannot sit on the right.
```

## Constraints

- The number of nodes in the tree is in the range `[1, 10^4]`.
- `-2^31 <= Node.val <= 2^31 - 1`

<br><br>

## Approach

### The One Rule to Remember

In a valid BST, <mark>every node must be bigger than everything on its left and smaller than everything on its right</mark>.

- Not just bigger than its left **child**. Bigger than the **entire** left side.
- Not just smaller than its right **child**. Smaller than the **entire** right side.

### The Trap Most People Fall Into

Checking only "parent vs child" is **not enough**. Look at this tree:

```ini
        5
       / \
      4   6
         / \
        3   7
```

- 4 < 5 ✓, 6 > 5 ✓, 3 < 6 ✓, 7 > 6 ✓. Every parent and child pair looks fine.
- But 3 lives on the **right side of 5**, and 3 is smaller than 5. So this tree is **not** a BST.

Both approaches below catch this trap.

### Approach 1: Inorder Traversal (Read the Tree Like a Sorted List)

**The idea:** If you read a BST in the order **left, node, right**, the values always come out **sorted**. This reading order is called **inorder traversal**.

So instead of checking the tree, just read it and check if the list is sorted.

**Steps:**

1. **Read the tree in inorder.**
   - At every node: first visit its whole left side, then write down the node's value, then visit its whole right side.
   - Every value goes into a list in the order you write it down.
2. **Walk through the list from start to end.**
   - Compare each value with the one just before it.
3. **Look for a problem.**
   - If any value is **smaller than or equal to** the one before it, the list is not sorted. Return `False`.
4. **No problem found?**
   - The list is perfectly sorted. Return `True`.

> Why "smaller than **or equal**"? Values must keep going **up**. Two equal values (a duplicate) also break the BST rule.

> Memory hook: <mark>"A real BST, read left to right, is always sorted."</mark>

### Approach 2: Recursive Range Check (Give Every Node a Safe Zone)

**The idea:** Every node has a **safe zone**, a range `(low, high)`. The node's value must sit **strictly inside** it.

**Steps:**

1. **Start at the root.**
   - The root can be any value, so its safe zone is `(-infinity, +infinity)`.
2. **Check the current node.**
   - Is `low < value < high`? If **not**, the tree is broken. Return `False`.
3. **Going left?** The ceiling comes down.
   - Everything on the left must be smaller than the current node.
   - So the new range is `(low, value)`. The floor stays the same.
4. **Going right?** The floor goes up.
   - Everything on the right must be bigger than the current node.
   - So the new range is `(value, high)`. The ceiling stays the same.
5. **Hit an empty spot (`None`)?**
   - Nothing to break there. Return `True`.
6. **The tree is valid only if both the left side and the right side are valid.**

**Why does this beat the trap?** The range carries limits from **all** ancestors, not just the parent. In the trap tree, node 3 gets the range `(5, 6)`, because it is on the right of 5 and on the left of 6. 3 is not inside `(5, 6)`, so it fails.

> Memory hook: <mark>"Going left lowers the ceiling, going right raises the floor."</mark>

### Which One to Pick?

- **Approach 1** is the easiest to explain: "inorder of a BST is sorted."
- **Approach 2** is usually preferred in interviews:
  - It does not store all values in a list, so it uses less memory.
  - It stops the moment it finds a bad node.

<br><br>

## Solution

### Approach 1: Inorder Traversal

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isValidBST(self, root: TreeNode | None) -> bool:
        # Helper function for inorder traversal
        def inorder_traversal(node, values):
            if node:
                inorder_traversal(node.left, values)
                values.append(node.val)
                inorder_traversal(node.right, values)

        # Perform inorder traversal to get the sequence
        sorted_values = []
        inorder_traversal(root, sorted_values)

        # Check if the sequence is strictly ascending
        for i in range(1, len(sorted_values)):
            if sorted_values[i] <= sorted_values[i - 1]:
                return False

        return True
```

### Approach 2: Recursive Range Check

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isValidBST(self, root: TreeNode | None) -> bool:
        # Helper function to validate BST recursively
        def is_valid(node, min_val=float('-inf'), max_val=float('inf')):
            if node is None:
                return True

            # Check if the current node value is within the valid range
            if not (min_val < node.val < max_val):
                return False

            # Recursively check the left and right subtrees
            return (is_valid(node.left, min_val, node.val) and
                    is_valid(node.right, node.val, max_val))

        # Start the validation from the root with the widest range
        return is_valid(root)
```

<br><br>

## Dry Run

```ini
#####################################################
APPROACH 1: INORDER TRAVERSAL
#####################################################

=====================================================
SCENARIO A: root = [2,1,3]
=====================================================

Starting Tree:

        2
       / \
      1   3

Setup:
  sorted_values = []

Phase 1: Inorder traversal (left, node, right)

  Step 1: inorder_traversal(2)
    Node 2 exists. First visit its LEFT side → call inorder_traversal(1)

  Step 2: inorder_traversal(1)
    Node 1 exists. First visit its LEFT side → call inorder_traversal(None)

  Step 3: inorder_traversal(None)
    Node is None. Nothing to do. Go back to node 1.

  Step 4: Back at node 1
    Left side done. Write down 1.
    sorted_values = [1]
    Now visit its RIGHT side → call inorder_traversal(None)

  Step 5: inorder_traversal(None)
    Node is None. Nothing to do. Node 1 is fully done. Go back to node 2.

  Step 6: Back at node 2
    Left side done. Write down 2.
    sorted_values = [1, 2]
    Now visit its RIGHT side → call inorder_traversal(3)

  Step 7: inorder_traversal(3)
    Node 3 exists. First visit its LEFT side → call inorder_traversal(None)
    Node is None. Nothing to do. Back at node 3.
    Left side done. Write down 3.
    sorted_values = [1, 2, 3]
    Visit its RIGHT side → inorder_traversal(None). Nothing to do.
    Node 3 is fully done. Go back to node 2. Node 2 is fully done.

  Traversal complete:
    sorted_values = [1, 2, 3]

Phase 2: Check if the list is strictly increasing

  Iteration 1: i = 1
    sorted_values[1] = 2, sorted_values[0] = 1
    Is 2 <= 1? NO. Fine, keep going.

  Iteration 2: i = 2
    sorted_values[2] = 3, sorted_values[1] = 2
    Is 3 <= 2? NO. Fine, keep going.

  Loop finished. No problem found.

Return True
Output: true  ✓


=====================================================
SCENARIO B: root = [5,1,4,null,null,3,6]
=====================================================

Starting Tree:

        5
       / \
      1   4
         / \
        3   6

Setup:
  sorted_values = []

Phase 1: Inorder traversal (left, node, right)

  Step 1: inorder_traversal(5)
    Node 5 exists. First visit its LEFT side → call inorder_traversal(1)

  Step 2: inorder_traversal(1)
    Node 1 exists. LEFT side → inorder_traversal(None). Nothing to do.
    Write down 1.
    sorted_values = [1]
    RIGHT side → inorder_traversal(None). Nothing to do.
    Node 1 is fully done. Go back to node 5.

  Step 3: Back at node 5
    Left side done. Write down 5.
    sorted_values = [1, 5]
    Now visit its RIGHT side → call inorder_traversal(4)

  Step 4: inorder_traversal(4)
    Node 4 exists. First visit its LEFT side → call inorder_traversal(3)

  Step 5: inorder_traversal(3)
    Node 3 exists. LEFT side → inorder_traversal(None). Nothing to do.
    Write down 3.
    sorted_values = [1, 5, 3]
    RIGHT side → inorder_traversal(None). Nothing to do.
    Node 3 is fully done. Go back to node 4.

  Step 6: Back at node 4
    Left side done. Write down 4.
    sorted_values = [1, 5, 3, 4]
    Now visit its RIGHT side → call inorder_traversal(6)

  Step 7: inorder_traversal(6)
    Node 6 exists. LEFT side → inorder_traversal(None). Nothing to do.
    Write down 6.
    sorted_values = [1, 5, 3, 4, 6]
    RIGHT side → inorder_traversal(None). Nothing to do.
    Node 6 done. Back to 4 (done). Back to 5 (done).

  Traversal complete:
    sorted_values = [1, 5, 3, 4, 6]

Phase 2: Check if the list is strictly increasing

  Iteration 1: i = 1
    sorted_values[1] = 5, sorted_values[0] = 1
    Is 5 <= 1? NO. Fine, keep going.

  Iteration 2: i = 2
    sorted_values[2] = 3, sorted_values[1] = 5
    Is 3 <= 5? YES. The list went DOWN. Not sorted.
    Return False immediately.

Output: false  ✓


#####################################################
APPROACH 2: RECURSIVE RANGE CHECK
#####################################################

=====================================================
SCENARIO C: root = [2,1,3]
=====================================================

Starting Tree:

        2
       / \
      1   3

Call 1: is_valid(node=2, min=-inf, max=+inf)
  Is node None? NO.
  Range check: is -inf < 2 < +inf? YES. Node 2 is safe.
  Now check the LEFT side first.
  Going left lowers the ceiling: new range = (-inf, 2)

  Call 2: is_valid(node=1, min=-inf, max=2)
    Is node None? NO.
    Range check: is -inf < 1 < 2? YES. Node 1 is safe.
    Check LEFT: new range = (-inf, 1)

    Call 3: is_valid(node=None, min=-inf, max=1)
      Node is None. Return True.

    Left side of 1 is True. Check RIGHT: new range = (1, 2)

    Call 4: is_valid(node=None, min=1, max=2)
      Node is None. Return True.

    Left = True AND Right = True → Call 2 returns True.

  Back in Call 1: Left side of 2 is True.
  Now check the RIGHT side.
  Going right raises the floor: new range = (2, +inf)

  Call 5: is_valid(node=3, min=2, max=+inf)
    Is node None? NO.
    Range check: is 2 < 3 < +inf? YES. Node 3 is safe.
    Check LEFT: new range = (2, 3)

    Call 6: is_valid(node=None, min=2, max=3)
      Node is None. Return True.

    Check RIGHT: new range = (3, +inf)

    Call 7: is_valid(node=None, min=3, max=+inf)
      Node is None. Return True.

    Left = True AND Right = True → Call 5 returns True.

  Back in Call 1: Left = True AND Right = True → Call 1 returns True.

Output: true  ✓


=====================================================
SCENARIO D: root = [5,1,4,null,null,3,6]
=====================================================

Starting Tree:

        5
       / \
      1   4
         / \
        3   6

Call 1: is_valid(node=5, min=-inf, max=+inf)
  Is node None? NO.
  Range check: is -inf < 5 < +inf? YES. Node 5 is safe.
  Check LEFT: new range = (-inf, 5)

  Call 2: is_valid(node=1, min=-inf, max=5)
    Is node None? NO.
    Range check: is -inf < 1 < 5? YES. Node 1 is safe.
    Check LEFT: is_valid(None, -inf, 1) → True
    Check RIGHT: is_valid(None, 1, 5) → True
    Left = True AND Right = True → Call 2 returns True.

  Back in Call 1: Left side of 5 is True.
  Check RIGHT: new range = (5, +inf)

  Call 3: is_valid(node=4, min=5, max=+inf)
    Is node None? NO.
    Range check: is 5 < 4 < +inf? NO. 4 is not bigger than 5.
    Node 4 is OUTSIDE its safe zone. Return False.
    (Its children 3 and 6 are never checked.)

  Back in Call 1: Left = True AND Right = False → Call 1 returns False.

Output: false  ✓


=====================================================
SCENARIO E: root = [5,4,6,null,null,3,7]  (the trap tree)
=====================================================

Starting Tree:

        5
       / \
      4   6
         / \
        3   7

Every parent and child pair looks fine here. Let's see if the range catches it.

Call 1: is_valid(node=5, min=-inf, max=+inf)
  Is node None? NO.
  Range check: is -inf < 5 < +inf? YES. Node 5 is safe.
  Check LEFT: new range = (-inf, 5)

  Call 2: is_valid(node=4, min=-inf, max=5)
    Is node None? NO.
    Range check: is -inf < 4 < 5? YES. Node 4 is safe.
    Check LEFT: is_valid(None, -inf, 4) → True
    Check RIGHT: is_valid(None, 4, 5) → True
    Left = True AND Right = True → Call 2 returns True.

  Back in Call 1: Left side of 5 is True.
  Check RIGHT: new range = (5, +inf)

  Call 3: is_valid(node=6, min=5, max=+inf)
    Is node None? NO.
    Range check: is 5 < 6 < +inf? YES. Node 6 is safe.
    Check LEFT: going left lowers the ceiling to 6.
    The floor stays 5 (it was passed down from the root).
    New range = (5, 6)

    Call 4: is_valid(node=3, min=5, max=6)
      Is node None? NO.
      Range check: is 5 < 3 < 6? NO. 3 is not bigger than 5.
      Node 3 is OUTSIDE its safe zone. Return False.

    Left side of 6 is False.
    Because of "and", the right side (node 7) is never checked.
    Call 3 returns False.

  Back in Call 1: Left = True AND Right = False → Call 1 returns False.

The floor of 5 travelled down from the root to node 3.
That is exactly how the range check catches the trap.

Output: false  ✓
```

<br><br>

## Complexity Analysis

### Approach 1: Inorder Traversal

- **Time Complexity:** `O(N)`, where `N` is the number of nodes.
  - The traversal visits every node once: `O(N)`.
  - The sorted check walks through the list once: `O(N)`.
- **Space Complexity:** `O(N)`.
  - The list stores all `N` values.
  - The recursion stack adds `O(H)`, where `H` is the height of the tree.

### Approach 2: Recursive Range Check

- **Time Complexity:** `O(N)`.
  - In the worst case (a valid BST), every node is checked once.
  - It can stop early as soon as a bad node is found.
- **Space Complexity:** `O(H)`, where `H` is the height of the tree.
  - Only the recursion stack is used, no extra list.
  - In a balanced tree this is `O(log N)`, and in a skewed tree it is `O(N)`.

<br><br>

## Related Problems

- [Binary Tree Inorder Traversal (94)](https://leetcode.com/problems/binary-tree-inorder-traversal/)
- [Recover Binary Search Tree (99)](https://leetcode.com/problems/recover-binary-search-tree/)
- [Binary Search Tree Iterator (173)](https://leetcode.com/problems/binary-search-tree-iterator/)
- [Kth Smallest Element in a BST (230)](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)
- [Largest BST Subtree (333)](https://leetcode.com/problems/largest-bst-subtree/)
- [Delete Node in a BST (450)](https://leetcode.com/problems/delete-node-in-a-bst/)
- [Find Mode in Binary Search Tree (501)](https://leetcode.com/problems/find-mode-in-binary-search-tree/)
- [Minimum Absolute Difference in BST (530)](https://leetcode.com/problems/minimum-absolute-difference-in-bst/)
- [Search in a Binary Search Tree (700)](https://leetcode.com/problems/search-in-a-binary-search-tree/)
- [Insert into a Binary Search Tree (701)](https://leetcode.com/problems/insert-into-a-binary-search-tree/)
- [Maximum Sum BST in Binary Tree (1373)](https://leetcode.com/problems/maximum-sum-bst-in-binary-tree/)