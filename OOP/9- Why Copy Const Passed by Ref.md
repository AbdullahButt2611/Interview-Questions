# Why Copy Constructor is Passed by Reference


In object-oriented programming languages like C++, a copy constructor is a special constructor that creates a new object by copying the values of another object of the same class. The copy constructor can be called in various situations, such as when an object is passed by value to a function, returned from a function, or explicitly used to create a new object.

When it comes to passing objects to functions, there are `two common ways` to pass them: by value and by reference. But we'll only discuss the Reference Approach

### Passing by Reference:

- In this approach, a reference to the original object is passed to the function.
- No new object is created, and the function works directly with the original object.
- This can be more efficient than passing by value, especially for large objects, as it avoids unnecessary copying.

```cpp
void myFunction(const MyClass &obj) {
    // Code here
}

MyClass mainObj;
myFunction(mainObj);  // No copy constructor is called, and the function works with mainObj directly
```