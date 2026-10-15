# Print all the divisors of the number

```pseudocode
import math

def print_divisors(n):
    divisors = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.append(i)  # Add the divisor
            if n // i != i:  # Add the paired divisor only if it's different
                divisors.append(n // i)
    
    divisors.sort()  # Sort the list of divisors
    return divisors

# Example usage:
n = 36
print(print_divisors(n))

```

> It's time complexity is `O(sqrt(n))`

### Common Problems
- GCD / HCF
- Prime numbers