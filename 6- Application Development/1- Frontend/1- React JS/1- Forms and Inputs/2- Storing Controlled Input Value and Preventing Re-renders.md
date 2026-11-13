# Controlled Input: Where to Store the Value and How to Prevent Excessive Re-renders

`Amazon` • `Flipkart` • `Accenture` • `Cognizant` • `Infosys` • `Wipro` • `micro1`

## Question

In a controlled input, where would you store the current value (component state, a reducer, or a form library store)?

And how do you prevent excessive re-renders when a large form updates on every keystroke?

<br><br>

## Answer

### The core problem first

In a controlled input, every keystroke updates state, and updating state makes React re-render.

- On a **small form**, that is totally fine.
- On a **large form**, re-rendering the whole thing on every letter can make typing feel slow.

So the question is really two things: where do you keep the value, and how do you stop the entire form from re-rendering on every key press.

<br><br>

### Part 1: Where do you store the value?

There are three choices, and the right one depends on how big and complex the form is.

**Option A: Component state (`useState`)**

- Best for **small, simple forms** (login, contact, search).
- Each field lives in `useState`, either one per field or one object for all of them.
- Quick and easy to set up.
- Trade-off: every keystroke re-renders this component, which is fine when the form is small.

```jsx
const [email, setEmail] = useState("");

<input value={email} onChange={(e) => setEmail(e.target.value)} />
```

**Option B: Reducer (`useReducer`)**

- Best for **medium to complex forms**, where fields depend on each other or the update logic gets messy (multi-step, conditional fields, lots of validation).
- All the "how state changes" logic sits in one place (the reducer), so it stays organized instead of being scattered across many `useState` calls.
- It still re-renders on updates, but the logic is far cleaner to maintain.

```jsx
const [state, dispatch] = useReducer(formReducer, initialState);

<input
  value={state.email}
  onChange={(e) => dispatch({ type: "email", value: e.target.value })}
/>
```

**Option C: Form library store (React Hook Form, Formik)**

- Best for **large forms** with many fields and heavy validation.
- A library like React Hook Form keeps the values in its own store (using refs, outside React's normal render cycle), so typing does not re-render the whole form.
- This is the option that actually solves the performance problem at scale.

<mark>Rule of thumb: small form uses useState, complex update logic uses useReducer, and a large performance-sensitive form uses a form library like React Hook Form.</mark>

<br><br>

### Part 2: How do you stop excessive re-renders on a big form?

The problem again: value in state, plus typing, equals a re-render on every keystroke, and a big tree makes that slow. Here are the fixes, strongest first.

**1. Use a form library (React Hook Form), the biggest win**

- It uses uncontrolled inputs under the hood and only re-renders the one field that changed, not the entire form.

**2. Split state into small components (isolate the re-render)**

- Instead of one giant component holding every value, give each input its own tiny component with its own state.
- Then a keystroke only re-renders that one small input, not the whole form.

```jsx
function Field({ label }) {
  const [value, setValue] = useState(""); // state lives HERE, not in the parent

  return <input value={value} onChange={(e) => setValue(e.target.value)} />;
}
```

**3. Go uncontrolled where you can**

- If a field only needs its value at submit time, use `defaultValue` and read it with a `ref` instead of tracking every keystroke.

**4. Debounce the expensive work**

- Debouncing does not stop re-renders, but it stops heavy side effects (API calls, filtering, live validation) from firing on every letter. You wait until the user pauses typing.

**5. Memoize children and handlers**

- Use `React.memo` on child components, `useCallback` for the onChange handlers, and `useMemo` for derived values, so the parts of the form that did not change do not re-render for nothing.

<br><br>

### Quick decision guide

| Situation | Where to store the value | Main re-render fix |
|-----------|--------------------------|--------------------|
| Small, simple form | `useState` | Nothing needed |
| Complex update logic | `useReducer` | Split components, memoize |
| Large, many fields | Form library store (React Hook Form) | Library handles it (field-level renders) |
| Value only needed on submit | DOM via `ref` (uncontrolled) | No per-keystroke render at all |

<br><br>

### The one-line mental model

Either move the state **closer to the input** so fewer things re-render (split components), or move the value **out of React's render cycle entirely** (a form library, or uncontrolled with refs). Then use debouncing and memoization to trim the leftover expensive work.

<br><br>

## What to Say in the Interview

Keep it simple and structured. Here is the easy words version you can say out loud:

> "It depends on the form's size. For a small form I keep the value in **component state** with `useState`. When the update logic gets complex or fields depend on each other, I move to a **reducer** with `useReducer` so all the logic is in one place. For a large form with lots of fields, I use a **form library like React Hook Form**, which stores the values in its own store using refs, so typing does not re-render everything.
>
> To stop excessive re-renders on a big form, the biggest win is a form library, because it only re-renders the field that changed. Beyond that, I **split the form into small components** so each keystroke only re-renders one input, use **uncontrolled inputs with refs** for fields I only need at submit, **debounce** heavy work like API calls or validation, and **memoize** children and handlers with `React.memo`, `useCallback`, and `useMemo`."