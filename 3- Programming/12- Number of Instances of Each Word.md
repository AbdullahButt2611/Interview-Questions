# Given a string, return a dictionary containing number of instances of each word

```python
def cal_instances(sentence):
    result = {}
    words = sentence.split()

    for word in words:
        if word in result:
            result[word] += 1
        else:
            result[word] = 1
    
    return result

# Example usage
sentence = 'The FurnitureShop represents the client code that orders furniture. It can switch between different styles (Modern or Victorian) by using the corresponding factory, and the client code remains independent of the specific classes used to create the furniture'
print(cal_instances(sentence))  
```