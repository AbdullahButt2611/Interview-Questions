# Iterative Inorder Traversal

`Microsoft` • `Adobe` • `Apple` • `Amazon` • `Google`

## Problem Statement

Given the `root` of a binary tree, return the **inorder** traversal of the binary tree.

In an inorder traversal, we visit the nodes in this order:

- First, the entire **left** subtree
- Then, the **current (root)** node
- Finally, the entire **right** subtree

The catch here is that we need to do this **iteratively** (using a loop and a stack), not with recursion.

## Examples

**Example 1**

```ini
Input  : root = [1, 4, null, 4, 2]
Output : [4, 4, 2, 1]
```

**Example 2**

```ini
Input  : root = [1, null, 2, 3]
Output : [1, 3, 2]
```

## Constraints

- `1 <= Number of Nodes <= 100`
- `-100 <= Node.val <= 100`

<br><br>

## Approach

When we do inorder traversal with recursion, the computer keeps track of things for us behind the scenes using something called the **call stack**. When we go iterative, we simply do that same bookkeeping ourselves using our **own stack**.

The whole idea rests on one simple rule of inorder: <mark>always finish the left side of a node before you are allowed to visit the node itself.</mark>

So we keep asking one question again and again: "Is there a left child I still need to go into?"

Here is the plain thinking, step by step:

- We keep a pointer called `node` that tells us where we currently are, and we start it at the `root`.

- We also keep an empty `stack` (to remember nodes we have to come back to later) and an empty list `inOrder` (our final answer).

- **If the current node is not empty**, that means we still have a left path to explore. So we push this node onto the stack (a promise that "I will come back to you later") and move left by setting `node = node.left`. We keep sliding left like this until there is nothing more on the left.

- **If the current node is empty**, it means we have hit a dead end on the left. Now it is time to come back. We pop the most recent node from the stack, record its value into our answer, and then turn our attention to its **right** side by setting `node = node.right`.

- We repeat this over and over. The moment the current node is empty **and** the stack is also empty, it means there is nothing left to come back to, so we stop.

In short, we slide left and stack nodes on the way down, then pop them one by one on the way back up, recording each value right when we pop it and then exploring its right child. That popping order is exactly what gives us Left, Node, Right.

**Time Complexity:** `O(n)`, because we touch every node exactly once.

**Space Complexity:** `O(h)`, where `h` is the height of the tree (this is the most nodes the stack holds at any moment). In the worst case of a fully skewed tree, this becomes `O(n)`.

<br><br>

## Code

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.data = val
#         self.left = left
#         self.right = right

class Solution:
    def inorder(self, root):
        stack = []
        inOrder = []
        node = root

        while True:
            if node is not None:
                stack.append(node)
                node = node.left
            else:
                if not stack:
                    break

                node = stack.pop()
                inOrder.append(node.data)
                node = node.right

        return inOrder
```

<br><br>

## Dry Run

Let us walk through **Example 2** where `root = [1, null, 2, 3]`.

The tree looks like this:

```ini
      1
       \
        2
       /
      3
```

Now here is exactly what happens on every single pass of the loop:

```ini
Start : node = 1, stack = [], inOrder = []

Iteration 1:
  node is 1 (not None)
  -> push 1 onto stack
  -> move left: node = 1.left = None
  stack = [1], inOrder = []

Iteration 2:
  node is None
  stack is not empty
  -> pop 1 from stack, record its value
  -> move right: node = 1.right = 2
  stack = [], inOrder = [1]

Iteration 3:
  node is 2 (not None)
  -> push 2 onto stack
  -> move left: node = 2.left = 3
  stack = [2], inOrder = [1]

Iteration 4:
  node is 3 (not None)
  -> push 3 onto stack
  -> move left: node = 3.left = None
  stack = [2, 3], inOrder = [1]

Iteration 5:
  node is None
  stack is not empty
  -> pop 3 from stack, record its value
  -> move right: node = 3.right = None
  stack = [2], inOrder = [1, 3]

Iteration 6:
  node is None
  stack is not empty
  -> pop 2 from stack, record its value
  -> move right: node = 2.right = None
  stack = [], inOrder = [1, 3, 2]

Iteration 7:
  node is None
  stack is empty
  -> break out of the loop

Final Answer: inOrder = [1, 3, 2]
```

Notice how each value gets added to the answer **only at the moment we pop it**, right after its whole left side is done. That is what keeps the output in perfect Left, Node, Right order.

<br><br>

## Related Problems

- [Binary Tree Inorder Traversal (94)](https://leetcode.com/problems/binary-tree-inorder-traversal/)
- [Binary Tree Preorder Traversal (144)](https://leetcode.com/problems/binary-tree-preorder-traversal/)
- [Binary Tree Postorder Traversal (145)](https://leetcode.com/problems/binary-tree-postorder-traversal/)
- [Binary Search Tree Iterator (173)](https://leetcode.com/problems/binary-search-tree-iterator/)
- [Kth Smallest Element in a BST (230)](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)
- [Validate Binary Search Tree (98)](https://leetcode.com/problems/validate-binary-search-tree/)