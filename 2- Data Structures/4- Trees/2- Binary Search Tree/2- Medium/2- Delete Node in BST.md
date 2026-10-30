# Delete Node in a BST

`Amazon` • `Microsoft` • `Google` • `Meta` • `LinkedIn` • `Pinterest` • `Intuit`

## Problem Statement

Given a root node reference of a BST and a key, delete the node with the given key in the BST. Return the **root node reference** (possibly updated) of the BST.

Basically, the deletion can be divided into two stages:

1. Search for a node to remove.
2. If the node is found, delete the node.

## Examples

**Example 1:**

```ini
Input: root = [5,3,6,2,4,null,7], key = 3
Output: [5,4,6,2,null,null,7]
Explanation: Given key to delete is 3. So we find the node with value 3 and delete it.
One valid answer is [5,4,6,2,null,null,7].
Another valid answer is [5,2,6,null,4,null,7] and it's also accepted.
```

**Example 2:**

```ini
Input: root = [5,3,6,2,4,null,7], key = 0
Output: [5,3,6,2,4,null,7]
Explanation: The tree does not contain a node with value = 0.
```

**Example 3:**

```ini
Input: root = [], key = 0
Output: []
```

## Constraints

- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-10^5 <= Node.val <= 10^5`
- Each node has a **unique** value.
- `root` is a valid binary search tree.
- `-10^5 <= key <= 10^5`

<br><br>

## Approach

### The One Rule to Remember

In a BST, <mark>everything on the left is smaller, everything on the right is bigger</mark>.

So the entire **left subtree** of a node is smaller than **every single node** in its right subtree. Keep this in mind, it is the whole trick.

### Step 1: Find the Node (and Remember Its Parent)

- Start at the root.
- If `key` is smaller than the current value, go **left**. If bigger, go **right**.
- While walking, always remember the node you came from. This is the **parent**.
- Stop when you find the key, or when you fall off the tree (key not present).
- If the key is not present, just return the tree as it is.

> Why remember the parent? Because after removing the node, someone has to point to its replacement. That someone is the parent.

### Step 2: Remove the Node (Three Simple Cases)

Think of it as: "Who will take this node's place?"

- **No left child** → its **right child** takes its place (could be `None`, that is fine).
- **No right child** → its **left child** takes its place.
- **Both children exist** → the **right child** takes its place. But now the left subtree has nowhere to go, so:
  - Walk down the right subtree, always going **left**, until you reach the **smallest** node there.
  - Attach the whole left subtree as the **left child** of that smallest node.

Why is this safe? The smallest node of the right subtree is still bigger than everything in the left subtree (the One Rule). And it has no left child, so the spot is empty and waiting.

> Memory hook: <mark>"Right child moves up, left subtree hangs under the smallest on the right."</mark>

### Step 3: Reconnect

- If the node being deleted was the **root**, there is no parent. Just return the replacement as the new root.
- Otherwise, check which side of the parent the node was on (left or right), and point that side to the replacement.
- Return the original root.

<br><br>

## Solution

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def nodeDeletionHelper(self, node):
        if not node.left:
            return node.right
        elif not node.right:
            return node.left
        else:
            root = node.right
            right = node.right
            while right.left:
                right = right.left
            right.left = node.left
            return root

    def deleteNode(self, root: TreeNode | None, key: int) -> TreeNode | None:
        if not root:
            return root

        if root.val == key:
            return self.nodeDeletionHelper(root)

        parent, node = None, root
        while node and node.val != key:
            parent = node
            node = node.left if key < node.val else node.right

        if node: # Key Found
            replacement = self.nodeDeletionHelper(node)
            if parent.left is node:
                parent.left = replacement
            else:
                parent.right = replacement

        return root
```

<br><br>

## Dry Run

```ini
=====================================================
SCENARIO A: root = [5,3,6,2,4,null,7], key = 3
=====================================================

Starting Tree:

          5
         / \
        3   6
       / \   \
      2   4   7

Check 1: Is root empty?
  root = 5, not empty. Continue.

Check 2: Is root itself the key?
  root.val = 5, key = 3. 5 != 3. Not the root. Continue.

Setup:
  parent = None
  node   = 5

Iteration 1:
  Loop check: node = 5 exists, node.val (5) != key (3). Enter loop.
  parent = 5
  Is key (3) < node.val (5)? YES, go LEFT.
  node = 5.left = 3

Iteration 2:
  Loop check: node = 3 exists, node.val (3) == key (3). Exit loop.

State after search:
  parent = 5
  node   = 3   (Key Found)

Call nodeDeletionHelper(3):
  Does 3 have a left child?  YES (2)
  Does 3 have a right child? YES (4)
  Both children exist, go to the else block.

  root  = 3.right = 4     (this will replace node 3)
  right = 3.right = 4     (walker to find the smallest on the right)

  Walking left inside the right subtree:
    Is right.left (4.left) present? NO (None). Stop walking.
    Smallest node on the right side = 4

  Attach left subtree under it:
    4.left = 3.left = 2

  Return 4 as the replacement.

  The replacement subtree now looks like:

        4
       /
      2

Reconnect with parent:
  Is parent.left (5.left) the node 3? YES.
  parent.left = 4  →  5.left = 4

Final Tree:

          5
         / \
        4   6
       /     \
      2       7

Return root = 5
Output: [5,4,6,2,null,null,7]  ✓


=====================================================
SCENARIO B: root = [5,3,6,2,4,null,7], key = 0
=====================================================

Starting Tree:

          5
         / \
        3   6
       / \   \
      2   4   7

Check 1: Is root empty? NO. Continue.
Check 2: Is root.val (5) == key (0)? NO. Continue.

Setup:
  parent = None
  node   = 5

Iteration 1:
  Loop check: node = 5 exists, 5 != 0. Enter loop.
  parent = 5
  Is 0 < 5? YES, go LEFT.
  node = 3

Iteration 2:
  Loop check: node = 3 exists, 3 != 0. Enter loop.
  parent = 3
  Is 0 < 3? YES, go LEFT.
  node = 2

Iteration 3:
  Loop check: node = 2 exists, 2 != 0. Enter loop.
  parent = 2
  Is 0 < 2? YES, go LEFT.
  node = 2.left = None

Iteration 4:
  Loop check: node = None. Exit loop.

State after search:
  node = None   (Key NOT Found)

  "if node:" is False, so nothing is deleted.

Return root = 5
Output: [5,3,6,2,4,null,7]  ✓ (unchanged)


=====================================================
SCENARIO C: root = [5,3,6,2,4,null,7], key = 5  (deleting the root)
=====================================================

Starting Tree:

          5
         / \
        3   6
       / \   \
      2   4   7

Check 1: Is root empty? NO. Continue.
Check 2: Is root.val (5) == key (5)? YES.
  No parent exists, so directly return nodeDeletionHelper(5).

Call nodeDeletionHelper(5):
  Does 5 have a left child?  YES (3)
  Does 5 have a right child? YES (6)
  Both children exist, go to the else block.

  root  = 5.right = 6     (this becomes the new root)
  right = 5.right = 6

  Walking left inside the right subtree:
    Is right.left (6.left) present? NO. Stop walking.
    Smallest node on the right side = 6

  Attach left subtree under it:
    6.left = 5.left = 3   (the whole subtree 3, 2, 4 moves along)

  Return 6 as the new root.

Final Tree:

          6
         / \
        3   7
       / \
      2   4

Output: [6,3,7,2,4]  ✓ (valid BST: 2 < 3 < 4 < 6 < 7)


=====================================================
SCENARIO D: root = [], key = 0
=====================================================

Check 1: Is root empty? YES.
  Return root (None) immediately.

Output: []  ✓
```

<br><br>

## Complexity Analysis

- **Time Complexity:** `O(H)`, where `H` is the height of the tree.
  - Searching for the key walks down one path: `O(H)`.
  - Finding the smallest node in the right subtree walks down another path: `O(H)`.
  - In a balanced tree this is `O(log N)`, and in a skewed tree it is `O(N)`.
- **Space Complexity:** `O(1)`.
  - The search is iterative (a `while` loop), so no recursion stack is used.
  - Only a few pointers (`parent`, `node`, `right`) are stored.

<br><br>

## Related Problems

- [Search in a Binary Search Tree (700)](https://leetcode.com/problems/search-in-a-binary-search-tree/)
- [Insert into a Binary Search Tree (701)](https://leetcode.com/problems/insert-into-a-binary-search-tree/)
- [Validate Binary Search Tree (98)](https://leetcode.com/problems/validate-binary-search-tree/)
- [Kth Smallest Element in a BST (230)](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)
- [Inorder Successor in BST (285)](https://leetcode.com/problems/inorder-successor-in-bst/)
- [Trim a Binary Search Tree (669)](https://leetcode.com/problems/trim-a-binary-search-tree/)
- [Delete Leaves With a Given Value (1325)](https://leetcode.com/problems/delete-leaves-with-a-given-value/)
- [Delete Node in a Linked List (237)](https://leetcode.com/problems/delete-node-in-a-linked-list/)