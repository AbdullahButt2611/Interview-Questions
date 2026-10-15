# Reverse a number and If there are trailing zeroes ignore them.
> If a number is 10400, the reverse will be 401

```python
num = 10400
reverse_num = 0
while num > 0:
    last_digit = num % 10
    num = num // 10
    reverse_num = (reverse_num * 10) + last_digit
```