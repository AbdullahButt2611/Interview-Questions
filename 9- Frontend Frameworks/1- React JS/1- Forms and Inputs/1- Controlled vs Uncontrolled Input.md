# Controlled vs Uncontrolled Form Input in React

`Accenture` • `Cognizant` • `Infosys` • `Wipro` • `TCS` • `Amazon` • `Flipkart` • `micro1`

## Question

What is the difference between Controlled and Uncontrolled form input in React.js, and when would you choose one over the other in production?

<br><br>

## Answer

### The core idea

Think of a form input (like a text box). The big question is: **who is in charge of remembering what the user typed?**

- **Controlled input** → React is in charge (it stores the value in state).
- **Uncontrolled input** → the browser/DOM is in charge (the input remembers its own value, like a normal HTML form).

<br><br>

### Easy analogy

Imagine writing on a whiteboard.

- **Controlled:** Every time you write a letter, you also copy it into your notebook. Your notebook (React state) is the "official truth." The whiteboard just shows what the notebook says.
- **Uncontrolled:** You just write on the whiteboard and read it later when you need it. You do not copy anything down as you go.

<br><br>

### Controlled input (React holds the value)

```jsx
function MyForm() {
  const [name, setName] = useState("");

  return (
    <input
      value={name}                              // value comes FROM state
      onChange={(e) => setName(e.target.value)} // every keystroke updates state
    />
  );
}
```

What is happening:

- The input shows whatever `name` currently is.
- Every keystroke fires `onChange`, updates state, and re-renders.
- React always knows the current value at any moment.

<br><br>

### Uncontrolled input (DOM holds the value)

```jsx
function MyForm() {
  const inputRef = useRef();

  const handleSubmit = () => {
    console.log(inputRef.current.value); // read the value only when needed
  };

  return (
    <>
      <input ref={inputRef} defaultValue="" />
      <button onClick={handleSubmit}>Submit</button>
    </>
  );
}
```

What is happening:

- React does not track keystrokes.
- You grab the value only when you need it (usually on submit) using a `ref`.
- Note it uses `defaultValue`, not `value`.

<br><br>

### Quick comparison

| Thing | Controlled | Uncontrolled |
|-------|-----------|--------------|
| Who stores the value | React state | The DOM |
| Reads value | Anytime (from state) | Only when you ask (via ref) |
| Re-renders on typing | Yes | No |
| Live validation / formatting | Easy | Hard |
| Code amount | More | Less |

<br><br>

### When to choose which (in production)

**Choose Controlled when (this is the default most of the time):**

- You need live validation (show an error as the user types).
- You need to format input while typing (phone numbers, currency, uppercase).
- One field's value should affect another (enabling a button, or a search box filtering a list).
- You want the value tied to other state or sent to a parent component.

**Choose Uncontrolled when:**

- The form is simple and you only need the value once on submit (like a basic login form).
- You are integrating with non-React code or a third-party library that manages the DOM.
- You want a file input (`<input type="file">` is almost always uncontrolled, since its value is read-only for security).
- You care about performance with a huge number of fields and do not need per-keystroke tracking.

<mark>Rule of thumb: default to Controlled because it gives you full control and predictability. Reach for Uncontrolled only when you specifically want the DOM to manage things or you need to avoid extra re-renders.</mark>

One extra note for real projects: many teams do not hand-roll all this. Libraries like `React Hook Form` actually lean on the `uncontrolled approach under the hood` to reduce re-renders, while still giving you validation, which is a nice middle ground.

<br><br>

## What to Say in the Interview

> "The main difference is: **who remembers what the user typed?**
>
> In a **controlled input**, React remembers it. The typed value is saved in state, the box shows whatever is in that state, and every time the user types, it updates that state. So React always knows the current value.
>
> In an **uncontrolled input**, the input box remembers it by itself, just like a normal HTML form. React does not watch every letter. I only go and grab the value when I actually need it, usually when the user hits submit, using a ref.
>
> For **when to use which**: most of the time I go with **controlled**, because when React always knows the value, it is easy to check for errors while the user types, show or hide things based on what they enter, or fix the formatting as they go.
>
> I would use **uncontrolled** when the form is really simple and I just need the value once at submit, or for a file upload box, or when I am working with some non-React code that already handles the input."

<br>

**Super Short Version:**

> "Controlled means React remembers the value in state and updates it on every keystroke, so it always knows the current value. Uncontrolled means the input box remembers its own value and I only read it when needed using a ref. I usually go with controlled because it makes live validation and dynamic behavior easy, and use uncontrolled for simple forms or file inputs."