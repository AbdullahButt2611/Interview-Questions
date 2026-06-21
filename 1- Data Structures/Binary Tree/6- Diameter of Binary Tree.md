## Calculate length of binary tree ( max distance from one node to other ) (aka diameter of tree)
`Educative`

```python
class Solution:
    def diameterOfBinaryTree(self, root):
        diameter = [0]
        self.height(root, diameter)
        return diameter[0]

    def height(self, node, diameter):
        if node is None:
            return 0
        lh = self.height(node.left, diameter)
        rh = self.height(node.right, diameter)
        diameter[0] = max(diameter[0], lh + rh)
        return 1 + max(lh, rh)

# Example usage:
# Constructing a sample binary tree
#         1
#       /   \
#      2     3
#     / \   / \
#    4   5 6   7
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)
root.right.left = TreeNode(6)
root.right.right = TreeNode(7)

solution = Solution()
print("Diameter of the binary tree:", solution.diameterOfBinaryTree(root))
```