# Implement Queue using Stacks

`Amazon` • `Microsoft` • `Google` • `Adobe` • `Goldman Sachs` • `Morgan Stanley`
<br>
## Problem Statement

Implement a first in first out (FIFO) queue using only two stacks. The implemented queue should support all the functions of a normal queue (`push`, `peek`, `pop`, and `empty`).

Implement the `MyQueue` class:

- `void push(int x)`: Pushes element x to the back of the queue.
- `int pop()`: Removes the element from the front of the queue and returns it.
- `int peek()`: Returns the element at the front of the queue.
- `boolean empty()`: Returns `true` if the queue is empty, `false` otherwise.

**Notes:**

- You must use only standard operations of a stack, which means only push to top, peek/pop from top, size, and is empty operations are valid.
- Depending on your language, the stack may not be supported natively. You may simulate a stack using a list or deque (double ended queue) as long as you use only a stack's standard operations.

## Examples

**Example 1:**

```
Input
["MyQueue", "push", "push", "peek", "pop", "empty"]
[[], [1], [2], [], [], []]
Output
[null, null, null, 1, 1, false]

Explanation
MyQueue myQueue = new MyQueue();
myQueue.push(1); // queue is: [1]
myQueue.push(2); // queue is: [1, 2] (leftmost is front of the queue)
myQueue.peek();  // return 1
myQueue.pop();   // return 1, queue is [2]
myQueue.empty(); // return false
```

## Constraints

- `1 <= x <= 9`
- At most `100` calls will be made to `push`, `pop`, `peek`, and `empty`.
- All the calls to `pop` and `peek` are valid (the queue will never be empty when these are called).

<br><br>

## Approach: Two Stacks (One for In, One for Out)

### The Core Idea

A stack only lets you reach the element you placed last (the top). A queue needs to reach the element placed first (the front). These are opposites, so a single stack alone cannot give us both.

The trick is to use two stacks with two different jobs:

- `enqueue`: a holding area where new elements land when we call `push`.
- `dequeue`: a ready area where elements wait in the correct order to leave the queue.

When `dequeue` is empty, we take everything out of `enqueue` one at a time and drop it into `dequeue`. Because a stack reverses order when you move items this way, the very first element that was pushed (the one stuck at the bottom of `enqueue`) ends up on top of `dequeue`, exactly where we need it for `pop` and `peek`.

### Code (Python)

```python
class MyQueue:

    def __init__(self):
        self.enqueue = []
        self.dequeue = []

    def push(self, x: int) -> None:
        self.enqueue.append(x)

    def pop(self) -> int:
        if not self.dequeue:
            while self.enqueue:
                self.dequeue.append(self.enqueue.pop())

        return self.dequeue.pop()

    def peek(self) -> int:
        if not self.dequeue:
            while self.enqueue:
                self.dequeue.append(self.enqueue.pop())

        return self.dequeue[-1]

    def empty(self) -> bool:
        return not self.enqueue and not self.dequeue


# Your MyQueue object will be instantiated and called as such:
# obj = MyQueue()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.peek()
# param_4 = obj.empty()
```

### Step by Step Walkthrough

Let's trace through the example from above. The right side of each stack is the top.

**1. `push(1)`**
`enqueue = [1]`, `dequeue = []`

**2. `push(2)`**
`enqueue = [1, 2]`, `dequeue = []`

**3. `peek()`**
`dequeue` is empty, so we move everything from `enqueue` to `dequeue`:
- pop `2` from `enqueue`, push it to `dequeue` → `dequeue = [2]`
- pop `1` from `enqueue`, push it to `dequeue` → `dequeue = [1, 2]`

Now `enqueue = []`, `dequeue = [1, 2]`. The top of `dequeue` is `1`, so `peek()` returns `1`. Notice `1` was the first thing pushed, and now it sits on top, ready to be read.

**4. `pop()`**
`dequeue` is not empty, so we skip the transfer. We just pop the top of `dequeue`, which is `1`. Returns `1`.
`enqueue = []`, `dequeue = [2]`

**5. `empty()`**
Both stacks together still hold `2`, so this returns `false`.

### Why It Works

Think of `enqueue` as a stack of plates being added one on top of another. The first plate placed is buried at the bottom. When that whole stack is picked up and placed, one plate at a time, onto a second stack, the order flips completely. The plate that was on the bottom (the oldest one) is now on top of the second stack. That is exactly the flip needed to turn "last in, first out" into "first in, first out".

This flip only happens when `dequeue` is empty, not on every single operation. So each element gets flipped at most once during its entire time in the queue.

### Complexity

- `push`: O(1), it is just one append.
- `pop` / `peek`: usually O(1). Only when `dequeue` is empty do we pay for the transfer, and that cost is spread out (amortized) across all the elements being moved, so on average it still works out to O(1) per call.
- `empty`: O(1).
- Space: O(n), where n is the number of elements currently in the queue.