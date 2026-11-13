# Difference Between `unknown` and `any` in TypeScript

`Micro1` • `Zara` • `Microsoft` • `Google` • `Airbnb` • `Netflix`

## Question

What is the difference between `unknown` and `any` in TypeScript, and when should you use each one?

<br><br>

## Answer

### 1. The Short Answer

Both `any` and `unknown` can **hold any value**. The difference is what TypeScript lets you **do** with that value afterwards.

- **`any`** turns type checking **off**
- **`unknown`** keeps type checking **on**, and forces you to prove the type before using it

<mark>unknown is the type-safe version of any. It accepts anything, but trusts nothing.</mark>

<br><br>

### 2. How `any` Behaves

Once a value is `any`, TypeScript stops asking questions. Anything you write compiles, and mistakes only show up at runtime.

```typescript
let a: any = "hello";

a.toFixed(2);       // No compile error, but CRASHES at runtime
a.foo.bar.baz;      // Still no complaint from TypeScript
let n: number = a;  // Freely assignable to any other type
```

You have written TypeScript, but you have the safety of plain JavaScript.

<br><br>

### 3. How `unknown` Behaves

`unknown` also accepts any value, but it **blocks you from using it** until you narrow it down to a real type.

```typescript
let u: unknown = "hello";

u.toFixed(2);       // Error: 'u' is of type 'unknown'
let n: number = u;  // Error: not assignable to number

// Narrow it first, then TypeScript allows the operation
if (typeof u === "string") {
  u.toUpperCase();  // Works, TypeScript now knows u is a string
}
```

Narrowing is done with `typeof`, `instanceof`, or a custom type guard.

<br><br>

### 4. Side by Side

| Behaviour | `any` | `unknown` |
|---|---|---|
| Can hold any value | Yes | Yes |
| Can access properties or call methods | Yes (unchecked) | No, until narrowed |
| Assignable **to** other types | Yes, to anything | Only to `unknown` and `any` |
| Type safety | Turned off | Preserved |
| Errors caught at | Runtime | Compile time |

<br><br>

### 5. When to Use Which

**Use `unknown`** for values whose shape you do not control:

- API and `fetch` responses
- `JSON.parse()` output
- The error in a `catch (e)` block
- User input or third party data

```typescript
async function getUser(): Promise<unknown> {
  const res = await fetch("/api/user");
  return res.json();   // We do not actually know the shape yet
}
```

**Use `any`** only as an escape hatch, knowing you are giving up safety:

- An untyped third party library
- A gradual migration from JavaScript to TypeScript
- A quick prototype where types are not settled yet

<mark>Rule of thumb: reach for unknown by default. It forces you to check the value before trusting it, which is exactly the check that any silently skips.</mark>

<br><br>

## Related Questions

- What is the `never` type, and how is it different from `void`?
- What are **type guards**, and how do you write a custom one?
- What does **type narrowing** mean in TypeScript?
- What is the difference between `interface` and `type`?
- What does the `strict` mode in `tsconfig.json` actually turn on?
- What is a **type assertion** (`as`), and why is it risky?
- How do you safely type an API response in TypeScript?