# Kth Last Element of a Singly Linked List

`Amazon` • `Microsoft` • `Cisco` • `CodeQuotient` • `Educative`

## Problem Statement

Given the `head` of a **singly linked list** and an integer `k`, find the **kth last element** of the list (the kth node counting from the **end**).

```cpp
Node* KthLastElement(Node* head, int k)
```

- The **1st last** element is the last node of the list.
- The **2nd last** element is the node just before it, and so on.
- If the list has fewer than `k` nodes, there is no such element. Return `None`.

## Examples

**Example 1:**

```ini
Input: head = [1,2,3,4,5], k = 2
Output: 4
Explanation: Counting from the end: 5 is the 1st last, 4 is the 2nd last.
```

**Example 2:**

```ini
Input: head = [1,2,3,4,5], k = 5
Output: 1
Explanation: The list has 5 nodes, so the 5th last element is the very first node.
```

**Example 3:**

```ini
Input: head = [1,2,3,4,5], k = 7
Output: None
Explanation: The list has only 5 nodes. There is no 7th last element.
```

## Constraints

- The number of nodes in the list is in the range `[0, 10^5]`.
- `-10^5 <= Node.val <= 10^5`
- `k >= 1`

<br><br>

## The One Rule to Remember

A singly linked list only moves **forward**. <mark>You can never walk backwards from the end.</mark>

- So "count from the end" must be turned into "count from the front".
- Both approaches below do exactly that, just in different ways.

<br><br>

## Approach 1: Count First, Then Walk (Two Passes)

### The Idea

If you know how long the list is, the kth last node is just a normal position from the front.

- A list of `5` nodes, `k = 2`.
- The 2nd last node is node number `5 - 2 + 1 = 4` from the front.
- To reach node 4 from the head, you take `5 - 2 = 3` steps.

### Step by Step

1. **Count the nodes.**
   - Start at the head with `length = 0`.
   - Walk to the end, adding 1 for every node. This gives `length`.
2. **Check if `k` is valid.**
   - If `k > length`, the list is too short. Return `None`.
3. **Walk again from the head.**
   - Take exactly `length - k` steps forward.
   - The node you land on is the answer.

> Memory hook: <mark>"Count it, then walk length minus k."</mark>

### Solution

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def KthLastElement(head, k):
    if head is None or k <= 0:
        return None

    # Pass 1: count the nodes
    length = 0
    current = head
    while current:
        length += 1
        current = current.next

    # The list is too short
    if k > length:
        return None

    # Pass 2: take (length - k) steps from the head
    current = head
    for _ in range(length - k):
        current = current.next

    return current
```

### Dry Run

```ini
=====================================================
SCENARIO A: head = [1,2,3,4,5], k = 2
=====================================================

Starting List:

  1 → 2 → 3 → 4 → 5 → None

Check: Is head None or k <= 0? NO. Continue.

Pass 1: Count the nodes
  Setup: length = 0, current = 1

  Iteration 1:
    Loop check: current = 1 exists. Enter loop.
    length = 0 + 1 = 1
    current = 1.next = 2

  Iteration 2:
    Loop check: current = 2 exists. Enter loop.
    length = 1 + 1 = 2
    current = 2.next = 3

  Iteration 3:
    Loop check: current = 3 exists. Enter loop.
    length = 2 + 1 = 3
    current = 3.next = 4

  Iteration 4:
    Loop check: current = 4 exists. Enter loop.
    length = 3 + 1 = 4
    current = 4.next = 5

  Iteration 5:
    Loop check: current = 5 exists. Enter loop.
    length = 4 + 1 = 5
    current = 5.next = None

  Iteration 6:
    Loop check: current = None. Exit loop.

  length = 5

Check: Is k (2) > length (5)? NO. Continue.

Pass 2: Walk (length - k) = 5 - 2 = 3 steps from the head
  Setup: current = 1

  Step 1: current = 1.next = 2
  Step 2: current = 2.next = 3
  Step 3: current = 3.next = 4

  3 steps done. Stop.

Nodes visited in total: 5 (counting) + 3 (walking) = 8
The list was read TWICE.

Return node 4
Output: 4  ✓


=====================================================
SCENARIO B: head = [1,2,3,4,5], k = 7  (k is bigger than the list)
=====================================================

Starting List:

  1 → 2 → 3 → 4 → 5 → None

Check: Is head None or k <= 0? NO. Continue.

Pass 1: Count the nodes
  Same walk as Scenario A.
  length = 5

Check: Is k (7) > length (5)? YES.
  The list is too short. Return None.

Pass 2 never starts.

Output: None  ✓
```

### Complexity Analysis

- **Time Complexity:** `O(N)`, where `N` is the number of nodes.
  - Counting visits all `N` nodes.
  - Walking takes another `N - k` steps.
  - Total work is about `2N - k`, which is still `O(N)`.
- **Space Complexity:** `O(1)`.
  - Only `length` and `current` are used.

### The Demerit

- It walks the list **two times**: once to count, once to reach the answer.
- In an interview, the follow up is almost always: **"Can you do it in one pass?"**
- If the list is huge, or the nodes are expensive to visit (for example, data coming from a slow source or a stream), reading everything twice is wasteful.
- We needed the length only to answer one question: "how far is this node from the end?" Approach 2 answers that **without ever counting**.

<br><br>

## Approach 2: Two Pointers With a Gap (One Pass)

### The Idea

Think of a **stick that is exactly `k` steps long**.

- Put one end of the stick (`slow`) at the head, and the other end (`fast`) `k` steps ahead.
- Now slide the whole stick forward, one step at a time, keeping its length the same.
- The moment the front end (`fast`) falls off the list (reaches `None`), the back end (`slow`) is **exactly `k` steps before the end**.
- That is the kth last node.

### Step by Step

1. **Put both pointers at the head.**
   - `slow = head`, `fast = head`.
2. **Give `fast` a head start of `k` steps.**
   - Move `fast` forward one step at a time, `k` times.
   - Before every step, check that `fast` is not `None`.
   - If `fast` runs out before `k` steps, the list is shorter than `k`. Return `None`.
3. **Move both pointers together.**
   - While `fast` is not `None`, move `slow` one step and `fast` one step.
   - The gap between them always stays `k`.
4. **Stop when `fast` falls off the list.**
   - `fast` is now `None` (one step past the last node).
   - `slow` is `k` steps behind it, so `slow` is the kth last node. Return it.

> Why does it work? When `fast` is at `None`, the distance from `slow` to the end is `k`. That is the definition of "kth last".

> Memory hook: <mark>"Give fast a k step head start. Then walk together. When fast falls off, slow is the answer."</mark>

### Solution

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def KthLastElement(head, k):
    slow = head
    fast = head

    # Give fast a head start of k steps
    while k > 0:
        if not fast:
            return None  # The list is shorter than k
        fast = fast.next
        k -= 1

    # Move both together until fast falls off the list
    while fast:
        slow = slow.next
        fast = fast.next

    return slow
```

### Dry Run

```ini
=====================================================
SCENARIO A: head = [1,2,3,4,5], k = 2
=====================================================

Starting List:

  1 → 2 → 3 → 4 → 5 → None

Setup:
  slow = 1
  fast = 1
  k    = 2

Phase 1: Give fast a head start of k = 2 steps

  Iteration 1:
    Loop check: k = 2 > 0. Enter loop.
    Is fast None? NO (fast = 1).
    Move fast: fast = 1.next = 2
    k = 2 - 1 = 1

    1 → 2 → 3 → 4 → 5 → None
    ↑   ↑
    S   F

  Iteration 2:
    Loop check: k = 1 > 0. Enter loop.
    Is fast None? NO (fast = 2).
    Move fast: fast = 2.next = 3
    k = 1 - 1 = 0

    1 → 2 → 3 → 4 → 5 → None
    ↑       ↑
    S       F

  Iteration 3:
    Loop check: k = 0. Condition 0 > 0 is False. Exit loop.

  The gap between slow and fast is now exactly 2 steps (the stick is ready).

Phase 2: Move both together until fast falls off

  Iteration 1:
    Loop check: fast = 3 exists. Enter loop.
    slow = 1.next = 2
    fast = 3.next = 4

    1 → 2 → 3 → 4 → 5 → None
        ↑       ↑
        S       F

  Iteration 2:
    Loop check: fast = 4 exists. Enter loop.
    slow = 2.next = 3
    fast = 4.next = 5

    1 → 2 → 3 → 4 → 5 → None
            ↑       ↑
            S       F

  Iteration 3:
    Loop check: fast = 5 exists. Enter loop.
    slow = 3.next = 4
    fast = 5.next = None

    1 → 2 → 3 → 4 → 5 → None
                ↑        ↑
                S        F

  Iteration 4:
    Loop check: fast = None. Exit loop.

State after the walk:
  fast = None  (fell off the list)
  slow = 4     (exactly 2 steps behind None)

Counting back from None: 5 is the 1st last, 4 is the 2nd last. ✓
The list was read only ONCE (fast touched every node one time).

Return node 4
Output: 4  ✓


=====================================================
SCENARIO B: head = [1,2,3,4,5], k = 5  (answer is the head)
=====================================================

Starting List:

  1 → 2 → 3 → 4 → 5 → None

Setup:
  slow = 1
  fast = 1
  k    = 5

Phase 1: Give fast a head start of k = 5 steps

  Iteration 1:
    Loop check: k = 5 > 0. Enter loop.
    Is fast None? NO (fast = 1).
    Move fast: fast = 2
    k = 4

  Iteration 2:
    Loop check: k = 4 > 0. Enter loop.
    Is fast None? NO (fast = 2).
    Move fast: fast = 3
    k = 3

  Iteration 3:
    Loop check: k = 3 > 0. Enter loop.
    Is fast None? NO (fast = 3).
    Move fast: fast = 4
    k = 2

  Iteration 4:
    Loop check: k = 2 > 0. Enter loop.
    Is fast None? NO (fast = 4).
    Move fast: fast = 5
    k = 1

  Iteration 5:
    Loop check: k = 1 > 0. Enter loop.
    Is fast None? NO (fast = 5).
    Move fast: fast = 5.next = None
    k = 0

  Iteration 6:
    Loop check: k = 0. Exit loop.

    1 → 2 → 3 → 4 → 5 → None
    ↑                    ↑
    S                    F

  Note: fast reached None, but only AFTER taking all 5 steps.
  The check "Is fast None?" happens BEFORE each step, so this is fine.

Phase 2: Move both together until fast falls off

  Iteration 1:
    Loop check: fast = None. The loop never runs.

State after the walk:
  fast = None
  slow = 1   (it never moved)

The list has exactly 5 nodes, so the 5th last is the first node. ✓

Return node 1
Output: 1  ✓


=====================================================
SCENARIO C: head = [1,2,3,4,5], k = 7  (k is bigger than the list)
=====================================================

Starting List:

  1 → 2 → 3 → 4 → 5 → None

Setup:
  slow = 1
  fast = 1
  k    = 7

Phase 1: Give fast a head start of k = 7 steps

  Iteration 1:
    Loop check: k = 7 > 0. Enter loop.
    Is fast None? NO (fast = 1).
    Move fast: fast = 2
    k = 6

  Iteration 2:
    Loop check: k = 6 > 0. Enter loop.
    Is fast None? NO (fast = 2).
    Move fast: fast = 3
    k = 5

  Iteration 3:
    Loop check: k = 5 > 0. Enter loop.
    Is fast None? NO (fast = 3).
    Move fast: fast = 4
    k = 4

  Iteration 4:
    Loop check: k = 4 > 0. Enter loop.
    Is fast None? NO (fast = 4).
    Move fast: fast = 5
    k = 3

  Iteration 5:
    Loop check: k = 3 > 0. Enter loop.
    Is fast None? NO (fast = 5).
    Move fast: fast = 5.next = None
    k = 2

  Iteration 6:
    Loop check: k = 2 > 0. Enter loop.
    Is fast None? YES. fast has fallen off the list.
    It still needed 2 more steps, so the list is shorter than k.
    Return None immediately.

Phase 2 never starts.

Output: None  ✓
```

### Complexity Analysis

- **Time Complexity:** `O(N)`.
  - `fast` visits every node exactly once, so this is a **single pass**.
  - `slow` follows behind and makes only `N - k` moves.
- **Space Complexity:** `O(1)`.
  - Only two pointers (`slow`, `fast`) are used.
  - No extra list, no recursion.

<br><br>

## Which One to Pick?

- **Approach 1** is the easiest to come up with and explain.
- **Approach 2** is what interviewers want: same `O(N)` time, but only **one pass** and no need to know the length.

<br><br>

## Related Problems

- [Remove Nth Node From End of List (19)](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)
- [Rotate List (61)](https://leetcode.com/problems/rotate-list/)
- [Linked List Cycle (141)](https://leetcode.com/problems/linked-list-cycle/)
- [Linked List Cycle II (142)](https://leetcode.com/problems/linked-list-cycle-ii/)
- [Reorder List (143)](https://leetcode.com/problems/reorder-list/)
- [Intersection of Two Linked Lists (160)](https://leetcode.com/problems/intersection-of-two-linked-lists/)
- [Palindrome Linked List (234)](https://leetcode.com/problems/palindrome-linked-list/)
- [Middle of the Linked List (876)](https://leetcode.com/problems/middle-of-the-linked-list/)
- [Swapping Nodes in a Linked List (1721)](https://leetcode.com/problems/swapping-nodes-in-a-linked-list/)
- [Delete the Middle Node of a Linked List (2095)](https://leetcode.com/problems/delete-the-middle-node-of-a-linked-list/)
