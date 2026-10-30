# Print Root to Node Path in a Binary Tree

`Amazon` • `Microsoft` • `Facebook` • `Bloomberg`

## Problem Statement

You are given a Binary Tree and a reference to its root, along with the value of a target node.

Your task is to return the path from the root node down to that target node, in order.

- The path must start at the root and end at the target node.
- Every node on the way down is part of the path.
- If the target node does not exist in the tree, return an empty path.

<mark>Note: No two nodes in the tree have the same data value, so the target node is always unique.</mark>

## Examples

```ini
Input:
Binary Tree (level order) : 1 2 3 4 5 -1 -1 -1 -1 7 -1
Target Node               : 7

Tree looks like this:

              1
            /   \
           2     3
         /   \
        4     5
             /
            7

Output: [1, 2, 5, 7]

Reason:
Start at 1, move left to 2, move right to 5, move left to 7.
So the road travelled is 1 -> 2 -> 5 -> 7.
```

```ini
Input:
Binary Tree (level order) : 1 2 3 4 5 6 7
Target Node               : 4

Tree looks like this:

              1
            /   \
           2     3
         /  \   /  \
        4    5 6    7

Output: [1, 2, 4]
```

```ini
Input:
Binary Tree (level order) : 1 2 3
Target Node               : 9

Output: []

Reason:
9 is not present anywhere in the tree, so there is no path.
```

## Constraints

- `1 <= Number of nodes <= 10^5`
- `1 <= Node value <= 10^5`
- All node values are distinct.

<br><br>

## Approach

Think of the tree as a set of roads and think of yourself as someone walking down them with a notebook in hand.

Every time you step onto a node, you write its value in the notebook. If you later realise that road was a dead end, you erase the last thing you wrote and try a different road. When you finally reach the target node, whatever is left in the notebook is exactly the path you walked.

That erasing step is called <mark>backtracking</mark>, and it is the heart of this problem.

**The rules you follow at every node**

- **You stepped onto nothing (an empty spot).** There is no node here, so nothing can be found. Report `false` to whoever sent you here.

- **You stepped onto a real node.** Write its value into the notebook right away, because for now you are assuming this node might be on the correct road.

- **Check if this is the target.** If the value matches the target, you are done. Report `true` immediately. Do not erase anything, since the notebook now holds the full answer.

- **Not the target, so try the left road.** Send the same instructions down to the left child. If the left side reports `true`, that means the target was found somewhere below on the left. You are part of that road, so you also report `true` without erasing anything.

- **Left road failed, so try the right road.** Same idea. If the right side reports `true`, you report `true` too.

- **Both roads failed.** This node is not on the correct road at all. Erase its value from the notebook (remove the last entry) and report `false` to your parent.

**Why the erasing is so important**

The notebook is shared by the whole journey. If you never erased failed nodes, the notebook would end up holding every node you ever visited instead of just the correct road.

By erasing on the way back up, the notebook always holds only the nodes on the road you are standing on right now.

**Why nothing gets erased after success**

The moment the target is found, `true` travels back up the tree. Every parent sees `true` and returns `true` straight away, so no parent ever reaches its own erase step.

The notebook freezes exactly at the correct answer.

<br><br>

## Code

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class Solution:

    def helper(self, node, target, path):
        # Stepped onto an empty spot, nothing to find here
        if node is None:
            return False

        # Assume this node is on the correct road, so record it
        path.append(node.data)

        # Found the target, stop everything
        if node.data == target:
            return True

        # Try the left road, then the right road
        if self.helper(node.left, target, path):
            return True
        if self.helper(node.right, target, path):
            return True

        # Both roads failed, so this node is not on the path
        path.pop()
        return False

    def rootToNodePath(self, root, target):
        path = []
        if root is None:
            return path

        self.helper(root, target, path)
        return path
```

<br><br>

## Dry Run

```ini
Tree:
              1
            /   \
           2     3
         /   \
        4     5
             /
            7

Target = 7
path   = []   (our notebook, empty at the start)


Iteration 1  ->  helper(node = 1)
   node is not None, so continue
   write 1 into the notebook
   path = [1]
   is 1 equal to 7 ?  No
   go left, call helper(node = 2)


Iteration 2  ->  helper(node = 2)
   node is not None, so continue
   write 2 into the notebook
   path = [1, 2]
   is 2 equal to 7 ?  No
   go left, call helper(node = 4)


Iteration 3  ->  helper(node = 4)
   node is not None, so continue
   write 4 into the notebook
   path = [1, 2, 4]
   is 4 equal to 7 ?  No
   go left, call helper(node = None)


Iteration 4  ->  helper(node = None)     [left child of 4]
   node is None
   return False


Iteration 5  ->  back inside helper(node = 4)
   left road returned False
   go right, call helper(node = None)


Iteration 6  ->  helper(node = None)     [right child of 4]
   node is None
   return False


Iteration 7  ->  back inside helper(node = 4)
   both roads returned False
   4 is a dead end, so erase it
   path = [1, 2]
   return False


Iteration 8  ->  back inside helper(node = 2)
   left road returned False
   go right, call helper(node = 5)


Iteration 9  ->  helper(node = 5)
   node is not None, so continue
   write 5 into the notebook
   path = [1, 2, 5]
   is 5 equal to 7 ?  No
   go left, call helper(node = 7)


Iteration 10 ->  helper(node = 7)
   node is not None, so continue
   write 7 into the notebook
   path = [1, 2, 5, 7]
   is 7 equal to 7 ?  YES
   return True immediately
   (nothing gets erased from here on)


Iteration 11 ->  back inside helper(node = 5)
   left road returned True
   return True without erasing
   path stays [1, 2, 5, 7]


Iteration 12 ->  back inside helper(node = 2)
   right road returned True
   return True without erasing
   path stays [1, 2, 5, 7]


Iteration 13 ->  back inside helper(node = 1)
   left road returned True
   return True without erasing
   path stays [1, 2, 5, 7]


Recursion is over.

Final Answer -> [1, 2, 5, 7]
```

<br><br>

## Complexity Analysis

**Time Complexity: O(N)**

- In the worst case (target sitting at the very last node visited, or not present at all), every node is stepped on exactly once.
- Writing a value and erasing a value both take constant time.

**Space Complexity: O(H)**

- `H` is the height of the tree.
- The recursion stack holds one frame per node on the current road, and the notebook holds at most that many values too.
- For a balanced tree this is `O(log N)`, and for a skewed tree (one long chain) it becomes `O(N)`.

<br><br>

## Related Problems

- [Binary Tree Paths (257)](https://leetcode.com/problems/binary-tree-paths/)
- [Path Sum (112)](https://leetcode.com/problems/path-sum/)
- [Path Sum II (113)](https://leetcode.com/problems/path-sum-ii/)
- [Sum Root to Leaf Numbers (129)](https://leetcode.com/problems/sum-root-to-leaf-numbers/)
- [Lowest Common Ancestor of a Binary Tree (236)](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/)
- [All Nodes Distance K in Binary Tree (863)](https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/)
- [Binary Tree Maximum Path Sum (124)](https://leetcode.com/problems/binary-tree-maximum-path-sum/)
- [Smallest String Starting From Leaf (988)](https://leetcode.com/problems/smallest-string-starting-from-leaf/)