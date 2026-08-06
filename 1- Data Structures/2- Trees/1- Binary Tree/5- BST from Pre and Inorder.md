## Construct a Binary Tree from PreOrder and Inorder arrays
`Educative`

Using hashing to optimize the search for the index of the root element in the inorder array can improve the time complexity of the algorithm. Here's how you can modify the previous code to utilize hashing:

```python
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def buildTree(preorder, inorder):
    if not preorder or not inorder:
        return None
    
    # Create a hashmap to store the index of elements in inorder array
    inorder_map = {val: idx for idx, val in enumerate(inorder)}
    
    def helper(preorder, inorder_start, inorder_end):
        nonlocal preorder_idx
        
        if inorder_start > inorder_end:
            return None
        
        root_val = preorder[preorder_idx]
        root = TreeNode(root_val)
        
        inorder_idx = inorder_map[root_val]
        
        preorder_idx += 1
        
        root.left = helper(preorder, inorder_start, inorder_idx - 1)
        root.right = helper(preorder, inorder_idx + 1, inorder_end)
        
        return root
    
    preorder_idx = 0
    return helper(preorder, 0, len(inorder) - 1)

def inorder_traversal(root):
    if root:
        inorder_traversal(root.left)
        print(root.val, end=" ")
        inorder_traversal(root.right)

def preorder_traversal(root):
    if root:
        print(root.val, end=" ")
        preorder_traversal(root.left)
        preorder_traversal(root.right)

# Example usage:
preorder = [3, 9, 20, 15, 7]
inorder = [9, 3, 15, 20, 7]

root = buildTree(preorder, inorder)

print("Inorder Traversal:")
inorder_traversal(root)
print("\nPreorder Traversal:")
preorder_traversal(root)
```
