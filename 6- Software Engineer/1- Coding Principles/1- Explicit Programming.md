# Explicit Programming

## In One Line

Explicit programming means you spell out the details yourself (types, conversions, intent) instead of letting the language guess them for you.

<br><br>

## What It Is

Every line of code has small details that someone has to decide: what type a value is, when to convert it, what a function should do by default. **Explicit programming** is when *you* state those details directly in the code. **Implicit programming** is when you let the language fill them in automatically using its own rules and defaults.

Explicit code is clear and predictable, but a little longer. Implicit code is short and quick to write, but it can do things behind your back that surprise you later.

<br><br>

## A Simple Analogy

Think of giving directions. Explicit is "drive 2 km, turn left at the petrol station, it is the third house." Implicit is "you know the way, just head over." The explicit version takes more words, but nobody gets lost. Implicit is faster to say, and works only if the other person already knows the route.

<br><br>

## Explicit vs Implicit at a Glance

| | Explicit | Implicit |
|---|---|---|
| Who decides the detail | you, written in the code | the language, automatically |
| Types | you declare them | inferred for you |
| Conversions | you convert on purpose | converted behind the scenes |
| Reads as | longer, very clear | shorter, sometimes surprising |
| Best for | critical or shared code | quick scripts, concise code |

<br>

## Examples

**1. Declaring a type**

```python
# Implicit: Python figures out the type
age = 25

# Explicit: you state the type yourself
age: int = 25
```

**2. Converting a type**

```javascript
// Implicit: JavaScript converts types on its own (coercion)
"5" + 3     // "53"  the 3 silently becomes text
"5" - 3     // 2     the "5" silently becomes a number

// Explicit: you convert on purpose, so there are no surprises
Number("5") + 3   // 8
```

**3. Default behavior**

```python
# Implicit: leans on a hidden default
def connect(timeout=30):   # the 30 is invisible at the call site
    ...

connect()            # what timeout? you cannot tell from here

# Explicit: the caller states what they want
connect(timeout=30)  # clear at a glance
```

<br>

## Why It Matters

- **Explicit** is easier to read, debug, and hand to a teammate, because nothing is hidden. The cost is a bit more typing.
- **Implicit** is shorter and faster to write, but the language's hidden choices (like type coercion) are a common source of bugs.

The goal is not to make everything explicit. It is to be explicit about the things that matter (types, conversions, important behavior) and let the language handle the boring, predictable parts.

<br><br>

## Key Takeaway

Explicit programming = you control the details and write them down. Implicit programming = the language decides for you. Be explicit when clarity matters, and lean on implicit only when it keeps simple code clean.