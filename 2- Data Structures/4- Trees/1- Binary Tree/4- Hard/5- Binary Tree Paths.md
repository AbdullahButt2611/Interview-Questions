# Binary Tree Paths

`Amazon` • `Meta` • `Microsoft` • `Google` • `Gopuff`

## Problem Statement

You are given the `root` of a binary tree.

Return all root-to-leaf paths in any order.

A leaf is a node with no children.

## Examples

**Example 1:**

```ini
Input:  root = [1,2,3,null,5]
Output: ["1->2->5","1->3"]
```

**Example 2:**

```ini
Input:  root = [1]
Output: ["1"]
```

## Constraints

* The number of nodes in the tree is in the range `[1, 100]`.
* `-100 <= Node.val <= 100`

<br><br>

## Approach

### The Core Idea

Think of yourself as a person walking down the tree from the top.

* In your hand you carry a **breadcrumb trail**, which is just a string of every node you have stepped on so far.
* Every time you step onto a new node, you write that node's value at the end of your trail.
* The moment you reach a node that has **no children below it**, your walk cannot continue, so the trail in your hand is one finished answer. You drop a copy of it into the answer list.
* If the node still has children, you are not done. You hand your trail down to each child and let them continue the walk.

That is the entire solution. Walk down, keep adding to the trail, and save the trail whenever the road ends.

### What Happens At Every Single Node

At each node you visit, only three questions matter, always in this order:

**1. What does my trail look like now?**

* If the trail is still empty (you are standing on the root), the trail simply becomes the root's value.
* Otherwise, you glue `->` and then your own value onto the end of the trail you received.

**2. Am I a leaf?**

* A leaf means both left and right are empty.
* If yes, this is the end of a road. Push the trail into the answer list and stop going deeper.

**3. If I am not a leaf, who do I pass the trail to?**

* If a left child exists, send the trail down the left.
* If a right child exists, send the trail down the right.
* If a child does not exist, simply ignore that side. You never step into empty space.

### The One Detail Everyone Misses

Notice there is **no cleanup step** here. In many path problems you have to remove the last node from your trail before turning around and exploring the other side. Here you do not.

<mark>The reason is that the path is a string, and strings in Python cannot be changed in place. Every child receives its own private copy of the trail, so nothing a child does can ever damage the parent's trail.</mark>

So when the left branch finishes and control comes back up, the parent's trail is still exactly what it was before the left branch started. The right branch then gets that same clean copy. The undo happens for free.

### Why The Answers List Is Different

The `paths` list is passed down too, but it is **not** copied. A list is a single shared object, so every node in the tree writes into the very same list. That is exactly what you want, since all the finished trails from every corner of the tree need to end up collected in one place.

<br><br>

## Code

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def helper(self, node, paths, path):
        path = str(node.val) if not path else path + '->' + str(node.val)

        if not node.left and not node.right:
            paths.append(path)
            return

        if node.left:
            self.helper(node.left, paths, path)
        if node.right:
            self.helper(node.right, paths, path)

    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        paths = []
        if not root:
            paths

        self.helper(root, paths, '')
        return paths
```

<br><br>

## Dry Run

```ini
INPUT: root = [1,2,3,null,5]

TREE SHAPE:

        1
       / \
      2   3
       \
        5

Node 1 -> left = 2, right = 3
Node 2 -> left = None, right = 5
Node 3 -> left = None, right = None   (leaf)
Node 5 -> left = None, right = None   (leaf)

SETUP:
paths = []
First call made -> helper(node = 1, paths = [], path = '')


=====================================================================
STEP 1  ->  helper(node = 1, path = '')
=====================================================================

Build the trail:
    path is '' which is falsy  ->  take the first branch
    path = str(1)
    path = "1"

Leaf check:
    node.left  = 2      (exists)
    node.right = 3      (exists)
    not node.left and not node.right  ->  False
    So node 1 is NOT a leaf. Do not append. Keep going down.

Send trail to children:
    if node.left  ->  node 2 exists  ->  GO LEFT with path = "1"

    STATE RIGHT NOW:
        paths = []
        node 1 is paused, holding its own copy path = "1"


    =================================================================
    STEP 2  ->  helper(node = 2, path = "1")
    =================================================================

    Build the trail:
        path is "1" which is truthy  ->  take the second branch
        path = "1" + "->" + str(2)
        path = "1->2"

    Leaf check:
        node.left  = None
        node.right = 5      (exists)
        not node.left and not node.right  ->  False
        Node 2 is NOT a leaf, because it still has a right child.

    Send trail to children:
        if node.left   ->  None  ->  SKIP the left side entirely
        if node.right  ->  node 5 exists  ->  GO RIGHT with path = "1->2"

        STATE RIGHT NOW:
            paths = []
            node 1 paused with path = "1"
            node 2 paused with path = "1->2"


        =============================================================
        STEP 3  ->  helper(node = 5, path = "1->2")
        =============================================================

        Build the trail:
            path is "1->2" which is truthy
            path = "1->2" + "->" + str(5)
            path = "1->2->5"

        Leaf check:
            node.left  = None
            node.right = None
            not node.left and not node.right  ->  True
            NODE 5 IS A LEAF. The road ends here.

        Save the answer:
            paths.append("1->2->5")
            paths = ["1->2->5"]

        return  ->  climb back up to node 2


    =================================================================
    STEP 4  ->  back inside helper(node = 2)
    =================================================================

    The right call is finished. There is nothing left to run in node 2.
    Its own path variable is still "1->2" and was never damaged.

    Function ends  ->  climb back up to node 1


=====================================================================
STEP 5  ->  back inside helper(node = 1)
=====================================================================

    The left call is finished.

    IMPORTANT: node 1's path is STILL "1".
    Everything that happened on the left branch worked on copies,
    so nothing here changed. This is the automatic backtracking.

    Now run the next line:
    if node.right  ->  node 3 exists  ->  GO RIGHT with path = "1"

    STATE RIGHT NOW:
        paths = ["1->2->5"]
        node 1 paused with path = "1"


    =================================================================
    STEP 6  ->  helper(node = 3, path = "1")
    =================================================================

    Build the trail:
        path is "1" which is truthy
        path = "1" + "->" + str(3)
        path = "1->3"

    Leaf check:
        node.left  = None
        node.right = None
        not node.left and not node.right  ->  True
        NODE 3 IS A LEAF. The road ends here.

    Save the answer:
        paths.append("1->3")
        paths = ["1->2->5", "1->3"]

    return  ->  climb back up to node 1


=====================================================================
STEP 7  ->  back inside helper(node = 1)
=====================================================================

    Both children have been explored.
    Function ends  ->  climb back up to binaryTreePaths


=====================================================================
STEP 8  ->  back inside binaryTreePaths
=====================================================================

    return paths

FINAL OUTPUT:
    ["1->2->5", "1->3"]
```

<br><br>

## Dry Run (Example 2)

```ini
INPUT: root = [1]

TREE SHAPE:

        1

Node 1 -> left = None, right = None   (leaf)

SETUP:
paths = []
First call made -> helper(node = 1, paths = [], path = '')


=====================================================================
STEP 1  ->  helper(node = 1, path = '')
=====================================================================

Build the trail:
    path is '' which is falsy
    path = str(1)
    path = "1"

Leaf check:
    node.left  = None
    node.right = None
    not node.left and not node.right  ->  True
    NODE 1 IS A LEAF, even though it is also the root.

Save the answer:
    paths.append("1")
    paths = ["1"]

return  ->  climb back up


=====================================================================
STEP 2  ->  back inside binaryTreePaths
=====================================================================

    return paths

FINAL OUTPUT:
    ["1"]
```

<br><br>

## Complexity Analysis

**Time Complexity**

* Every node is visited exactly once, which is `O(N)` visits.
* At each node you build a new string by copying the old one, and that copy costs as much as the current path length, which is at most the height `H`.
* So the total is `O(N * H)`.
* For a balanced tree the height is `log N`, giving roughly `O(N log N)`.
* For a completely one sided (skewed) tree the height is `N`, giving `O(N^2)` in the worst case.

**Space Complexity**

* The recursion stack goes as deep as the height of the tree, so `O(H)`.
* The answer list itself holds every root to leaf path, which needs `O(N * H)` in total.

<br><br>

## Key Takeaways

* Carry the path down as an argument instead of trying to rebuild it later. Going down is easy, going back up is not.
* A node is a leaf only when **both** sides are empty. Checking just one side is the most common bug in this problem.
* Because Python strings are immutable, each recursive call gets a fresh copy of the path, so no manual undo step is needed.
* The `paths` list is shared by reference on purpose, so every branch adds into the same collection.
* The `if not root: paths` line in the original code does nothing useful, but the constraints guarantee at least one node, so the solution is still correct.

<br><br>

## Related Problems

* [Path Sum (112)](https://leetcode.com/problems/path-sum/)
* [Path Sum II (113)](https://leetcode.com/problems/path-sum-ii/)
* [Minimum Depth of Binary Tree (111)](https://leetcode.com/problems/minimum-depth-of-binary-tree/)
* [Sum Root to Leaf Numbers (129)](https://leetcode.com/problems/sum-root-to-leaf-numbers/)
* [Path Sum III (437)](https://leetcode.com/problems/path-sum-iii/)
* [Binary Tree Maximum Path Sum (124)](https://leetcode.com/problems/binary-tree-maximum-path-sum/)
* [Smallest String Starting From Leaf (988)](https://leetcode.com/problems/smallest-string-starting-from-leaf/)
* [Insufficient Nodes in Root to Leaf Paths (1080)](https://leetcode.com/problems/insufficient-nodes-in-root-to-leaf-paths/)
* [Binary Tree Longest Consecutive Sequence (298)](https://leetcode.com/problems/binary-tree-longest-consecutive-sequence/)