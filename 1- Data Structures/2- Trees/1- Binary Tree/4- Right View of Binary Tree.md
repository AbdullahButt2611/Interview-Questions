## Right View of Binary Tree
`Educative`

```python
class Solution:
    def rightSideView(self, root):
        result = []
        self.rightView(root, result, 0)
        return result
        
    def rightView(self, curr, result, currDepth):
        if not curr:
            return
        if currDepth == len(result):
            result.append(curr.val)
        self.rightView(curr.right, result, currDepth + 1)
        self.rightView(curr.left, result, currDepth + 1)
```

## Iterative Approach

```python
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

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
                if i == level_size - 1:  # Check if it's the last node in the level
                    result.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return result
```