# Symmetric Tree

`Google` • `Apple` • `LinkedIn` • `Microsoft` • `Meta` • `Adobe` • `Bloomberg` • `Yahoo` • `Yandex`

## Problem Statement

Given the root of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).

## Examples

**Example 1:**

```ini
Input: root = [1,2,2,3,4,4,3]
Output: true
```

**Example 2:**

```ini
Input: root = [1,2,2,null,3,null,3]
Output: false
```

## Constraints

* The number of nodes in the tree is in the range `[1, 1000]`.
* `-100 <= Node.val <= 100`

<br><br>

## Approach

**The picture in your head**

* Imagine the tree is printed on paper and you fold the paper along the vertical line passing through the root.
* If every node on the left half lands exactly on a node with the same value on the right half, the tree is symmetric.
* So the real question is not "is this tree special", it is simply: **is the left half a mirror of the right half?**

<br>

**What "mirror" actually means**

* Mirror is not the same as "equal". Two halves that are equal would be copies, not reflections.
* In a mirror, the outermost node on the left pairs with the outermost node on the right, and the innermost node on the left pairs with the innermost node on the right.
* That is why the comparison happens in a **crossed** way instead of a straight way.

<mark>left.left is compared with right.right, and left.right is compared with right.left</mark>

<br>

**The raw steps we follow**

We always work with a **pair of nodes**, one taken from the left half and one taken from the right half. The very first pair is `root.left` and `root.right`.

For any pair we are holding right now:

* If **both nodes are empty**, nothing is there on either side, so this pair is fine. Answer `True`.
* If **only one of them is empty**, one side has a node and the other side has a hole. A mirror can never look like that. Answer `False`.
* If **both exist but their values are different**, the reflection is broken at this exact spot. Answer `False`.
* If **both exist and their values match**, this pair is good, but we are not done. We now go one level deeper and form two new pairs in the crossed manner:
  * the outer pair: `left.left` with `right.right`
  * the inner pair: `left.right` with `right.left`
* **Both of these new pairs must come back `True`**. If even one of them is `False`, the whole tree is `False`.

<br>

**Why this keeps shrinking until it ends**

* Every time a pair passes the value check, we throw it away and replace it with two smaller pairs that sit one level lower.
* Since the tree has a limited height, we eventually reach pairs where both nodes are empty, and those return `True` immediately.
* Those `True` values travel back upward, get combined with `and`, and finally give the answer at the top.

<br>

**One small but useful detail**

* The checks are combined using `and`, so the moment any pair fails, the remaining work is skipped and `False` travels straight back to the top.
* We never need to compare a node from the left half with another node from the left half. Every comparison is always one node from each half.

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
    def symmetricHelper(self, left, right):
        if not left and not right:
            return True

        if not left or not right:
            return False

        return (left.val == right.val) and self.symmetricHelper(left.left, right.right) and self.symmetricHelper(left.right, right.left)

    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True

        return self.symmetricHelper(root.left, root.right)
```

<br><br>

## Dry Run

```ini
=========================================================
EXAMPLE 1  ->  root = [1,2,2,3,4,4,3]      Expected: true
=========================================================

Tree Structure:

                 1  (A)
               /      \
          (B) 2        2  (C)
             / \      / \
        (D) 3   4    4   3
               (E)  (F) (G)

Names used below:
  A = root, value 1
  B = A.left,  value 2       C = A.right, value 2
  D = B.left,  value 3       E = B.right, value 4
  F = C.left,  value 4       G = C.right, value 3
  All of D, E, F, G have no children (their left and right are None)

---------------------------------------------------------
Start: isSymmetric(A)
  root is A, which is not None, so we do not return early
  We call symmetricHelper(A.left, A.right) = symmetricHelper(B, C)

Iteration 1: symmetricHelper(left = B(2), right = C(2))
  Check "both empty?"     -> B exists and C exists    -> No
  Check "only one empty?" -> both exist               -> No
  Compare values          -> 2 == 2                   -> Match
  Values matched, so two deeper pairs must be checked:
      Check A (outer pair): symmetricHelper(B.left,  C.right) = symmetricHelper(D(3), G(3))
      Check B (inner pair): symmetricHelper(B.right, C.left)  = symmetricHelper(E(4), F(4))
  Python evaluates Check A first, so we go there now
  Iteration 1 is PAUSED, waiting for its answers

Iteration 2: symmetricHelper(left = D(3), right = G(3))
  Check "both empty?"     -> both exist               -> No
  Check "only one empty?" -> both exist               -> No
  Compare values          -> 3 == 3                   -> Match
  Go one level deeper with the crossed pairs:
      Check A: symmetricHelper(D.left,  G.right) = symmetricHelper(None, None)
      Check B: symmetricHelper(D.right, G.left)  = symmetricHelper(None, None)
  Iteration 2 is PAUSED

Iteration 3: symmetricHelper(left = None, right = None)
  Check "both empty?"     -> Yes
  RETURN True   (this is the first Check A of Iteration 2)

Iteration 4: symmetricHelper(left = None, right = None)
  Check "both empty?"     -> Yes
  RETURN True   (this is the Check B of Iteration 2)

Back inside Iteration 2:
  Values matched (True) and Check A (True) and Check B (True)
  RETURN True   -> so the pair D(3) with G(3) is a valid mirror
  This True goes back to Iteration 1 as its Check A answer

Back inside Iteration 1:
  Check A came back True, so we now run Check B
  We call symmetricHelper(E(4), F(4))

Iteration 5: symmetricHelper(left = E(4), right = F(4))
  Check "both empty?"     -> both exist               -> No
  Check "only one empty?" -> both exist               -> No
  Compare values          -> 4 == 4                   -> Match
  Go one level deeper with the crossed pairs:
      Check A: symmetricHelper(E.left,  F.right) = symmetricHelper(None, None)
      Check B: symmetricHelper(E.right, F.left)  = symmetricHelper(None, None)
  Iteration 5 is PAUSED

Iteration 6: symmetricHelper(left = None, right = None)
  Check "both empty?"     -> Yes
  RETURN True

Iteration 7: symmetricHelper(left = None, right = None)
  Check "both empty?"     -> Yes
  RETURN True

Back inside Iteration 5:
  True and True and True
  RETURN True   -> so the pair E(4) with F(4) is a valid mirror
  This True goes back to Iteration 1 as its Check B answer

Back inside Iteration 1:
  values matched (True) and Check A (True) and Check B (True)
  RETURN True

Final Output: true


=========================================================
EXAMPLE 2  ->  root = [1,2,2,null,3,null,3]  Expected: false
=========================================================

Tree Structure:

                 1  (A)
               /      \
          (B) 2        2  (C)
               \         \
                3 (D)     3 (E)

Names used below:
  A = root, value 1
  B = A.left,  value 2       C = A.right, value 2
  B.left  = None             C.left  = None
  D = B.right, value 3       E = C.right, value 3

---------------------------------------------------------
Start: isSymmetric(A)
  A is not None, so we call symmetricHelper(B, C)

Iteration 1: symmetricHelper(left = B(2), right = C(2))
  Check "both empty?"     -> both exist               -> No
  Check "only one empty?" -> both exist               -> No
  Compare values          -> 2 == 2                   -> Match
  Two deeper pairs are formed:
      Check A (outer pair): symmetricHelper(B.left,  C.right) = symmetricHelper(None, E(3))
      Check B (inner pair): symmetricHelper(B.right, C.left)  = symmetricHelper(D(3), None)
  Check A runs first
  Iteration 1 is PAUSED

Iteration 2: symmetricHelper(left = None, right = E(3))
  Check "both empty?"     -> left is None but right exists   -> No
  Check "only one empty?" -> Yes, exactly one side is missing
  The left half has a hole where the right half has a node,
  so the reflection is already broken here
  RETURN False

Back inside Iteration 1:
  Check A came back False
  Because the checks are joined with "and", Check B is never even run
  RETURN False

Final Output: false
```

<br><br>

## Complexity Analysis

**Time Complexity: O(n)**

* In the worst case every node of the tree takes part in exactly one pair comparison.
* So the work grows in a straight line with the number of nodes `n`.

<br>

**Space Complexity: O(h)**

* No extra list or dictionary is created, but each paused call sits on the recursion stack until its deeper calls finish.
* At any moment the number of paused calls is at most the height `h` of the tree.
* For a balanced tree this is `O(log n)`, and for a completely skewed tree it becomes `O(n)`.

<br><br>

## Related Problems

* [Same Tree (100)](https://leetcode.com/problems/same-tree/)
* [Maximum Depth of Binary Tree (104)](https://leetcode.com/problems/maximum-depth-of-binary-tree/)
* [Balanced Binary Tree (110)](https://leetcode.com/problems/balanced-binary-tree/)
* [Invert Binary Tree (226)](https://leetcode.com/problems/invert-binary-tree/)
* [Subtree of Another Tree (572)](https://leetcode.com/problems/subtree-of-another-tree/)
* [Leaf-Similar Trees (872)](https://leetcode.com/problems/leaf-similar-trees/)
* [Binary Tree Level Order Traversal (102)](https://leetcode.com/problems/binary-tree-level-order-traversal/)