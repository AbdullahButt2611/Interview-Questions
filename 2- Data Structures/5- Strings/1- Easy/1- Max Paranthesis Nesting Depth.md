# Maximum Nesting Depth of the Parentheses

`Amazon` • `Google` • `Meta`

## Problem Statement
Given a valid parentheses string `s`, return the nesting depth of `s`. The nesting depth is the maximum number of nested parentheses.

## Examples

**Example 1:**
```ini
Input: s = "(1+(2*3)+((8)/4))+1"
Output: 3
Explanation: Digit 8 is inside of 3 nested parentheses in the string.
```

**Example 2:**
```ini
Input: s = "(1)+((2))+(((3)))"
Output: 3
Explanation: Digit 3 is inside of 3 nested parentheses in the string.
```

**Example 3:**
```ini
Input: s = "()(())((()()))"
Output: 3
```

## Constraints
* `1 <= s.length <= 100`
* `s` consists of digits `0-9` and characters `'+'`, `'-'`, `'*'`, `'/'`, `'('`, and `')'`.
* It is guaranteed that parentheses expression `s` is a VPS.

<br><br>

## Approach

Think of the parentheses like floors in a building.

* Every time you see an opening bracket `(`, you go one floor up.
* Every time you see a closing bracket `)`, you come one floor down.
* All the other characters (digits, `+`, `-`, `*`, `/`) are just people standing on a floor. They do not move you up or down, so you can simply ignore them.

The question is only asking one thing: what was the **highest floor** you ever reached during the whole walk?

So we keep two simple values with us:

* `depth`, which tells us the floor we are standing on right now.
* `max_depth`, which remembers the highest floor we have touched so far.

Now we just walk through the string one character at a time:

* On a `(` we add 1 to `depth` (we climbed up), and then we check if this new floor beats our record. If it does, we update `max_depth`.
* On a `)` we subtract 1 from `depth` (we climbed down). We do not need to touch `max_depth` here, because going down can never set a new highest record.

When the walk is over, `max_depth` holds the deepest we ever went, and that is our answer.

The nice part is that we never need a stack to store the brackets. Since the string is guaranteed to be valid, a plain counter is enough. That keeps the memory usage constant.

<mark>Key idea: the nesting depth at any moment is simply the number of opening brackets that are still not closed, so counting up and down is all we need.</mark>

<br><br>

## Code

```python
class Solution:
    def maxDepth(self, s: str) -> int:
        max_depth = 0
        depth = 0

        for char in s:
            if char == '(':
                depth += 1
                max_depth = max(max_depth, depth)
            elif char == ')':
                depth -= 1
        
        return max_depth
```

<br><br>

## Dry Run

Let us take `s = "(1+(2*3)+((8)/4))+1"` and walk through it character by character.

```ini
Start: depth = 0, max_depth = 0

Iteration 1  -> char = '('
   depth becomes 1
   max_depth = max(0, 1) = 1

Iteration 2  -> char = '1'
   not a bracket, ignore
   depth = 1, max_depth = 1

Iteration 3  -> char = '+'
   not a bracket, ignore
   depth = 1, max_depth = 1

Iteration 4  -> char = '('
   depth becomes 2
   max_depth = max(1, 2) = 2

Iteration 5  -> char = '2'
   not a bracket, ignore
   depth = 2, max_depth = 2

Iteration 6  -> char = '*'
   not a bracket, ignore
   depth = 2, max_depth = 2

Iteration 7  -> char = '3'
   not a bracket, ignore
   depth = 2, max_depth = 2

Iteration 8  -> char = ')'
   depth becomes 1
   max_depth stays 2

Iteration 9  -> char = '+'
   not a bracket, ignore
   depth = 1, max_depth = 2

Iteration 10 -> char = '('
   depth becomes 2
   max_depth = max(2, 2) = 2

Iteration 11 -> char = '('
   depth becomes 3
   max_depth = max(2, 3) = 3

Iteration 12 -> char = '8'
   not a bracket, ignore
   depth = 3, max_depth = 3

Iteration 13 -> char = ')'
   depth becomes 2
   max_depth stays 3

Iteration 14 -> char = '/'
   not a bracket, ignore
   depth = 2, max_depth = 3

Iteration 15 -> char = '4'
   not a bracket, ignore
   depth = 2, max_depth = 3

Iteration 16 -> char = ')'
   depth becomes 1
   max_depth stays 3

Iteration 17 -> char = ')'
   depth becomes 0
   max_depth stays 3

Iteration 18 -> char = '+'
   not a bracket, ignore
   depth = 0, max_depth = 3

Iteration 19 -> char = '1'
   not a bracket, ignore
   depth = 0, max_depth = 3

End of string
Return max_depth = 3
```

**Final Answer: 3**

<br><br>

## Complexity

* **Time Complexity:** `O(n)`, where `n` is the length of the string. We look at each character exactly once.
* **Space Complexity:** `O(1)`, since we only use two counter variables no matter how long the string is.

<br><br>

## Related Problems

* [Valid Parentheses (20)](https://leetcode.com/problems/valid-parentheses/)
* [Remove Outermost Parentheses (1021)](https://leetcode.com/problems/remove-outermost-parentheses/)
* [Maximum Nesting Depth of Two Valid Parentheses Strings (1111)](https://leetcode.com/problems/maximum-nesting-depth-of-two-valid-parentheses-strings/)
* [Minimum Remove to Make Valid Parentheses (1249)](https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/)
* [Score of Parentheses (856)](https://leetcode.com/problems/score-of-parentheses/)