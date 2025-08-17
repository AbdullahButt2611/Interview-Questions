## What is Debouncing in JavaScript?
`Turing - JavaScript`

**Debouncing is a programming technique used to delay the execution of a function until after a specified time has passed since the last time the event was triggered.** It ensures the function only runs once, even if the event is triggered multiple times quickly.

### **Example**

Without debouncing:

```js
const search = () => console.log("API Call");
document.getElementById("input").addEventListener("keyup", search);
```

👉 Every keystroke triggers an API call (bad for performance).

With debouncing:

```js
function debounce(func, delay) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), delay);
  }
}

const search = () => console.log("API Call");
document.getElementById("input").addEventListener("keyup", debounce(search, 500));
```

👉 The function will run **only once, 500ms after typing stops**.

✅ **Purpose:**

* Prevents unnecessary repeated function calls
* Improves performance
* Commonly used in **search boxes, form validations, window resizing, and autocomplete**
