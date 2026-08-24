## Given a binary tree, determine if it is a valid binary search tree (BST).
`Educative`

To determine if a binary tree is a valid binary search tree (BST), you can perform an inorder traversal of the tree and check if the resulting sequence is sorted in ascending order. If it is, then the tree is a valid BST; otherwise, it's not. This approach works because for a BST, an inorder traversal produces elements in sorted order.

Here's how you can implement this approach in Python:

```python
class TreeNode:
    def __init__(self, value=0, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def is_valid_BST(root):
    # Helper function for inorder traversal
    def inorder_traversal(node, values):
        if node:
            inorder_traversal(node.left, values)
            values.append(node.value)
            inorder_traversal(node.right, values)

    # Perform inorder traversal to get the sorted sequence
    sorted_values = []
    inorder_traversal(root, sorted_values)

    # Check if the sorted sequence is in ascending order
    for i in range(1, len(sorted_values)):
        if sorted_values[i] <= sorted_values[i - 1]:
            return False
    
    return True

# Example usage:
# Constructing a sample binary search tree
root = TreeNode(2)
root.left = TreeNode(1)
root.right = TreeNode(3)

# Check if the tree is a valid BST
if is_valid_BST(root):
    print("The binary tree is a valid BST.")
else:
    print("The binary tree is not a valid BST.")
```

### Recursive Solution

```python
class TreeNode:
    def __init__(self, value=0, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def is_valid_BST(root):
    # Helper function to validate BST recursively
    def is_valid(node, min_val=float('-inf'), max_val=float('inf')):
        if node is None:
            return True
        
        # Check if the current node value is within the valid range
        if not (min_val < node.value < max_val):
            return False
        
        # Recursively check the left and right subtrees
        return (is_valid(node.left, min_val, node.value) and
                is_valid(node.right, node.value, max_val))

    # Start the validation from the root with default range values
    return is_valid(root)

# Example usage:
# Constructing a sample binary search tree
root = TreeNode(2)
root.left = TreeNode(1)
root.right = TreeNode(3)

# Check if the tree is a valid BST
if is_valid_BST(root):
    print("The binary tree is a valid BST.")
else:
    print("The binary tree is not a valid BST.")
```

This recursive solution uses a helper function is_valid which checks if the current node's value is within the valid range defined by min_val and max_val. It recursively validates the left and right subtrees while updating the range accordingly. The is_valid_BST function initiates the validation process from the root node with default range values of negative infinity and positive infinity. If the tree is a valid BST, the function returns True; otherwise, it returns False.