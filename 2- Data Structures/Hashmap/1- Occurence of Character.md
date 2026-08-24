## Optimal Data Structure for Finding Occurrence of a Character in a String
`I2C`

The optimal data structure for finding the occurrence of a character in a string would typically be a hashmap (or dictionary in some languages), where the characters are stored as keys, and their corresponding frequencies (occurrences) are stored as values.

Here's how you could implement it in Python:

```python
def char_occurrences(string):
    occurrences = {}
    for char in string:
        if char in occurrences:
            occurrences[char] += 1
        else:
            occurrences[char] = 1
    return occurrences

# Example usage:
my_string = "hello"
print(char_occurrences(my_string))  # Output: {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

Using a hashmap allows you to achieve a time complexity of O(n) for finding the occurrences of characters in a string, where n is the length of the string. This is because accessing elements in a hashmap typically has an average-case time complexity of `O(1)`.