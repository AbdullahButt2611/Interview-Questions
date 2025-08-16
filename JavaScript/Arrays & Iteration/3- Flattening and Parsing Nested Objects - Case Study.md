## Flattening and parsing nested sensor readings in JavaScript

You are getting sensor readings from a temperature sensor in degree celsius and you need to convert them to Fahrenheit. How would you parse those readings in JS replacing ?? so that the line below it will be able to convert those values to Fahrenheit?

> Assumption: Fahrenheit = Temperature in degree celsius * 2;

```js
const sensorReading = [1, 2, 3, [null, 5, [4, 10], 89, "20", , [
    [
        [
            [, "96"]
        ]
    ]
]]];

function convert() {
    ??
    const mapped = flatArray.map((temperature) => temperature * 2);
    console.log(mapped);
}
convert();
```

`Turing - JavaScript`

---

Alright — the goal is to **flatten** and **parse** the `sensorReading` array so that we can multiply all numeric values by 2 for the fake "Celsius to Fahrenheit" formula.

### Step-by-step thinking

1. **`sensorReading`** contains:

   * Nested arrays (deeply nested)
   * Strings (`"20"`, `"96"`)
   * Nulls
   * Empty slots
2. We need to:

   * Flatten completely (`Infinity` depth).
   * Filter out **non-numeric** values except those that can be parsed into numbers.
   * Parse strings into numbers.
3. `Array.prototype.flat(Infinity)` is perfect for deep flattening.
4. Then use `.filter()` + `.map()` to clean and parse.

### Implementation

```javascript
function convert() {
  const flatArray = sensorReading
    .flat(Infinity)                         // Flatten deeply
    .filter(v => v !== null && v !== undefined && v !== "") // Remove null/empty
    .map(Number)                             // Convert to numbers
    .filter(v => !isNaN(v));                  // Remove NaN

  const mapped = flatArray.map((temperature) => temperature * 2);
  console.log(mapped);
}
```

### How this works

* `.flat(Infinity)` turns
  `[1, 2, 3, [null, 5, [4, 10], 89, "20", , [[[[, "96"]]]]]]`
  into
  `[1, 2, 3, null, 5, 4, 10, 89, "20", undefined, "96"]`
* `.map(Number)` converts `"20"` → `20`, `"96"` → `96`.
* `.filter(v => !isNaN(v))` removes non-numeric junk.
* Then multiplication works fine.

✅ **Output with given data:**

```
[ 2, 4, 6, 10, 8, 20, 178, 40, 192 ]
```
