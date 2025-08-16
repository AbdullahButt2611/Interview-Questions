## What is the purpose of "use strict"; in JavaScript?
`Turing - JavaScript`

---

The `"use strict";` directive in JavaScript is used to enable **Strict Mode**, which is a restricted version of JavaScript that helps you write cleaner, safer, and less error-prone code.

When you put `"use strict";` at the top of a file or a function, JavaScript executes in strict mode, which enforces stricter parsing and error handling rules.

### Key reasons why it's used:

1. **Eliminates some silent errors**

   * In non-strict mode, JavaScript sometimes fails silently. Strict mode converts these into actual errors.

   ```js
   "use strict";
   x = 10; // ❌ ReferenceError: x is not defined (in strict mode)
   ```

2. **Prevents use of reserved keywords**

   * Future reserved words like `implements`, `interface`, `private`, etc., cannot be used as variable names.

3. **Disallows accidental globals**

   * Variables must be declared with `let`, `const`, or `var`.
     Without strict mode:

   ```js
   function test() {
     a = 5; // creates a global variable accidentally
   }
   ```

   With strict mode:

   ```js
   "use strict";
   function test() {
     a = 5; // ❌ ReferenceError
   }
   ```

4. **Makes assignments safer**

   * Assignments to non-writable, getter-only, or undeclared properties throw an error.

   ```js
   "use strict";
   const obj = {};
   Object.defineProperty(obj, "x", { value: 42, writable: false });
   obj.x = 9; // ❌ TypeError
   ```

5. **Prevents `this` from defaulting to global object**

   * In non-strict mode:

     ```js
     function showThis() {
       console.log(this); // window (in browsers)
     }
     showThis();
     ```
   * In strict mode:

     ```js
     "use strict";
     function showThis() {
       console.log(this); // undefined
     }
     showThis();
     ```


✅ **In short:** `"use strict";` makes JavaScript behave more predictably, avoids bad practices, and improves security by catching common mistakes early.
