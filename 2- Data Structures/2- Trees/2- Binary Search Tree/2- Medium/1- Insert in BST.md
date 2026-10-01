# Insert into a Binary Search Tree

`Amazon` • `Microsoft` • `Meta` • `Google` • `LinkedIn` • `Bloomberg`

## Problem Statement
You are given the `root` node of a binary search tree (BST) and a value to insert into the tree. Return the root node of the BST after the insertion. It is guaranteed that the new value does not exist in the original BST.

Notice that there may exist multiple valid ways for the insertion, as long as the tree remains a BST after insertion. You can return any of them.

## Examples
**Example 1:**

```ini
Input: root = [4,2,7,1,3], val = 5
Output: [4,2,7,1,3,5]
```

**Example 2:**

```ini
Input: root = [40,20,60,10,30,50,70], val = 25
Output: [40,20,60,10,30,50,70,null,null,25]
```

**Example 3:**

```ini
Input: root = [4,2,7,1,3,null,null,null,null,null,null], val = 5
Output: [4,2,7,1,3,5]
```

## Constraints
- The number of nodes in the tree will be in the range `[0, 10^4]`.
- `-10^8 <= Node.val <= 10^8`
- All the values `Node.val` are unique.
- `-10^8 <= val <= 10^8`
- It is guaranteed that `val` does not exist in the original BST.

<br><br>

## Approach
The whole trick here comes from one simple rule that every BST follows: for any node, everything smaller goes to its left and everything bigger goes to its right. If we always respect that rule, we will naturally land on the exact empty spot where our new value belongs.

So first we create the new node that holds our value, since we know we will need it no matter what.

Then we handle the easiest case. If the tree is empty (there is no root), the new node simply becomes the whole tree, so we return it directly.

If the tree is not empty, we start walking from the root and keep comparing our value with the current node:

- If our value is bigger than the current node, it belongs somewhere on the right side. So we look to the right. If the right spot is empty, we have found its home, so we attach the new node there and stop. If the right spot is already taken, we move down into that right child and repeat.
- If our value is smaller (or equal in the general case), it belongs on the left side. So we look to the left. If the left spot is empty, we attach the new node there and stop. Otherwise we move down into that left child and repeat.

We keep doing this walk, going left or right based on the comparison, until we find an empty spot to hang the new node. Because the new value is guaranteed not to already exist, we will always eventually reach an empty position.

Finally, we return the original `root`. We never changed where the root is, we only attached a new node somewhere deeper inside the tree.

<mark>The key idea: inserting into a BST is just a guided walk down the tree. Keep comparing and moving in the direction the BST rule tells you, and the correct empty slot reveals itself on its own.</mark>

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
    def insertIntoBST(self, root: TreeNode | None, val: int) -> TreeNode | None:
        node = TreeNode(val=val)

        if not root:
            return node

        curr = root
        while True:
            if val > curr.val:                 # Right Side
                if not curr.right:
                    curr.right = node
                    break
                curr = curr.right
            else:                               # Left Side
                if not curr.left:
                    curr.left = node
                    break
                curr = curr.left
        
        return root
```

<br><br>

## Dry Run
Let us walk through `root = [40,20,60,10,30,50,70]` with `val = 25` step by step. The tree looks like this to begin with:

```ini
            40
           /  \
         20    60
        /  \   /  \
      10   30 50   70
```

```ini
Input: root = [40,20,60,10,30,50,70], val = 25

Initial State:
Create node with val = 25  ->  node = (25)
Root exists, so we start walking.
curr = 40

Iteration 1 -> curr = 40
  Compare: is 25 > 40? No.
  So we go to the Left Side.
  Is curr.left empty? No, left child is 20.
  Action: move down to the left child.
  curr = 20

Iteration 2 -> curr = 20
  Compare: is 25 > 20? Yes.
  So we go to the Right Side.
  Is curr.right empty? No, right child is 30.
  Action: move down to the right child.
  curr = 30

Iteration 3 -> curr = 30
  Compare: is 25 > 30? No.
  So we go to the Left Side.
  Is curr.left empty? Yes, there is nothing there.
  Action: attach node (25) as the left child of 30, then stop.
  30.left = 25

Loop breaks because we placed the node.

Return the original root (40).
```

The tree after insertion becomes:

```ini
            40
           /  \
         20    60
        /  \   /  \
      10   30 50   70
           /
         25
```

```ini
Output: [40,20,60,10,30,50,70,null,null,25]
```

<br><br>

## Complexity
- **Time Complexity:** `O(h)` where `h` is the height of the tree, because we walk down one path from the root to an empty spot. In a balanced tree this is `O(log n)`, and in the worst case (a tree shaped like a straight line) it becomes `O(n)`.
- **Space Complexity:** `O(1)` because we only use a couple of pointers and do not use any extra recursion or data structures.

<br><br>

## Related Problems
- [Search in a Binary Search Tree (700)](https://leetcode.com/problems/search-in-a-binary-search-tree/)
- [Delete Node in a BST (450)](https://leetcode.com/problems/delete-node-in-a-bst/)
- [Validate Binary Search Tree (98)](https://leetcode.com/problems/validate-binary-search-tree/)
- [Convert Sorted Array to Binary Search Tree (108)](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/)
- [Trim a Binary Search Tree (669)](https://leetcode.com/problems/trim-a-binary-search-tree/)
- [Balance a Binary Search Tree (1382)](https://leetcode.com/problems/balance-a-binary-search-tree/)