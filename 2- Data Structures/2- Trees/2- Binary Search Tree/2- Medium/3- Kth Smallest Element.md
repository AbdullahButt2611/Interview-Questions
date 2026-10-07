# Kth Smallest Element in a BST

`Amazon` • `Google` • `Meta` • `Uber`

## Problem Statement

Given the `root` of a binary search tree, and an integer `k`, return the `kth` smallest value (**1-indexed**) of all the values of the nodes in the tree.

## Examples

**Example 1:**

```ini
Input: root = [3,1,4,null,2], k = 1
Output: 1
Explanation: Sorted values are [1, 2, 3, 4]. The 1st smallest is 1.
```

**Example 2:**

```ini
Input: root = [5,3,6,2,4,null,null,1], k = 3
Output: 3
Explanation: Sorted values are [1, 2, 3, 4, 5, 6]. The 3rd smallest is 3.
```

## Constraints

- The number of nodes in the tree is `n`.
- `1 <= k <= n <= 10^4`
- `0 <= Node.val <= 10^4`

<br><br>

## Approach

### The One Rule to Remember

In a BST, <mark>reading the tree as "left, node, right" gives the values in sorted order</mark>.

- This reading order is called **inorder traversal**.
- So the kth smallest value is simply the **kth node we visit** in inorder.
- We do not need to visit the whole tree. We stop the moment we reach the kth node.

### The Idea in Plain Words

Think of the stack as a **"to-do list" of nodes we have seen but not counted yet**.

- The **smallest** value in any tree is found by going **left, left, left** until you cannot go further.
- On the way down, we drop every node onto the stack, because we will come back to them later.
- Whatever is on **top of the stack** is always the **next smallest** value not yet counted.

### Step by Step

1. **Go left as far as you can.**
   - Push every node you pass onto the stack.
   - Stop when you hit `None`.
2. **Take the top node off the stack.**
   - This is the next smallest value.
3. **Count it.**
   - Reduce `k` by 1.
   - If `k` becomes `0`, this node is the answer. Return its value.
4. **Step right.**
   - Move to the right child of the node you just counted.
   - Its right subtree holds the values that come **right after** it.
   - Go back to Step 1 and repeat.

> Why does the loop never get stuck? Because `k <= n`, we are guaranteed to reach the kth node before the tree runs out.

> Memory hook: <mark>"Dive left, pop one, count it, step right. Repeat."</mark>

<br><br>

## Solution

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def kthSmallest(self, root: TreeNode | None, k: int) -> int:
        stack = []
        node = root
        while True:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            k -= 1
            if k == 0:
                return node.val
            node = node.right
```

<br><br>

## Dry Run

```ini
=====================================================
SCENARIO A: root = [3,1,4,null,2], k = 1
=====================================================

Starting Tree:

        3
       / \
      1   4
       \
        2

Setup:
  stack = []
  node  = 3
  k     = 1

Iteration 1:
  Step 1: Dive left as far as possible.
    node = 3 exists → push 3. stack = [3]. Move left: node = 3.left = 1
    node = 1 exists → push 1. stack = [3, 1]. Move left: node = 1.left = None
    node = None → stop diving.

  Step 2: Pop the top.
    node  = 1
    stack = [3]

  Step 3: Count it.
    k = 1 - 1 = 0

  Step 4: Is k == 0? YES.
    Return node.val = 1

Output: 1  ✓


=====================================================
SCENARIO B: root = [5,3,6,2,4,null,null,1], k = 3
=====================================================

Starting Tree:

            5
           / \
          3   6
         / \
        2   4
       /
      1

Setup:
  stack = []
  node  = 5
  k     = 3

Iteration 1:
  Step 1: Dive left as far as possible.
    node = 5 exists → push 5. stack = [5].          Move left: node = 3
    node = 3 exists → push 3. stack = [5, 3].       Move left: node = 2
    node = 2 exists → push 2. stack = [5, 3, 2].    Move left: node = 1
    node = 1 exists → push 1. stack = [5, 3, 2, 1]. Move left: node = None
    node = None → stop diving.

  Step 2: Pop the top.
    node  = 1
    stack = [5, 3, 2]

  Step 3: Count it.
    k = 3 - 1 = 2      (1 is the 1st smallest)

  Step 4: Is k == 0? NO.
    Step right: node = 1.right = None

Iteration 2:
  Step 1: Dive left as far as possible.
    node = None → nothing to push. stack = [5, 3, 2]

  Step 2: Pop the top.
    node  = 2
    stack = [5, 3]

  Step 3: Count it.
    k = 2 - 1 = 1      (2 is the 2nd smallest)

  Step 4: Is k == 0? NO.
    Step right: node = 2.right = None

Iteration 3:
  Step 1: Dive left as far as possible.
    node = None → nothing to push. stack = [5, 3]

  Step 2: Pop the top.
    node  = 3
    stack = [5]

  Step 3: Count it.
    k = 1 - 1 = 0      (3 is the 3rd smallest)

  Step 4: Is k == 0? YES.
    Return node.val = 3

Visited order: 1 → 2 → 3  (stopped early, nodes 4, 5, 6 never counted)
Output: 3  ✓


=====================================================
SCENARIO C: root = [3,1,4,null,2], k = 4  (answer is the largest node)
=====================================================

Starting Tree:

        3
       / \
      1   4
       \
        2

Setup:
  stack = []
  node  = 3
  k     = 4

Iteration 1:
  Step 1: Dive left as far as possible.
    node = 3 exists → push 3. stack = [3].    Move left: node = 1
    node = 1 exists → push 1. stack = [3, 1]. Move left: node = None
    node = None → stop diving.

  Step 2: Pop the top.
    node  = 1
    stack = [3]

  Step 3: Count it.
    k = 4 - 1 = 3      (1 is the 1st smallest)

  Step 4: Is k == 0? NO.
    Step right: node = 1.right = 2

Iteration 2:
  Step 1: Dive left as far as possible.
    node = 2 exists → push 2. stack = [3, 2]. Move left: node = 2.left = None
    node = None → stop diving.

  Step 2: Pop the top.
    node  = 2
    stack = [3]

  Step 3: Count it.
    k = 3 - 1 = 2      (2 is the 2nd smallest)

  Step 4: Is k == 0? NO.
    Step right: node = 2.right = None

Iteration 3:
  Step 1: Dive left as far as possible.
    node = None → nothing to push. stack = [3]

  Step 2: Pop the top.
    node  = 3
    stack = []

  Step 3: Count it.
    k = 2 - 1 = 1      (3 is the 3rd smallest)

  Step 4: Is k == 0? NO.
    Step right: node = 3.right = 4

Iteration 4:
  Step 1: Dive left as far as possible.
    node = 4 exists → push 4. stack = [4]. Move left: node = 4.left = None
    node = None → stop diving.

  Step 2: Pop the top.
    node  = 4
    stack = []

  Step 3: Count it.
    k = 1 - 1 = 0      (4 is the 4th smallest)

  Step 4: Is k == 0? YES.
    Return node.val = 4

Visited order: 1 → 2 → 3 → 4  (sorted, exactly as the One Rule promised)
Output: 4  ✓
```

<br><br>

## Complexity Analysis

- **Time Complexity:** `O(H + k)`, where `H` is the height of the tree.
  - Diving down to the smallest node takes `O(H)`.
  - After that, we count only `k` nodes and then stop.
  - In the worst case (skewed tree, or `k = n`), this becomes `O(N)`.
- **Space Complexity:** `O(H)`.
  - The stack holds at most one path from the root down, so its size is at most the height.
  - In a balanced tree this is `O(log N)`, and in a skewed tree it is `O(N)`.

<br><br>

## Related Problems

- [Binary Tree Inorder Traversal (94)](https://leetcode.com/problems/binary-tree-inorder-traversal/)
- [Validate Binary Search Tree (98)](https://leetcode.com/problems/validate-binary-search-tree/)
- [Binary Search Tree Iterator (173)](https://leetcode.com/problems/binary-search-tree-iterator/)
- [Kth Largest Element in an Array (215)](https://leetcode.com/problems/kth-largest-element-in-an-array/)
- [Delete Node in a BST (450)](https://leetcode.com/problems/delete-node-in-a-bst/)
- [Find Mode in Binary Search Tree (501)](https://leetcode.com/problems/find-mode-in-binary-search-tree/)
- [Minimum Absolute Difference in BST (530)](https://leetcode.com/problems/minimum-absolute-difference-in-bst/)
- [Second Minimum Node In a Binary Tree (671)](https://leetcode.com/problems/second-minimum-node-in-a-binary-tree/)
- [Kth Largest Element in a Stream (703)](https://leetcode.com/problems/kth-largest-element-in-a-stream/)