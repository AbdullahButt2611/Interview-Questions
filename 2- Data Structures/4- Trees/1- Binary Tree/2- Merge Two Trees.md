## Input: root1 = [1,3,2,5], root2 = [2,1,3,null,4,null,7]

## Output: [3,4,5,5,4,null,7]

> You are given two binary trees root1 and root2.

> Imagine that when you put one of them to cover the other, some nodes of the two trees are overlapped while the others are not. You need to merge the two trees into a new binary tree. The merge rule is that if two nodes overlap, then sum node values up as the new value of the merged node. Otherwise, the NOT null node will be used as the node of the new tree.

> Return the merged tree.

> Note: The merging process must start from the root nodes of both trees.

`Educative`

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def mergeTrees(root1, root2):
    if not root1 and not root2:
        return None
    if not root1:
        return root2
    if not root2:
        return root1
    
    merged = TreeNode(root1.val + root2.val)
    merged.left = mergeTrees(root1.left, root2.left)
    merged.right = mergeTrees(root1.right, root2.right)
    
    return merged

def array_to_tree(arr):
    if not arr:
        return None
    root = TreeNode(arr[0])
    queue = [root]
    i = 1
    while queue and i < len(arr):
        node = queue.pop(0)
        if arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            queue.append(node.right)
        i += 1
    return root

def tree_to_array(root):
    if not root:
        return []
    result = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    while result[-1] is None:
        result.pop()
    return result

# Input arrays representing trees
root1 = [1, 3, 2, 5]
root2 = [2, 1, 3, None, 4, None, 7]

# Construct trees from arrays
tree1 = array_to_tree(root1)
tree2 = array_to_tree(root2)

# Merge trees
merged_tree = mergeTrees(tree1, tree2)

# Convert merged tree back to array for output
result_array = tree_to_array(merged_tree)
print(result_array)
```