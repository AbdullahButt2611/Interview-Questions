# Reopen Closed Tab

## Question

You accidentally close a browser tab. Chrome brings it back instantly with "Reopen Closed Tab" (`Ctrl + Shift + T`).

- Which data structure is Chrome using?
- How would you design it?

## Answer

<mark>A stack. The last tab you closed is the first one you get back (LIFO). A real browser caps the stack's size and saves it to disk so it survives a crash.</mark>

<br><br>

### Why a Stack

Say you close three tabs in this order:

```ini
Close A
Close B
Close C
```

When you hit "Reopen Closed Tab", you expect **C** first, because it's the one you just lost. Press again and you get **B**, then **A**.

That is Last In, First Out, which is exactly what a stack does.

```ini
Top → C
      B
      A
```

<br><br>

### Step 1: Push on Close

Every time a tab closes, push an entry onto the stack. The entry stores more than the URL:

- URL and title
- Navigation history (so Back and Forward still work after restore)
- Scroll position
- Which window it was in and its position in the tab strip

Push is `O(1)`.

<br><br>

### Step 2: Pop on Restore

"Reopen Closed Tab" pops the top entry and opens a tab from it.

```ini
Stack: [A, B, C]   →  pop  →  restore C
Stack: [A, B]      →  pop  →  restore B
Stack: [A]
```

Pop is `O(1)`, which is why the restore feels instant.

<br><br>

### Step 3: Cap the Size

An unbounded stack grows forever if someone closes thousands of tabs. So the stack keeps only the most recent N entries. When it's full, the **oldest** entry (the bottom) gets dropped.

Chrome keeps about 25 entries.

A plain stack can't remove from the bottom cheaply, so use a **deque** (or a ring buffer) instead:

- Push and pop at the top
- Drop from the bottom when full
- All three are `O(1)`

```python
from collections import deque

closed_tabs = deque(maxlen=25)   # oldest entry falls off automatically

def on_tab_close(tab):
    closed_tabs.append(tab)

def reopen_closed_tab():
    if closed_tabs:
        return closed_tabs.pop()
    return None
```

<br><br>

### Step 4: Persist to Disk

If the stack only lives in memory, a crash or restart wipes it. So the browser writes the closed-tab list to disk every so often.

- **Memory:** gives the instant restore
- **Disk:** brings the list back after a crash or restart (this is also what "Restore previous session" uses)

<br><br>

### Follow-up: Closing a Whole Window

If you close a window with 10 tabs, "Reopen" should bring back the whole window, not one tab.

So each stack entry is either a **tab** or a **window** (a group of tabs). One pop restores the whole entry.

<br><br>

### Final Design

| Part         | Choice                      | Why                                      |
| :----------- | :-------------------------- | :--------------------------------------- |
| Order        | Stack (LIFO)                | Most recently closed comes back first    |
| Size limit   | Deque / ring buffer, max N  | `O(1)` drop of the oldest entry          |
| Entry        | Tab or window snapshot      | Restores history, scroll, and position   |
| Persistence  | Periodic save to disk       | Survives crashes and restarts            |

<br><br>

### Interview Ready Line

> "It's a stack, because the last tab you closed should come back first. In practice I'd use a bounded deque so the oldest entries drop off in O(1), store a full snapshot of each tab (URL, history, scroll position), and save the list to disk so it survives a crash."

<br><br>

## Other Ways to Ask This Question

- How does `Ctrl + Shift + T` work in a browser?
- Design the "Recently Closed Tabs" feature for a browser.
- Which data structure would you use for an undo feature, and why?
- How would you limit the size of an undo history without slowing it down?
- How does a browser restore your tabs after it crashes?
