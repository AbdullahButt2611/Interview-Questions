# Iterative Postorder Traversal using 2 Stacks

`Amazon` • `Adobe` • `FactSet` • `Paytm` • `Fourkites`

## Problem Statement
Given the `root` of a binary tree, return the **postorder** traversal of the binary tree.

Postorder means we read the tree in the order: left child, then right child, then the node itself (left, right, root).

## Examples
**Example 1**

```ini
Input  : root = [1, 4, null, 4, 2]
Output : [4, 2, 4, 1]
```

**Example 2**

```ini
Input  : root = [1, null, 2, 3]
Output : [3, 2, 1]
```

## Constraints
- `1 <= Number of Nodes <= 100`
- `-100 <= Node.val <= 100`

<br><br>

## Approach

Postorder reads a tree as **left, right, root**. The tricky part is that the node itself must come **last**, only after both of its children are finished. Handling that directly with a plain loop gets messy.

So this approach uses one neat observation:

- The **reverse** of postorder (left, right, root) is **root, right, left**.
- The order "root, right, left" is very easy to build with a simple loop (it is just a small twist on preorder).
- So the plan becomes: build "root, right, left" first, then flip it, and we land exactly on postorder.

Here is the raw idea, step by step:

- Take a stack (call it the **traverse stack**) and put the `root` inside it to start.
- Repeat until this stack is empty:
  - Pop the top node.
  - Put that popped node into a second stack (call it the **collect stack**).
  - Push its **left** child first, then its **right** child, into the traverse stack.
- When the traverse stack is empty, the collect stack now holds every node in "root, right, left" order.
- Pop everything out of the collect stack one by one. Because a stack reverses whatever you put in, what comes out is "left, right, root", which is the postorder we wanted.

**Why push left first and then right?**

A stack always hands back the **last** thing you pushed. By pushing left before right, the right child ends up on top, so it gets popped and processed **before** the left child. That is what gives us the "right before left" part of the reversed order.

<br><br>

## Why 2 Stacks (and what each one does)

This is the heart of the trick, so let me split the two stacks clearly.

**Stack 1, the traverse stack (the worker)**
- Its only job is to walk the tree and decide who to visit next.
- Every time we pop from it, we hand that node over to Stack 2, and then push that node's children back into Stack 1.
- It controls the traversal and produces nodes in "root, right, left" order (the reverse of the answer).

**Stack 2, the collect stack (the recorder)**
- We never pop from it during the walk, we only keep stacking nodes on top of it.
- Because it receives nodes in "root, right, left" order, and a stack gives things back in reverse, popping it at the very end flips the whole sequence into "left, right, root".

<mark>Stack 2 exists purely to reverse the order for us, using the natural LIFO (last in, first out) behaviour of a stack, instead of us writing extra reversing code by hand.</mark>

In one line: Stack 1 generates the reverse of the answer, and Stack 2 turns that reverse back into the answer.

<br><br>

## Complexity
- **Time:** `O(N)`, because every node is pushed and popped a fixed number of times.
- **Space:** `O(N)`, because both stacks together can hold all the nodes.

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
    def postorder(self, root):
        tree_stack = []
        if root == None:
            return tree_stack

        tree = []
        traverse_stack = [root]

        while traverse_stack:
            node = traverse_stack.pop()
            tree_stack.append(node)

            if node.left:
                traverse_stack.append(node.left)

            if node.right:
                traverse_stack.append(node.right)

        while tree_stack:
            tree.append(tree_stack.pop().data)

        return tree
```

<br><br>

## Dry Run

```ini
Input tree for [1, 4, null, 4, 2]:

            1
           /
          4              <- middle 4
         / \
        4   2            <- left 4 , right 2

Goal: postorder = left, right, root

We use:
  traverse_stack  (Stack 1) -> walks the tree
  tree_stack      (Stack 2) -> collects nodes so we can reverse them later
  tree                      -> final answer

Start:
  traverse_stack = [1]
  tree_stack     = []

Iteration 1:
  pop 1 from traverse_stack
  push 1 into tree_stack
  1.left  = 4(middle)  -> push it
  1.right = null       -> skip
  traverse_stack = [4(middle)]
  tree_stack     = [1]

Iteration 2:
  pop 4(middle) from traverse_stack
  push 4(middle) into tree_stack
  4(middle).left  = 4(left)  -> push it
  4(middle).right = 2        -> push it
  traverse_stack = [4(left), 2]
  tree_stack     = [1, 4(middle)]

Iteration 3:
  pop 2 from traverse_stack   (2 is on top, it was pushed last)
  push 2 into tree_stack
  2.left  = null  -> skip
  2.right = null  -> skip
  traverse_stack = [4(left)]
  tree_stack     = [1, 4(middle), 2]

Iteration 4:
  pop 4(left) from traverse_stack
  push 4(left) into tree_stack
  4(left).left  = null  -> skip
  4(left).right = null  -> skip
  traverse_stack = []            (empty, so the first loop ends)
  tree_stack     = [1, 4(middle), 2, 4(left)]

Now empty tree_stack into the answer (always pop from the top):
  pop 4(left)   -> tree = [4]
  pop 2         -> tree = [4, 2]
  pop 4(middle) -> tree = [4, 2, 4]
  pop 1         -> tree = [4, 2, 4, 1]

Final answer: [4, 2, 4, 1]
```

<br><br>

## Related Problems
- [Binary Tree Postorder Traversal (145)](https://leetcode.com/problems/binary-tree-postorder-traversal/)
- [Binary Tree Preorder Traversal (144)](https://leetcode.com/problems/binary-tree-preorder-traversal/)
- [Binary Tree Inorder Traversal (94)](https://leetcode.com/problems/binary-tree-inorder-traversal/)
- [Binary Tree Level Order Traversal (102)](https://leetcode.com/problems/binary-tree-level-order-traversal/)
- [N-ary Tree Postorder Traversal (590)](https://leetcode.com/problems/n-ary-tree-postorder-traversal/)