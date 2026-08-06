# Distance Between Two Nodes in a Binary Tree
`Visnext`

## Problem Statement
Given a binary tree and two nodes, the goal is to find the shortest distance between the two nodes. The distance is defined as the number of edges between them.

## Approach
To determine the shortest distance between two nodes in a binary tree, follow these steps:

1. **Find the Lowest Common Ancestor (LCA)**: The LCA of two nodes is the deepest node that is an ancestor of both nodes.
2. **Find the Depth of Each Node from LCA**: Compute the distance of both nodes from the LCA.
3. **Calculate the Distance**: The sum of the distances from LCA to both nodes gives the shortest distance between them.

## Python Solution
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Step 1: Find the Lowest Common Ancestor (LCA)
def find_lca(root, node1, node2):
    if not root:
        return None
    if root.val == node1 or root.val == node2:
        return root
    
    left_lca = find_lca(root.left, node1, node2)
    right_lca = find_lca(root.right, node1, node2)
    
    if left_lca and right_lca:
        return root  # If node1 and node2 are in different subtrees
    
    return left_lca if left_lca else right_lca

# Step 2: Find Distance from LCA to a Given Node
def find_distance_from_lca(lca, target, distance):
    if not lca:
        return -1  # Base case: node not found
    if lca.val == target:
        return distance
    
    left_distance = find_distance_from_lca(lca.left, target, distance + 1)
    if left_distance != -1:
        return left_distance
    
    return find_distance_from_lca(lca.right, target, distance + 1)

# Step 3: Compute Distance Between Two Nodes
def find_distance(root, node1, node2):
    lca = find_lca(root, node1, node2)
    if not lca:
        return -1  # If LCA is not found, nodes are not in the tree
    
    dist1 = find_distance_from_lca(lca, node1, 0)
    dist2 = find_distance_from_lca(lca, node2, 0)
    
    return dist1 + dist2

# Example Usage:
# Constructing the tree
#         1
#        / \
#       2   3
#      / \   \
#     4   5   6
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)
root.right.right = TreeNode(6)

node1 = 4
node2 = 6

print("Distance between nodes:", find_distance(root, node1, node2))
```

## Explanation
1. **Finding LCA:** The algorithm first locates the Lowest Common Ancestor of the given nodes.
2. **Finding Distance:** It calculates the distance from the LCA to both nodes.
3. **Summing Distances:** The final distance is the sum of both distances from the LCA.

### Complexity Analysis
- **Finding LCA:** \(O(N)\) in the worst case where \(N\) is the number of nodes.
- **Finding Distance:** \(O(N)\) in the worst case for each node.
- **Total Complexity:** \(O(N)\), making this solution efficient for a binary tree.
