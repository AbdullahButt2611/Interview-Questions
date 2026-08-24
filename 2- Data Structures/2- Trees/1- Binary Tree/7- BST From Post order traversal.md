## Construct BST where post order traversal is given: [1, 7, 5, 50, 40, 10]
`Educative`

To construct a Binary Search Tree (BST) from its postorder traversal, you can follow these steps:

- The last element of the postorder traversal is the root of the BST.
- All elements to the left of the root in the postorder traversal are part of the left subtree.
- All elements to the right of the root in the postorder traversal are part of the right subtree.
- Recursively apply the above steps to construct the left and right subtrees.

Here's a Python function to construct the BST:

```python
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def constructBSTFromPostorder(postorder):
    if not postorder:
        return None
    
    root_val = postorder.pop()  # Last element is the root
    root = TreeNode(root_val)
    
    # Find the index where the left subtree ends
    split_index = len(postorder)
    for i in range(len(postorder)):
        if postorder[i] > root_val:
            split_index = i
            break
    
    # Construct left and right subtrees recursively
    root.right = constructBSTFromPostorder(postorder[split_index:])
    root.left = constructBSTFromPostorder(postorder[:split_index])
    
    return root

def inorderTraversal(root):
    if root:
        inorderTraversal(root.left)
        print(root.val, end=' ')
        inorderTraversal(root.right)

# Example usage:
postorder = [1, 7, 5, 50, 40, 10]
root = constructBSTFromPostorder(postorder)
print("Inorder Traversal of the constructed BST:")
inorderTraversal(root)
```

This code takes a list representing the postorder traversal of the BST and constructs the BST accordingly. Then, it prints the inorder traversal of the constructed BST to verify its correctness. You can replace the postorder list with your own list to construct different BSTs.