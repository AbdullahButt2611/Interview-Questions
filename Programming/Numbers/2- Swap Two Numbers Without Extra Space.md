# Swap Two Numbers Without Using Extra Space

`Pentaloop`

## Problem

Swap the values of **two numbers** without using any extra variable.

## Solution

You can use **arithmetic operations** to swap the numbers:

```python
x = 10
y = 20

# Step 1: Add x and y
x = x + y       # x = 30

# Step 2: Subtract y from new x to get original x
y = x - y       # y = 10

# Step 3: Subtract new y from x to get original y
x = x - y       # x = 20
```

✅ **Result:**

* `x = 20`
* `y = 10`

This method **does not use any extra variable** and successfully swaps the two numbers.
