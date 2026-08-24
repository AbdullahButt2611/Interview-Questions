# Check if Two Binary Trees are Identical

`Educative`

```python
def are_identical(root1, root2):
    # Returns true if both trees have null as root (first base case)
    if not root1 and not root2:
        return True

    # Function returns false if one of the roots here is null (second base case)
    if root1 and root2:
        # Returns true if both nodes have the same left sub-tree, right sub-tree
        # and value
        return (root1.data == root2.data and
                are_identical(root1.left, root2.left) and
                are_identical(root1.right, root2.right))

    # Returns false if neither of the above cases are satisfied
    return False
```