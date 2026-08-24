# Why Is Python Called a Multi Paradigm Programming Language?

`Google` • `Meta` • `Intel`

## Question
Why is Python called a multi paradigm programming language, and what exactly does "multi paradigm" mean?

<br><br>

## Answer

### What Is a Programming Paradigm?
A programming paradigm is a style or approach to writing and organizing code. It is essentially a philosophy for how you model problems and structure your solution.

- Some paradigms organize code around step by step procedures.
- Others organize code around objects that hold both data and behavior.
- Others treat computation as the evaluation of mathematical functions.

Each paradigm gives you a different set of mental tools for expressing logic.

<br><br>

### What Does "Multi Paradigm" Mean?
"Multi paradigm" simply means a language supports more than one of these styles. You are not locked into a single way of thinking, so you can:

- Mix and match different styles within the same program.
- Choose whichever approach best fits the problem in front of you.
- Blend several paradigms together when that produces the clearest code.

<br><br>

### Why Python Qualifies as Multi Paradigm
Python comfortably supports several paradigms, which is why it earns the label. The three most common are described below.

<br><br>

#### 1. Procedural (Imperative) Programming
- Code is written as a sequence of statements that run in order.
- Reusable logic is grouped into functions.
- This is often the first style beginners learn.

```python
def greet(name):
    print("Hello", name)

greet("Sam")
```

<br><br>

#### 2. Object Oriented Programming (OOP)
- Data (attributes) and behavior (methods) are bundled together into objects.
- Built on classes, inheritance, encapsulation, and polymorphism.
- Useful for modeling real world entities.

```python
class Dog:
    def __init__(self, name):
        self.name = name

    def bark(self):
        print(self.name, "says woof")

Dog("Rex").bark()
```

<br><br>

#### 3. Functional Programming
- Functions are first class citizens (they can be passed around and returned from other functions).
- Favors pure functions and tools like map, filter, lambda, and comprehensions.
- Note that Python supports this only partially (it does not enforce immutability).

```python
nums = [1, 2, 3, 4]
squares = list(map(lambda x: x * x, nums))
```

<br><br>

### Key Takeaway
- Python does not force any single paradigm on you.
- A single script can freely combine classes, standalone functions, and functional tools.
- Languages like C are primarily procedural and older Java was primarily object oriented, but Python deliberately gives you the freedom to move between styles.
- That flexibility is exactly what earns Python the "multi paradigm" label.
