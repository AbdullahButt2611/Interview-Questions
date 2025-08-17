## What is Throttling in JavaScript?
`Turing  - JavaScript`

**Throttling in JavaScript (and web development in general) is a technique used to control the rate at which a function is executed.** It ensures that even if an event (like `scroll`, `resize`, or `mousemove`) is triggered multiple times very quickly, the function will only run at fixed intervals.

### **Example**

Without throttling:

```js
window.addEventListener("scroll", () => {
  console.log("Scroll event fired"); 
});
```

👉 This may run **hundreds of times per second**, causing performance issues.

With throttling:

```js
function throttle(func, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  }
}

window.addEventListener("scroll", throttle(() => {
  console.log("Throttled scroll event");
}, 1000));
```

👉 Now the function runs **once every 1 second**, no matter how often you scroll.

✅ **Purpose:**

* Improve performance
* Prevent unnecessary function calls
* Commonly used for events like **scrolling, resizing, keypresses, and mouse movements**