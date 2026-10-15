# Calculate number of non numeric characters in a string using regular expressions? 
`Rolustech`

You can calculate the number of non-numeric characters in a string using regular expressions by first finding all matches of non-numeric characters and then counting the number of matches. Here's how you can do it in Python:

```python
import re

def count_non_numeric_chars(input_string):
    non_numeric_chars = re.findall(r'[^0-9]', input_string)
    return len(non_numeric_chars)

# Example usage:
input_string = "abc123def456ghi"
num_non_numeric_chars = count_non_numeric_chars(input_string)
print("Number of non-numeric characters:", num_non_numeric_chars)
```

In this code:

- `re.findall(r'[^0-9]', input_string)` finds all non-numeric characters in the input string.
- `len(non_numeric_chars)` returns the number of non-numeric characters found.