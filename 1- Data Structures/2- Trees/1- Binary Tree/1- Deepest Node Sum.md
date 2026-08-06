# Deepest Leaves Sum
`Educative`

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def __init__(self):
        self.sum = 0

    def deepestLeavesSum(self, root):
        max_depth = self.maxDepth(root)
        self.findSum(root, 1, max_depth)
        return self.sum

    def maxDepth(self, node):
        if not node:
            return 0
        return 1 + max(self.maxDepth(node.left), self.maxDepth(node.right))

    def findSum(self, node, curr, depth):
        if node is not None:
            if curr == depth:
                self.sum += node.val
            self.findSum(node.left, curr + 1, depth)
            self.findSum(node.right, curr + 1, depth)

# Example usage:
# Constructing a sample binary tree
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)
root.right.right = TreeNode(6)
root.left.left.left = TreeNode(7)
root.right.right.right = TreeNode(8)

solution = Solution()
print(solution.deepestLeavesSum(root))  # Output should be 15
```