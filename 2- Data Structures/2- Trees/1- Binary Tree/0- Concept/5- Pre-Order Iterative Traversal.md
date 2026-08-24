# Preorder Traversal (Iterative Approach)

`Meta` • `Amazon` • `Google` • `OpenAI` • `Anthropic`

## Problem Statement
Given the `root` of a binary tree, return the **preorder traversal** of the binary tree.

Preorder means we visit the nodes in this order:

- First the **Root** (current node)
- Then the **Left** subtree
- Then the **Right** subtree

So the rule to always remember is: <mark>Root → Left → Right</mark>

## Examples

**Example 1**

```ini
Input  : root = [1, 4, null, 4, 2]
Output : [1, 4, 4, 2]
```

**Example 2**

```ini
Input  : root = [1]
Output : [1]
```

## Constraints

- `1 <= Number of Nodes <= 100`
- `-100 <= Node.val <= 100`

<br><br>

## Approach

We want to visit nodes in the order **Root → Left → Right**, but without using recursion. To do this by hand, we use a **stack** (a last in, first out box). The stack simply remembers which nodes we still need to visit.

Here is the plain idea behind it:

- A stack always gives us back the **last thing we put in first**. We use this behavior to control the order in which nodes come out.
- Every time we pop a node from the stack, we immediately record its value. That takes care of the **Root** part.
- Now here is the small trick. We want **Left** to be handled before **Right**. Since the stack reverses the order (last in comes out first), we push the **Right child first** and the **Left child second**. That way, the Left child sits on top and gets popped next.

So the whole thing runs like a simple loop:

- Put the root inside the stack to begin.
- Keep going while the stack still has something in it.
- Pop the top node, write down its value.
- Push its right child (if it exists), then push its left child (if it exists).
- Repeat until the stack is empty.

The reason this works is that the stack is doing the exact job that recursion would normally do for us behind the scenes. Instead of the computer remembering the pending nodes on its own, **we remember them ourselves inside the stack**. Once you see that the stack is just a to-do list of nodes, the whole approach becomes easy to hold onto forever.

<br><br>

## Code

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def preorderTraversal(root):
    if not root:
        return []

    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)

        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return result
```

<br><br>

## Dry Run

We will use the tree from Example 1 where the root is `1`, its left child is `4`, that `4` has a left child `4` and a right child `2`.

```ini
Tree structure:

        1
       /
      4
     / \
    4   2

Start:
stack   = [1]
result  = []

Iteration 1:
- Pop 1 from stack        -> node = 1
- Add 1 to result         -> result = [1]
- Node 1 has no right child, skip
- Node 1 has left child 4 -> push 4
stack   = [4]
result  = [1]

Iteration 2:
- Pop 4 from stack        -> node = 4
- Add 4 to result         -> result = [1, 4]
- Node 4 has right child 2 -> push 2
- Node 4 has left child 4  -> push 4
stack   = [2, 4]        (4 is on top because it was pushed last)
result  = [1, 4]

Iteration 3:
- Pop 4 from stack        -> node = 4
- Add 4 to result         -> result = [1, 4, 4]
- Node 4 has no right child, skip
- Node 4 has no left child, skip
stack   = [2]
result  = [1, 4, 4]

Iteration 4:
- Pop 2 from stack        -> node = 2
- Add 2 to result         -> result = [1, 4, 4, 2]
- Node 2 has no right child, skip
- Node 2 has no left child, skip
stack   = []
result  = [1, 4, 4, 2]

Stack is now empty, loop ends.

Final Output: [1, 4, 4, 2]
```

<br><br>

## Complexity

- **Time Complexity:** `O(n)` because we visit every node exactly once, where `n` is the number of nodes.
- **Space Complexity:** `O(n)` in the worst case for the stack, since it may hold many nodes at the same time.

<br><br>

## Related Problems

- [Binary Tree Inorder Traversal (94)](https://leetcode.com/problems/binary-tree-inorder-traversal/)
- [Binary Tree Postorder Traversal (145)](https://leetcode.com/problems/binary-tree-postorder-traversal/)
- [Binary Tree Level Order Traversal (102)](https://leetcode.com/problems/binary-tree-level-order-traversal/)
- [N-ary Tree Preorder Traversal (589)](https://leetcode.com/problems/n-ary-tree-preorder-traversal/)
- [Construct Binary Tree from Preorder and Inorder Traversal (105)](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)