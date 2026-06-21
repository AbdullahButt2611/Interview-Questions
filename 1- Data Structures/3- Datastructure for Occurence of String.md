# Which Data Strcuture is used to find the occurence of a character in a string
`i2C`

To find the occurrence of a character in a string optimally, you can use a data structure called a hash table or a dictionary, depending on the programming language you're using.

In languages like Python or JavaScript, dictionaries (Python) or objects (JavaScript) are commonly used. The key-value pairs in these structures allow for efficient lookup of characters in constant time. Here's a simple example in Python:

```python
def char_occurrence(string):
    char_count = {}
    for char in string:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1

    return char_count

string_example = "example"
result = char_occurrence(string_example)
print(result)
```

In this example, the `char_occurrence` function uses a dictionary `(char_count)` to store the occurrences of each character in the string. The time complexity for checking whether a character is in the dictionary is generally O(1), making this approach efficient.

If you need to find the occurrence of a specific character, you can then look it up in the dictionary, and the count will be readily available.

Other languages may have similar data structures with different names, but the concept remains the same: a data structure that allows for efficient lookup based on the characters in the string.