# Boundary Traversal of Binary Tree

`Amazon` • `Microsoft` • `eBay` • `Morgan Stanley` • `Google`

## Problem Statement

Given the `root` of a Binary Tree, perform the boundary traversal of the tree.

The boundary traversal means visiting the boundary nodes of the tree in the anticlockwise direction, starting from the root.

The boundary is the concatenation of these four parts, in this exact order:

- The **root**.
- The **left boundary** (top to bottom), not including any leaf.
- The **leaves**, from left to right.
- The **right boundary** (added in bottom to top order), not including any leaf.

Rules for the **left boundary**:

- The root's left child is in the left boundary. If the root has no left child, the left boundary is empty.
- If a node is in the left boundary and has a left child, that left child is also in the left boundary.
- If a node is in the left boundary, has no left child but has a right child, that right child is in the left boundary.
- The leftmost leaf is not part of the left boundary.

Rules for the **right boundary** are the mirror image of the above (walk the right side of the root's right subtree). The leaf is again not included, and the right boundary is empty if the root has no right child.

## Examples

**Example 1**

```ini
Input  : root = [1, 2, 3, 4, 5, 6, 7, null, null, 8, 9]
Output : [1, 2, 4, 8, 9, 6, 7, 3]
```

**Example 2**

```ini
Input  : root = [1, 2, null, 4, 9, 6, 5, 3, null, null, null, null, null, 7, 8]
Output : [1, 2, 4, 6, 5, 7, 8]
```

## Constraints

- `0 <= Number of Nodes <= 10^4`
- `-10^3 <= Node.val <= 10^3`

<br><br>

## Approach

The whole idea fits in one sentence: walk around the outside of the tree, counter clockwise, like tracing its outline with a pencil.

Here is the tree we will use to picture it (the same one in the diagram):

![Boundary Traversal Tree](../../../../images/Binary%20Trees/2_2_1_3_2.png)

That single walk is broken into **three simple parts that never overlap**:

- **Down the left wall.** Start at the root and keep stepping to the left child. If a node has no left child, step to its right child instead. Keep going until you reach a leaf. Add every node you pass on the way down (but not the leaf, it gets picked up in the next part).
- **Along the floor.** Collect every leaf from left to right. A plain depth first walk does this for you: because you always visit the left side before the right side, the leaves come out in left to right order on their own.
- **Up the right wall.** Start on the root's right side and keep stepping to the right child. If a node has no right child, step to its left child instead. Stop at the leaf. This wall has to come out bottom to top, so you add each node while coming back up, not while going down.

The one clever bit is **when you add the node**:

- On the left wall you want top to bottom, and you are already moving top to bottom, so you add the node **before** you go deeper.
- On the right wall you want bottom to top, but you are moving top to bottom, so you add the node **after** the deeper call finishes. Recursion always unwinds from the deepest node back up, so it hands you the bottom to top order for free.

<mark>The only real difference between the left wall and the right wall is one line: add the node before going deeper (left) versus after coming back (right). Same idea, just flipped.</mark>

**Why leaves are skipped on the two walls:**

- A corner leaf could be reached both by a wall and by the floor pass. Skipping leaves on the walls makes sure no node is ever printed twice.

**The catch most people miss:**

- Look at the diagram. Nodes `5` and `6` are not leaves, and they are not on the outline either. Boundary is not "whatever the shape looks like", it is a strict path rule (keep going left, or keep going right). That is exactly why `5` and `6` are left out even though they sit right in the middle of the picture.

If you can say out loud why `5` and `6` are not on the boundary, you have understood the idea, not just memorized it.

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
    def leafBoundary(self, node, boundary):
        if node == None: return
    
        self.leafBoundary(node.left, boundary)
        if node.left == None and node.right == None:
            boundary.append(node.data)
        self.leafBoundary(node.right, boundary)
            
        
    def leftBoundary(self, node, boundary):
        if node.left == None and node.right == None: return
        boundary.append(node.data)
        
        if node.left:
            self.leftBoundary(node.left, boundary)
        elif node.right:
            self.leftBoundary(node.right, boundary)
            
    def rightBoundary(self, node, boundary):
        if node.left == None and node.right == None: return
        
        if node.right:
            self.rightBoundary(node.right, boundary)
        elif node.left:
            self.rightBoundary(node.left, boundary)
            
        boundary.append(node.data)
    def boundary(self, root):
        boundary = []
        
        if root == None:
            return boundary
            
        self.leftBoundary(root, boundary)
        self.leafBoundary(root, boundary)
        if root.right:
            self.rightBoundary(root.right, boundary)
        return boundary
```

<br><br>

## Dry Run

We will trace the tree from the diagram, step by step, so you can see exactly what enters the list at each moment.

```ini
The tree we are tracing:

              1
            /   \
           2       3
          / \     / \
         4   5   6   7
        /     \   \
       8       9   10

Leaf nodes  : 8, 9, 10, 7
boundary    : []   (this is the list we keep filling)


=========================================================
PHASE 1  ->  LEFT BOUNDARY   (call leftBoundary(root = 1))
Rule: add the node FIRST, then step down (left, else right).
=========================================================

Step 1: at node 1
        - is 1 a leaf? no  -> continue
        - add 1
        - node 1 has a left child (2) -> go left
        boundary = [1]

Step 2: at node 2
        - is 2 a leaf? no  -> continue
        - add 2
        - node 2 has a left child (4) -> go left
        boundary = [1, 2]

Step 3: at node 4
        - is 4 a leaf? no (it has left child 8) -> continue
        - add 4
        - node 4 has a left child (8) -> go left
        boundary = [1, 2, 4]

Step 4: at node 8
        - is 8 a leaf? YES -> stop this walk, add nothing
        boundary = [1, 2, 4]

Left boundary done -> boundary = [1, 2, 4]


=========================================================
PHASE 2  ->  LEAVES          (call leafBoundary(root = 1))
Rule: normal in-order walk, add a node only if it is a leaf.
      Left side is always visited before right side, so
      leaves fall out in left-to-right order automatically.
=========================================================

Step 1: dive left all the way, reach node 8
        - 8 has no children -> it is a leaf -> add 8
        boundary = [1, 2, 4, 8]

Step 2: come back up through 4 and 2
        - 4 is not a leaf -> skip
        - 2 is not a leaf -> skip

Step 3: go into 5's side, reach node 9
        - 9 has no children -> it is a leaf -> add 9
        boundary = [1, 2, 4, 8, 9]

Step 4: come back up through 5 and 1
        - 5 is not a leaf -> skip
        - 1 is not a leaf -> skip

Step 5: go into the right side, reach node 10
        - 10 has no children -> it is a leaf -> add 10
        boundary = [1, 2, 4, 8, 9, 10]

Step 6: come back up through 6 and 3
        - 6 is not a leaf -> skip
        - 3 is not a leaf -> skip

Step 7: reach node 7
        - 7 has no children -> it is a leaf -> add 7
        boundary = [1, 2, 4, 8, 9, 10, 7]

Leaves done -> boundary = [1, 2, 4, 8, 9, 10, 7]


=========================================================
PHASE 3  ->  RIGHT BOUNDARY  (call rightBoundary(root.right = 3))
Rule: step down FIRST (right, else left), add the node AFTER
      the deeper call returns, so nodes come out bottom-to-top.
=========================================================

Step 1: at node 3
        - is 3 a leaf? no -> continue
        - node 3 has a right child (7) -> go right FIRST
          (we will add 3 only after this deeper call finishes)

Step 2: at node 7
        - is 7 a leaf? YES -> stop, add nothing
        - return back up to node 3

Step 3: back at node 3 (deeper call finished)
        - now add 3
        boundary = [1, 2, 4, 8, 9, 10, 7, 3]

Right boundary done -> boundary = [1, 2, 4, 8, 9, 10, 7, 3]


=========================================================
FINAL ANSWER
=========================================================
boundary = [1, 2, 4, 8, 9, 10, 7, 3]
```

Notice how internal nodes `5` and `6` were correctly left out. They were never on a wall path, and they are not leaves, so no phase ever added them.

<br><br>

## Complexity

- **Time:** `O(n)`, since each node is visited a constant number of times across the three passes.
- **Space:** `O(h)`, where `h` is the height of the tree, for the recursion call stack.

<br><br>

## Related Problems

- [Binary Tree Right Side View (199)](https://leetcode.com/problems/binary-tree-right-side-view/)
- [Find Leaves of Binary Tree (366)](https://leetcode.com/problems/find-leaves-of-binary-tree/)
- [Binary Tree Level Order Traversal (102)](https://leetcode.com/problems/binary-tree-level-order-traversal/)
- [Vertical Order Traversal of a Binary Tree (987)](https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree/)
- [Binary Tree Preorder Traversal (144)](https://leetcode.com/problems/binary-tree-preorder-traversal/)
- [Binary Tree Postorder Traversal (145)](https://leetcode.com/problems/binary-tree-postorder-traversal/)