# Controlled vs. Uncontrolled Components in React
`Linkedin`
<br><br>

#### Sample Interview Question

> <br>“Can you explain the difference between controlled and uncontrolled components in React, including how each one works under the hood, and describe scenarios where you would choose one approach over the other?”
<br>

<br><br>


**In Simplest way**:  
- **Controlled Components** tie every form field’s value to React state.  
- **Uncontrolled Components** let the DOM manage its own state, accessed via refs.
<br><br>

### 1. Controlled Components  
- **How they work**  
  - You store the input’s current value in React state (e.g. via `useState`).  
  - You render the field with a `value={stateValue}` and update that state in an `onChange` handler.  
- **Why use them**  
  - **Single source of truth**: Your React state is always up to date with what’s on screen.  
  - **Validation & formatting**: You can veto or transform every keystroke (e.g. force uppercase, block invalid characters).  
  - **Easier testing**: You can snapshot or simulate state changes directly.  
  - **Dynamic inputs**: When one field’s value determines another’s options or visibility.  
- **Drawbacks**  
  - More boilerplate: `value` + `onChange` for every field.  
  - Potential performance hit if you have many high-frequency fields (e.g. very large forms).


### 2. Uncontrolled Components  
- **How they work**  
  - You render a normal `<input />` (no `value` prop).  
  - You attach a `ref` (via `useRef`) to the DOM node.  
  - You read `.current.value` on submit (or at any time) to get the latest value.  
- **Why use them**  
  - **Less code**: No need for state handlers on every keystroke.  
  - **Better for simple or legacy forms**: When you just need one-off reads, like file uploads or small forms with few fields.  
  - **Performance**: Avoids re-rendering React on every keystroke.  
- **Drawbacks**  
  - Harder to validate or transform input in real time.  
  - No immediate React-driven UI feedback on each change.  
  - Testing often requires simulating DOM events rather than inspecting state.


#### 3. When to Choose Which?  

| Scenario                               | Controlled                                    | Uncontrolled                              |
|----------------------------------------|-----------------------------------------------|--------------------------------------------|
| **Complex form logic**                 | ✔︎ instant validation, conditional fields     |                                            |
| **Simple, static form**                |                                               | ✔︎ quick setup, minimal code               |
| **Performance-sensitive inputs**       |                                               | ✔︎ avoids frequent re-renders              |
| **Need to sync value elsewhere**       | ✔︎ e.g. live previews, other components’ UI   |                                            |
| **Legacy code or quick prototypes**    |                                               | ✔︎ fits DOM-centric patterns               |

