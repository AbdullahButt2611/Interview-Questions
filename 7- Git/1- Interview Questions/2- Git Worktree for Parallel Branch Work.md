# How Do You Work on Multiple Branches Simultaneously Without Stashing or Cloning?

## What This Question Is Asking

The question is really about whether you know a cleaner alternative to the usual "stash and switch" dance when you need to be on two branches at once.

A typical trigger scenario: you are deep in a feature branch with many uncommitted changes, and suddenly production breaks and you must ship a hotfix now. The interviewer wants to know:

- How you would handle that interruption **without losing or risking your current work**.
- Whether you know the `git worktree` feature and can explain **what it does and why it helps**.
- How it **differs from `git stash`** and from cloning the repo a second time.

<mark>The core idea to land: a worktree lets one repository have several working directories checked out at once, so you can work on multiple branches in parallel with no stashing and no branch switching.</mark>

<br><br>

## How to Answer This Well

- Start by naming the **pain point** (stashing, switching, and hoping nothing breaks) so the interviewer sees you understand the problem.
- Define a worktree in **one clean sentence** before showing any commands.
- Show the **three commands** that cover the whole lifecycle (add, list, remove).
- Draw a **direct contrast with `git stash`** so the trade-off is obvious.
- Close with a couple of **real use cases** and a crisp one-line definition.
<br><br>

## Answer

### The problem it solves

You are on a feature branch, 50 files changed, half of them uncommitted. Then production goes down and you need to fix it immediately.

The common approach is to stash the changes, switch branches, fix the bug, switch back, and hope nothing broke in between. It works, but it interrupts your flow and puts your in-progress work at risk.

<br><br>

### What a Git worktree is

A Git worktree lets you check out multiple branches into separate directories at the same time, all backed by the same repository.

- No stashing.
- No branch switching.
- No extra clones of the repository.

In short: two branches, one repository, multiple working directories.

<br><br>

### How to use it

Create a new worktree (a new folder checked out to a branch):

```bash
git worktree add ../hotfix-folder hotfix-branch
```

Now you can fix the production issue inside `../hotfix-folder` while your feature branch stays completely untouched in the original directory.

List all worktrees:

```bash
git worktree list
```

Remove a worktree when you are done:

```bash
git worktree remove ../hotfix-folder
```

<br><br>

### Git stash vs Git worktree

| Aspect | Git Stash | Git Worktree |
|--------|-----------|--------------|
| **What it does** | Temporarily shelves your changes | Creates parallel working directories |
| **Branches at once** | One branch at a time | Multiple branches simultaneously |
| **Effect on flow** | Interrupts your workflow | No context switching needed |

The key distinction: `git stash` solves the interruption temporarily, while `git worktree` removes the need to interrupt at all.

<br><br>

### Real-world use cases

- Fix an urgent production issue while a feature is still in progress.
- Compare two branches side by side in two folders.
- Review a pull request without disturbing your current work.
- Run a long test suite on `main` while you keep developing elsewhere.

<mark>Interview-ready line: Git worktree lets developers check out multiple branches simultaneously in separate directories, enabling parallel development without stashing changes, switching branches, or cloning the repository.</mark>
<br><br>

## Other Ways This Question Can Be Asked

- What is a Git worktree, and when would you use one?
- How would you handle an urgent hotfix while you have uncommitted work on a feature branch?
- What is the difference between `git stash` and `git worktree`?
- How can you have two branches checked out at the same time without cloning the repo twice?
- How do you list and clean up worktrees once you are finished with them?