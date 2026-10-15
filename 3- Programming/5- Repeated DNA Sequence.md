##  Write a function to find all the 10-letter-long sequences (substrings) that occur more than once in a DNA molecule.
```
Example:
Input: s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
Output: ["AAAAACCCCC", "CCCCCAAAAA"]
```
`Eduucative`



You can implement this in Python using a simple function that iterates through the DNA sequence and checks for recurring 10-letter sequences. Here's one way to do it:

```python
def find_repeated_sequences(s):
    sequence_count = []
    repeated_sequences = []

    # Iterate through the string and count occurrences of 10-letter sequences
    for i in range(len(s) - 9):
        sequence = s[i:i+10]
        if sequence in sequence_count:
            repeated_sequences.append(sequence)
        else:
            sequence_count.append(sequence)

    return repeated_sequences

# Example usage:
s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
print(find_repeated_sequences(s))
```