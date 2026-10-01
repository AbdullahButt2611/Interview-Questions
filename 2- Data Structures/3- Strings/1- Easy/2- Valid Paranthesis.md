# Valid Parentheses

`Google` • `Amazon` • `Meta` • `Microsoft` • `Apple` • `Bloomberg` • `LinkedIn` • `Goldman Sachs`

## Problem Statement
Given a string `s` containing just the characters `(`, `)`, `{`, `}`, `[` and `]`, determine if the input string is valid.

An input string is valid if:

- Open brackets must be closed by the same type of brackets.
- Open brackets must be closed in the correct order.
- Every close bracket has a corresponding open bracket of the same type.

## Examples
**Example 1:**

```ini
Input: s = "()"
Output: true
```

**Example 2:**

```ini
Input: s = "()[]{}"
Output: true
```

**Example 3:**

```ini
Input: s = "(]"
Output: false
```

**Example 4:**

```ini
Input: s = "([])"
Output: true
```

**Example 5:**

```ini
Input: s = "([)]"
Output: false
```

## Constraints
- `1 <= s.length <= 10^4`
- `s` consists of parentheses only `()[]{}`.

<br><br>

## Approach
Think of it like stacking plates. Every time you open a bracket, you put it on top of a pile. The rule of a valid string is simple: the bracket you close must always match the one sitting on top of the pile, because that is the most recent one you still have to deal with.

So we read the string one character at a time and keep a `stack` (just a list that we add to and remove from the top).

For each character, we look at what is currently on top of the stack:

- If the stack is empty, there is nothing to match against yet, so we simply put the current character on top and move on.
- If the current character is a closing bracket and the top of the stack is its matching opening bracket, then we found a complete pair. We remove (pop) that opening bracket from the stack because it is now settled.
- In every other case, we put the current character on top of the stack.

Here is the important part. The only way a bracket ever leaves the stack is when it gets properly closed by its correct partner. That means if the string is perfectly balanced, every opening bracket will eventually find its match and the stack will end up completely empty.

So after we finish reading the whole string, we just ask one question: is the stack empty? If it is empty, every bracket was matched correctly and the string is valid. If anything is left behind, something was never closed properly, so the string is invalid.

That is the whole idea. Match from the top, pop when it fits, and check that nothing is left at the end.

<mark>The core intuition: the last opening bracket you see must be the first one that gets closed. This Last In First Out behaviour is exactly why a stack is the perfect tool here.</mark>

<br><br>

## Code

```python
class Solution:
    def isValid(self, s: str) -> bool:
        stack = []

        for char in s:
            if not stack:
                stack.append(char)
                continue
            
            if (char == ')' and stack[-1] == '(') or (char == '}' and stack[-1] == '{') or (char == ']' and stack[-1] == '['):
                stack.pop()
            else:
                stack.append(char)
        
        return not stack
```

<br><br>

## Dry Run
Let us walk through `s = "([])"` step by step so you can see exactly what happens to the stack at each moment.

```ini
Input: s = "([])"

Initial State:
stack = []

Iteration 1 -> char = '('
  Stack is empty, so nothing to match against.
  Action: push '(' onto the stack.
  stack = ['(']

Iteration 2 -> char = '['
  Top of stack is '('.
  '[' is not a closing bracket that matches '(', so no pair formed.
  Action: push '[' onto the stack.
  stack = ['(', '[']

Iteration 3 -> char = ']'
  Top of stack is '['.
  ']' is the correct closing bracket for '[', so a pair is complete.
  Action: pop '[' off the stack.
  stack = ['(']

Iteration 4 -> char = ')'
  Top of stack is '('.
  ')' is the correct closing bracket for '(', so a pair is complete.
  Action: pop '(' off the stack.
  stack = []

End of string reached.
Check: is the stack empty? Yes.
Every bracket was matched correctly.

Output: true
```

Now let us try an invalid one, `s = "([)]"`, so you can see how it catches the mistake.

```ini
Input: s = "([)]"

Initial State:
stack = []

Iteration 1 -> char = '('
  Stack is empty.
  Action: push '(' onto the stack.
  stack = ['(']

Iteration 2 -> char = '['
  Top of stack is '('.
  '[' does not close '(', so no pair.
  Action: push '[' onto the stack.
  stack = ['(', '[']

Iteration 3 -> char = ')'
  Top of stack is '['.
  ')' does not match '[' (it would need ']' on top).
  Action: push ')' onto the stack.
  stack = ['(', '[', ')']

Iteration 4 -> char = ']'
  Top of stack is ')'.
  ']' does not match ')'.
  Action: push ']' onto the stack.
  stack = ['(', '[', ')', ']']

End of string reached.
Check: is the stack empty? No, it still has leftover brackets.
The brackets were closed in the wrong order.

Output: false
```

<br><br>

## Complexity
- **Time Complexity:** `O(n)` because we visit each character of the string exactly once.
- **Space Complexity:** `O(n)` because in the worst case (all opening brackets) the stack can hold every character.

<br><br>

## Related Problems
- [Generate Parentheses (22)](https://leetcode.com/problems/generate-parentheses/)
- [Longest Valid Parentheses (32)](https://leetcode.com/problems/longest-valid-parentheses/)
- [Remove Invalid Parentheses (301)](https://leetcode.com/problems/remove-invalid-parentheses/)
- [Minimum Remove to Make Valid Parentheses (1249)](https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/)
- [Valid Parenthesis String (678)](https://leetcode.com/problems/valid-parenthesis-string/)
- [Check If Word Is Valid After Substitutions (1003)](https://leetcode.com/problems/check-if-word-is-valid-after-substitutions/)