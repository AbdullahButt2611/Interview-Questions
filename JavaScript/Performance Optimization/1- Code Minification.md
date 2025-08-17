## What is Code Minification in JavaScript?

**Code Minification is the process of removing unnecessary characters (like spaces, line breaks, comments, and long variable names) from source code without changing its functionality.** It is mainly used to **reduce file size and improve performance** (faster load times).

### **Example**

Original (readable):

```js
function add(a, b) {
  return a + b; // returns sum
}
```

Minified (smaller, but same result):

```js
function add(a,b){return a+b;}
```

✅ **Purpose:**

* Reduce file size
* Improve website performance
* Faster download and execution