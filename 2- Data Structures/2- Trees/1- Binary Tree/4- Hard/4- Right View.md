# Binary Tree Right Side View

`Amazon` • `Meta` • `Google` • `Apple` • `Microsoft` • `Bloomberg` • `ByteDance` • `Alibaba` • `Tencent` • `Educative`

## Problem Statement

Given the `root` of a binary tree, imagine yourself standing on the **right side** of it. Return the values of the nodes you can see, ordered from **top to bottom**.

In simple words, from every level of the tree, only the **rightmost node** is visible to you. Everything sitting behind it is blocked from your view.

## Examples

**Example 1**

```ini
Input:  root = [1,2,3,null,5,null,4]
Output: [1,3,4]

Tree:
        1        <--- you see 1
      /   \
     2     3     <--- you see 3
      \     \
       5     4   <--- you see 4
```

**Example 2**

```ini
Input:  root = [1,2,3,4,null,null,null,5]
Output: [1,3,4,5]

Tree:
        1        <--- you see 1
      /   \
     2     3     <--- you see 3
    /
   4             <--- you see 4 (only node on this level)
  /
 5               <--- you see 5 (only node on this level)
```

**Example 3**

```ini
Input:  root = [1,null,3]
Output: [1,3]
```

**Example 4**

```ini
Input:  root = []
Output: []
```

## Constraints

* The number of nodes in the tree is in the range `[0, 100]`.
* `-100 <= Node.val <= 100`

<br><br>

## Approach 1: Recursive (DFS, Right Side First)

### The Core Idea

The trick here is one single sentence:

<mark>The first node we ever touch at a new depth is the answer for that depth, as long as we always walk right before left.</mark>

Why does that work? Because if we always prefer the right child over the left child, then when we go deep into the tree, the very first node we land on at depth `d` is the rightmost node at depth `d`. Everything we visit later at that same depth is sitting to its left, which means it is hidden behind it.

<br>

### How Do We Know a Depth Is "New"?

We keep one answer list. That list is filled top to bottom, so:

* `answer` has `0` items, means depth `0` has not been filled yet
* `answer` has `1` item, means depth `1` has not been filled yet
* `answer` has `k` items, means depth `k` has not been filled yet

So the check becomes beautifully simple:

```ini
if depth == len(answer):
    this depth is being seen for the very first time
    -> record this node, it is the rightmost one
else:
    this depth already has its winner
    -> skip this node, it is hidden
```

The length of the list doubles as a counter of how many levels are already done. No extra dictionary, no extra bookkeeping.

<br>

### Step by Step Walk

* Start at the root with `depth = 0` and an empty `answer` list
* If the current node is empty, simply stop and go back
* Compare `depth` with `len(answer)`. If they match, add this node's value to `answer`
* Move to the **right child** with `depth + 1`
* Then move to the **left child** with `depth + 1`
* When everything finishes, `answer` holds the right view from top to bottom

The order of those last two moves is the whole solution. Flip them and you get the left view instead.

<br>

### Code

```python
class Solution:
    def rightViewCalculator(self, node, depth, rightView):
        if node is None:
            return

        if depth == len(rightView):
            rightView.append(node.val)

        self.rightViewCalculator(node.right, depth + 1, rightView)
        self.rightViewCalculator(node.left, depth + 1, rightView)

    def rightSideView(self, root):
        if not root:
            return []

        rightView = []
        self.rightViewCalculator(root, 0, rightView)
        return rightView
```

<br>

### Dry Run

```ini
Input tree: root = [1,2,3,null,5,null,4]

        1
      /   \
     2     3
      \     \
       5     4

Start: rightView = [], call on node 1 with depth = 0

Step 1  -> node = 1, depth = 0
          depth (0) == len(rightView) (0)  -> TRUE
          record 1
          rightView = [1]
          now go RIGHT first -> node 3

Step 2  -> node = 3, depth = 1
          depth (1) == len(rightView) (1)  -> TRUE
          record 3
          rightView = [1, 3]
          now go RIGHT first -> node 4

Step 3  -> node = 4, depth = 2
          depth (2) == len(rightView) (2)  -> TRUE
          record 4
          rightView = [1, 3, 4]
          now go RIGHT -> node 4 has no right child

Step 4  -> node = None, depth = 3
          node is empty -> return immediately
          back at node 4, now go LEFT -> node 4 has no left child

Step 5  -> node = None, depth = 3
          node is empty -> return immediately
          node 4 is fully done, go back up to node 3

Step 6  -> back at node 3, right side finished, now go LEFT
          node 3 has no left child -> node = None, depth = 2
          node is empty -> return immediately
          node 3 is fully done, go back up to node 1

Step 7  -> back at node 1, right side finished, now go LEFT -> node 2
          node = 2, depth = 1
          depth (1) == len(rightView) (3)  -> FALSE
          skip 2, it is hidden behind 3
          rightView stays [1, 3, 4]
          now go RIGHT first -> node 5

Step 8  -> node = 5, depth = 2
          depth (2) == len(rightView) (3)  -> FALSE
          skip 5, it is hidden behind 4
          rightView = [1, 3, 4]
          go RIGHT -> None -> return
          go LEFT  -> None -> return
          node 5 is fully done, go back up to node 2

Step 9  -> back at node 2, now go LEFT
          node 2 has no left child -> node = None, depth = 2
          node is empty -> return immediately
          node 2 is fully done, go back up to node 1

Step 10 -> node 1 is fully done, recursion ends

Final Answer: rightView = [1, 3, 4]
```

<br>

### Complexity

* **Time:** `O(n)`, every node is visited exactly once
* **Space:** `O(h)` for the recursion stack, where `h` is the height of the tree. In the worst case (a tree shaped like a straight line) this becomes `O(n)`

<br><br>

## Approach 2: Iterative (BFS, Level by Level)

### The Core Idea

This one matches the picture in your head much more directly.

<mark>Process the tree one full level at a time, and from each level pick the last node.</mark>

If we can grab a whole level at once, then picking the rightmost node is trivial. It is simply the last one in that level.

<br>

### The One Thing That Makes This Work

A normal queue mixes nodes of different levels together, so we would never know where one level ends and the next begins. The fix is a single line:

```ini
level_size = len(queue)
```

At the moment we start a level, the queue holds **exactly** the nodes of that level and nothing else. So we freeze that count first, then pop exactly that many nodes. Everything we push during that loop belongs to the next level, and it patiently waits behind.

Since we push left child first and right child second, the nodes of every level stay in left to right order. So the last node popped in a level is the rightmost one.

<br>

### Step by Step Walk

* If the tree is empty, return an empty list
* Put the root inside a queue
* While the queue is not empty:
  * Note down `level_size`, the current number of nodes in the queue. This is the size of the current level
  * Pop exactly `level_size` nodes one by one
  * For each popped node, push its left child and then its right child (if they exist)
  * If the node we popped was the **last one** of this level (position `level_size - 1`), add its value to the answer
* When the queue empties out, the answer holds the right view

<br>

### Code

```python
from collections import deque

class Solution:
    def rightSideView(self, root):
        if not root:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)

            for i in range(level_size):
                node = queue.popleft()

                if i == level_size - 1:   # last node of this level
                    result.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return result
```

<br>

### Dry Run

```ini
Input tree: root = [1,2,3,null,5,null,4]

        1
      /   \
     2     3
      \     \
       5     4

Start: result = [], queue = [1]

===== LEVEL 0 =====
queue = [1]
level_size = 1   (freeze this, only node 1 belongs to level 0)

  i = 0 -> pop node 1
          is i == level_size - 1 ? 0 == 0 -> YES, this is the last of the level
          record 1
          result = [1]
          push left child  2 -> queue = [2]
          push right child 3 -> queue = [2, 3]

level 0 finished
queue = [2, 3]

===== LEVEL 1 =====
level_size = 2   (freeze this, nodes 2 and 3 belong to level 1)

  i = 0 -> pop node 2
          is i == level_size - 1 ? 0 == 1 -> NO, node 2 is hidden
          do not record
          result = [1]
          node 2 has no left child  -> nothing pushed
          push right child 5        -> queue = [3, 5]

  i = 1 -> pop node 3
          is i == level_size - 1 ? 1 == 1 -> YES, this is the last of the level
          record 3
          result = [1, 3]
          node 3 has no left child  -> nothing pushed
          push right child 4        -> queue = [5, 4]

level 1 finished
queue = [5, 4]

===== LEVEL 2 =====
level_size = 2   (freeze this, nodes 5 and 4 belong to level 2)

  i = 0 -> pop node 5
          is i == level_size - 1 ? 0 == 1 -> NO, node 5 is hidden
          do not record
          result = [1, 3]
          node 5 has no children -> nothing pushed
          queue = [4]

  i = 1 -> pop node 4
          is i == level_size - 1 ? 1 == 1 -> YES, this is the last of the level
          record 4
          result = [1, 3, 4]
          node 4 has no children -> nothing pushed
          queue = []

level 2 finished
queue = []  -> while loop stops

Final Answer: result = [1, 3, 4]
```

<br>

### Complexity

* **Time:** `O(n)`, every node is pushed once and popped once
* **Space:** `O(w)`, where `w` is the maximum width of the tree, because the queue holds at most one level at a time. In the worst case (a full bottom level) this becomes `O(n)`

<br><br>

## Which One Should You Use in an Interview?

* **BFS** is easier to explain out loud because it mirrors the real world picture of looking at the tree from the side. It is the safer default.
* **DFS** is shorter to write and often impresses, but you must clearly say the key line, that going right before left makes the first visit at each depth the correct answer.
* A good move is to mention both, code one, and note the space trade off. DFS uses stack space proportional to height, BFS uses queue space proportional to width.

<br><br>

## Related Problems

* [Binary Tree Level Order Traversal (102)](https://leetcode.com/problems/binary-tree-level-order-traversal/)
* [Binary Tree Zigzag Level Order Traversal (103)](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/)
* [Maximum Depth of Binary Tree (104)](https://leetcode.com/problems/maximum-depth-of-binary-tree/)
* [Binary Tree Level Order Traversal II (107)](https://leetcode.com/problems/binary-tree-level-order-traversal-ii/)
* [Populating Next Right Pointers in Each Node (116)](https://leetcode.com/problems/populating-next-right-pointers-in-each-node/)
* [Find Bottom Left Tree Value (513)](https://leetcode.com/problems/find-bottom-left-tree-value/)
* [Find Largest Value in Each Tree Row (515)](https://leetcode.com/problems/find-largest-value-in-each-tree-row/)
* [Average of Levels in Binary Tree (637)](https://leetcode.com/problems/average-of-levels-in-binary-tree/)
* [Maximum Level Sum of a Binary Tree (1161)](https://leetcode.com/problems/maximum-level-sum-of-a-binary-tree/)
* [Deepest Leaves Sum (1302)](https://leetcode.com/problems/deepest-leaves-sum/)
* [Vertical Order Traversal of a Binary Tree (987)](https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree/)