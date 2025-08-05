# Iterative In-order Traversal of Binary Tree

`Educative`

```python
# Function that prints the in-order traversal of the binary tree
def inorder_iterative(root):
  result = ""
  if not root:
      # If the root is None, we simply print None
      print("None", end = "")
  else:
      # Initializing the stack
      stk = deque()
      curr_node = root

      # This loop will keep printing the tree node in "L N R" fashion
      # until the current node is None or the stack becomes empty
      while stk or curr_node:
          # If the current node is not None, we push it into the stack and point it
          # to its left child and skip to the next iteration
          if curr_node:
              stk.append(curr_node)
              curr_node = curr_node.left
              continue

          # Current node is None, meaning that it's time to print the nodes in the "L"
          # sub-tree
          # So, printing and popping the top-most element of the stack
          result += str(stk[-1].data) + ", "
          curr_node = stk[-1].right
          stk.pop()

      # Truncating right most comma
      result_ = result[:-2]
      print(str(result_), end = "")
```


### 🌳 **In-order Traversal (LNR)**

In-order traversal means visiting nodes in this order:

> **Left → Node → Right**

This is typically done **recursively**, but here it’s done **iteratively using a stack**.


### 🧠 **Why Use a Stack?**

Recursion uses the **call stack** under the hood. To simulate recursion manually, we use our own **explicit stack** to keep track of nodes.


### 📘 Full Explanation of the Code

```python
from collections import deque  # Needed for stack

def inorder_iterative(root):
    result = ""
    if not root:
        print("None", end="")
        return
```

* If the tree is empty (`root is None`), print `"None"` and return.


```python
    stk = deque()         # stack to store nodes
    curr_node = root      # start from the root
```

* We use a **stack (`stk`)** to remember nodes we haven’t fully processed yet.
* `curr_node` is our traversal pointer.


### 🔁 Loop Begins

```python
    while stk or curr_node:
```

We keep looping as long as:

* There's something in the stack (unprocessed ancestors), or
* `curr_node` is not `None` (we're still exploring the tree)


### ⬅️ Step 1: Go Left

```python
        if curr_node:
            stk.append(curr_node)
            curr_node = curr_node.left
            continue
```

* If `curr_node` is not `None`, we push it onto the stack.
* Then move left (`curr_node = curr_node.left`)
* This mimics the **Left** step of LNR.

We keep pushing left children until we hit a leaf (`curr_node == None`).


### 🔄 Step 2: Visit Node, Go Right

```python
        result += str(stk[-1].data) + ", "
        curr_node = stk[-1].right
        stk.pop()
```

Now `curr_node` is `None`, so:

* Pop the top of the stack.
* This is the **Node (N)** step of LNR.
* Append the node’s value to `result`.
* Then move to the right child: **Right (R)** step.

This restarts the loop.


### 🧹 Final Touch

```python
    result_ = result[:-2]  # remove the trailing ", "
    print(str(result_), end = "")
```

* Remove the last comma and space from the result string.
* Print the final in-order traversal.


### ✅ Example Walkthrough

Consider the tree:

```
      1
     / \
    2   3
   /
  4
```

* In-order should be: **4, 2, 1, 3**

Steps:

1. Go to 1 → push to stack
2. Go to 2 → push
3. Go to 4 → push
4. No left → process 4
5. Back to 2 → process
6. Back to 1 → process
7. Go to 3 → process

Result: `"4, 2, 1, 3"`

