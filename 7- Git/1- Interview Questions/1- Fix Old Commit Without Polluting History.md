# How Do You Fix a Bug in a Commit Made 5 Commits Ago Without Polluting Git History?

`Amazon` • `Atlassian` • `GitLab` • `Compile Code Club`

## Question

You made 10 clean commits, then found a small bug in commit number 6. How do you fix it without adding a messy "fix typo" commit on top, keeping your history clean as if the bug were never there?

<br><br>

## Answer

Each commit is like a photo you take after finishing a room in a house. If room 6 has a crack, you do not want a sticky note on photo 10 saying "room 6 was broken." You want photo 6 to look perfect all along. So instead of stacking a correction commit on top, you fold the fix back into the original commit. The cleanest way to do this is `git commit --fixup` paired with `git rebase --autosquash`.

### Your Three Options

| Option | What You Do | Result |
|--------|-------------|--------|
| **A: New "fix typo" commit** | Commit the fix on top as usual | Works, but leaves a junk commit in your history forever whose only job is to patch an earlier one |
| **B: Manual interactive rebase** | Edit the old commit by hand, switching `pick` to `edit` and stepping through it | Works, but feels error prone |
| **C: `git commit --fixup` (recommended)** | Tell Git the fix belongs to a specific old commit | Git quietly merges it in and deletes the temporary patch. Clean history, minimal stress |

### The Starting History

```
abc1234 → feat: add login page
def5678 → feat: add dashboard
ghi9012 → feat: add payment flow   (bug lives here)
jkl3456 → feat: add profile page
mno7890 → feat: add settings page
```

The short codes (like `ghi9012`) are Git's ID tags for each commit, like a serial number on a photo. The bug is inside the payment flow commit, `ghi9012`.

<br><br>

### Step 1: Fix the Bug and Commit It as a Fixup

Fix the code, stage it, then run:

```bash
git add <files>
git commit --fixup ghi9012
```

This means "save my fix and note that it belongs to commit `ghi9012`." Git creates a commit whose message starts with `fixup!`:

```
pqr1234 → fixup! feat: add payment flow
```

That `fixup!` prefix is the secret handshake Git uses later to recognize the patch. At this point the original payment commit is still there, with the fixup waiting at the bottom:

```
abc1234 → feat: add login page
def5678 → feat: add dashboard
ghi9012 → feat: add payment flow          (original, still here)
jkl3456 → feat: add profile page
mno7890 → feat: add settings page
pqr1234 → fixup! feat: add payment flow   (your fix, waiting)
```

Nothing is merged yet. The original stays put until the next step runs.

<br><br>

### Step 2: Squash It In With Autosquash

```bash
git rebase -i --autosquash HEAD~6
```

In plain words: `git rebase -i` rewrites recent history interactively, `--autosquash` handles any `fixup!` commits for you, and `HEAD~6` sets how far back you can edit. Git slides the fixup up under the payment commit, merges them into one, and deletes the temporary fixup:

```
abc1234 → feat: add login page
def5678 → feat: add dashboard
ghi9012 → feat: add payment flow   (now silently contains your fix)
jkl3456 → feat: add profile page
mno7890 → feat: add settings page
```

The `fixup!` commit is gone, and room 6 looks perfect.

### Picking the HEAD Number

The rule is simple: aim the rebase at the parent of the buggy commit (the commit right before it). If the bug is 5 commits back, use `HEAD~6`, one step further than the buggy commit. Interactive rebase can only edit commits after the base you give it, so you always go one step past. Do not memorize a number, just target the commit right before the broken one.

<br><br>

### Step 3: Make Autosquash Automatic (Optional)

To avoid typing `--autosquash` every time:

```bash
git config --global rebase.autoSquash true
```

`--global` applies it to all your projects. From now on every interactive rebase handles fixup commits on its own. (Note: this only applies to interactive rebases with `-i`. A plain `git rebase` will not autosquash.)

<br><br>

### The Safety Caveat

This rewrites history, changing the ID codes on that commit and every commit after it. That is safe while the commits live only on your machine. But if you already pushed and teammates built on top, rewriting can break their work. Two honest choices then:

- Coordinate with your team and update the remote with `git push --force-with-lease` (safer than `--force`).
- Or just accept a small follow-up fix commit.

A clean history is nice, but not worth breaking someone else's work.