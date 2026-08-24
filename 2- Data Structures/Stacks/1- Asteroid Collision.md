# Asteroid Collision
`LeetCode 75`

## Problem Statement

You are given an array `asteroids` of integers.

* Each integer represents an asteroid.
* The **absolute value** represents the size of the asteroid.
* The **sign** represents the direction:

  * Positive (`+`) → moving right
  * Negative (`-`) → moving left
* All asteroids move at the same speed.

When two asteroids collide:

* The smaller asteroid explodes.
* If both asteroids have the same size, both explode.
* Asteroids moving in the same direction never meet.

Return the final state of the asteroids after all collisions.

## Examples

### Example 1

```
Input:  [5, 10, -5]
Output: [5, 10]
```

### Example 2

```
Input:  [8, -8]
Output: []
```

### Example 3

```
Input:  [10, 2, -5]
Output: [10]
```

## Constraints

* `1 <= asteroids.length <= 10^4`
* `-1000 <= asteroids[i] <= 1000`
* `asteroids[i] != 0`

<br><br>

## Approach 1: Direct Simulation (Inefficient)

### Idea

Simulate collisions by checking neighbors repeatedly until no more collisions happen.

### Steps

1. Scan the array.
2. If two adjacent asteroids can collide, resolve it.
3. Repeat until the array stops changing.

### Problem with this approach

* Requires many passes over the array.
* Becomes very slow for large inputs.

### Time Complexity

* Worst case: `O(n^2)`

Because of poor performance, this approach is not ideal.

<br><br>

## Approach 2: Stack Based Solution (Optimal)

### Core Idea

A collision only happens when:

* One asteroid moves right (`> 0`)
* The next asteroid moves left (`< 0`)

We use a stack to keep track of asteroids that are still alive.

### Algorithm

1. Create an empty stack.
2. Iterate through each asteroid:

   * Assume the current asteroid is alive.
   * While the stack is not empty **and** a collision is possible:

     * Compare sizes.
     * Remove the smaller asteroid.
     * If sizes are equal, remove both.
   * If the current asteroid survives, push it into the stack.
3. The stack represents the final state.

### Python Implementation

```python
def asteroidCollision(asteroids):
    stack = []

    for cur in asteroids:
        alive = True

        while stack and cur < 0 < stack[-1]:
            if abs(stack[-1]) < abs(cur):
                stack.pop()
                continue
            elif abs(stack[-1]) == abs(cur):
                stack.pop()
                alive = False
                break
            else:
                alive = False
                break

        if alive:
            stack.append(cur)

    return stack
```

### Explanation

* The stack stores asteroids that have not exploded.
* When a left-moving asteroid appears, it may collide with right-moving ones in the stack.
* Collisions are resolved immediately, so no extra passes are needed.

### Time Complexity

* `O(n)` — each asteroid is pushed and popped at most once.

### Space Complexity

* `O(n)` — stack space in the worst case.

<br><br>

## Final Notes

* The stack approach is the best solution for interviews.
* It is simple, fast, and handles all edge cases.
* This problem tests understanding of stack usage and collision rules.
