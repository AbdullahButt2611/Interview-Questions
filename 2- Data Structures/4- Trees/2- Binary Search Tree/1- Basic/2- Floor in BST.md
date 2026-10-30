# Floor in a Binary Search Tree

`Oracle` • `Google`

## Problem Statement

Given the root of a binary search tree and a number `k`, find the greatest number in the tree that is less than or equal to `k`.

In simple words, we want the closest value that sits at or just below `k`.

**Note:** If no such value exists (every value in the tree is bigger than `k`), then return `-1`.

## Examples

**Example 1**

```ini
Input: root = [10, 7, 15, 2, 8, 11, 16], k = 14
Output: 11
```

The greatest element in the tree that is less than or equal to 14 is 11.

**Example 2**

```ini
Input: root = [5, 2, 12, 1, 3, 9, 21, N, N, N, N, N, N, 19, 25], k = 24
Output: 21
```

The greatest element in the tree that is less than or equal to 24 is 21.

**Example 3**

```ini
Input: root = [5, 2, 12, 1, 3, 9, 21, N, N, N, N, N, N, 19, 25], k = 4
Output: 3
```

The greatest element in the tree that is less than or equal to 4 is 3.

## Constraints

- `1 ≤ size of binary tree ≤ 10^5`
- `1 ≤ node.data ≤ 10^5`
- `1 ≤ k ≤ 10^5`
- All node values in the tree are unique.

<br><br>

## Approach

The key thing to remember about a Binary Search Tree is one simple rule:

- Everything on the **left** of a node is **smaller** than it.
- Everything on the **right** of a node is **larger** than it.

We use this rule to avoid checking every node. Instead, we walk down the tree in a smart way.

At every node we stand on, we ask ourselves one question: *"Is this value allowed to be the answer?"*

A value is allowed if it is less than or equal to `k`. So we compare the current node's value with `k`:

- **If the current value is less than or equal to `k`:**
  This value is a valid candidate for our answer. We save it as our best answer so far. But maybe there is an even bigger valid value hiding on the right side (right side has larger numbers), so we move **right** to try our luck.

- **If the current value is greater than `k`:**
  This value is too big, it can never be our answer. Everything on its right is even bigger, so that whole side is useless too. We move **left** to look at smaller values.

We keep doing this until we fall off the tree (reach an empty spot). Whatever we last saved is our floor.

If we never saved anything (meaning every value was bigger than `k`), the answer stays `-1`.

<mark>The beauty here is that we only ever go one direction at each step, so we touch just one path from top to bottom, never the whole tree.</mark>

## Code

```python
class Solution:
    def floor(self, root, k):
        ans = -1                    # best valid value found so far

        while root:
            if root.data <= k:
                ans = root.data     # current value is valid, save it
                root = root.right   # try to find a bigger valid value
            else:
                root = root.left    # current value too big, go smaller

        return ans
```

<br><br>

## Dry Run

Let us walk through **Example 1** step by step.

```ini
Tree:
              10
            /    \
           7      15
          / \    /  \
         2   8  11   16

k = 14
Goal: find the greatest value that is <= 14

Start: ans = -1, current node = 10

Iteration 1:
  current = 10
  Is 10 <= 14 ?  YES
  10 is valid, so save it -> ans = 10
  Move right to look for something bigger -> current = 15

Iteration 2:
  current = 15
  Is 15 <= 14 ?  NO (15 is too big)
  Cannot use 15, move left to smaller values -> current = 11

Iteration 3:
  current = 11
  Is 11 <= 14 ?  YES
  11 is valid and bigger than our saved 10, so save it -> ans = 11
  Move right to look for something bigger -> current = None (16 is not reachable from here, 11 has no right child)

Loop ends because current is None.

Final Answer: ans = 11
```

Notice how we never visited nodes 7, 2, 8, or 16. We only walked one clean path down the tree, which is exactly why this is fast.

<br><br>

## Complexity

- **Time Complexity:** `O(H)` where `H` is the height of the tree. We only travel down one path. For a balanced tree this is about `O(log N)`, and in the worst case (a skewed tree) it becomes `O(N)`.
- **Space Complexity:** `O(1)` because we use only a couple of variables and no extra data structures.

<br><br>

## Related Problems

- [Search in a Binary Search Tree (700)](https://leetcode.com/problems/search-in-a-binary-search-tree/)
- [Closest Binary Search Tree Value (270)](https://leetcode.com/problems/closest-binary-search-tree-value/)
- [Kth Smallest Element in a BST (230)](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)
- [Insert into a Binary Search Tree (701)](https://leetcode.com/problems/insert-into-a-binary-search-tree/)
- [Validate Binary Search Tree (98)](https://leetcode.com/problems/validate-binary-search-tree/)