# Flipping bits problem
### You will be given a list of 32 bit unsigned integers. Flip all the bits ( 0 -> 1 and 1 -> 0 ) and return the result as an unsigned integer.

`HackerRank`

<br>


```python
def flippingBits(n):
    return ~n & 0xFFFFFFFF
```
<br>

- The bitwise NOT operation (`~`) flips all the bits.
- Since we are dealing with unsigned 32-bit integers, the range is from `0` to `2^32 - 1`.
- To ensure that the result fits within 32 bits, we use a mask: `0xFFFFFFFF` (which is the maximum 32-bit value).