# Deciding Between Local Component State and Global State (Context / Redux)

`Amazon` • `Flipkart` • `Accenture` • `Cognizant` • `Infosys` • `micro1`

## Question

In React, how do you decide what belongs in local component state versus global state (Context / Redux), especially to avoid unnecessary re-renders across the app?

<br><br>

## Answer

### The core idea

Every piece of state has a "home." The real question is: does this state belong to **one component** (local), or does it need to be **shared across many components** (global)?

The trap is that people dump too much into global state (Context or Redux), and then every time that global state changes, everything reading it re-renders, even the parts that did not care about the change. That is exactly what causes unnecessary re-renders across the app.

<mark>Golden rule: keep state as local as possible, and only lift it up to global when multiple distant components genuinely need it.</mark>

<br><br>

### The simple test to decide

Ask one question: **who needs this piece of state?**

- Only this component needs it → **local** (`useState` / `useReducer`).
- A few nearby components need it → **lift it up** to the closest shared parent and pass it down as props.
- Many components far apart in the tree need it → **global** (Context or Redux).

<br><br>

### What belongs in LOCAL state

Things that only matter inside one component:

- Whether a dropdown or modal is open.
- The current text in an input field.
- A "show password" toggle, a hover state, or a loading spinner for one button.
- Which tab is active inside one widget.

If no other component cares about it, it stays local. This is the default choice. Keeping fast-changing things (like text being typed) local is also what prevents most re-render problems, since it never touches the rest of the app.

<br><br>

### What belongs in GLOBAL state

Things that many unrelated parts of the app need to read or change:

- The logged-in user / auth status.
- Theme (dark or light mode).
- Language / locale.
- Shopping cart contents.
- App-wide notifications.

These are needed "everywhere," so passing them through props (prop drilling) would be painful, and global state is the cleaner choice.

A key point: global state should hold things that are **shared and relatively stable**, not things that change on every keystroke. Fast-changing values in a shared Context are dangerous, because when a Context value changes, every component reading that context re-renders.

<br><br>

### The one-line mental model

Start local, lift only when sharing is truly needed, and keep anything that changes rapidly out of shared global state, because global state is for things that are shared and stable, not for things that change on every keystroke.

<br><br>

## What to Say in the Interview

Keep it simple and structured. Here is the easy words version you can say out loud:

> "The way I decide is by asking one question: **who needs this piece of state?**
>
> If only one component needs it, I keep it **local** with `useState` or `useReducer`. Things like whether a dropdown is open, the text in an input, or a loading spinner for one button all stay inside that component.
>
> If a few nearby components need it, I do not jump to global. I just **lift the state up** to their closest shared parent and pass it down as props.
>
> I only reach for **global state**, like Context or Redux, when many components far apart in the tree genuinely need the same data, like the logged-in user, the theme, the language, or the shopping cart. These are needed everywhere, so passing them through props would be painful.
>
> My default is to keep state **as local as possible** and only lift it when sharing is really needed. The main thing I am careful about is that global state should hold things that are **shared and fairly stable, not things that change on every keystroke**, because when a Context value changes, every component reading that context re-renders. Keeping those fast-changing values local is what avoids the unnecessary renders."

<br><br>

**Super short version (if you want to keep it quick):**

> "I decide based on who needs the state. If one component needs it, it stays local with `useState`. If a few nearby components need it, I lift it up and pass props. I only use global state like Context or Redux for things many distant components share, like auth, theme, or the cart. And I keep fast-changing values out of global state, because a Context change re-renders every consumer, which is what causes unnecessary renders across the app."