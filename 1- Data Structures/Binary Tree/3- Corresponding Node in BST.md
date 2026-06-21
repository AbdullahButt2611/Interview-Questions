## Find a Corresponding Node of a Binary Tree in a Clone of That Tree
`Educative`

```python
class Solution:
    def __init__(self):
        self.res = None

    def getTargetCopy(self, original, cloned, target):
        self.dfs(original, cloned, target)
        return self.res

    def dfs(self, original, cloned, target):
        if original is None:
            return
        if original == target:
            self.res = cloned
            return
        self.dfs(original.left, cloned.left, target)
        self.dfs(original.right, cloned.right, target)

```

