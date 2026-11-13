# dependencies vs devDependencies

## Question

What is the difference between `dependencies` and `devDependencies`?

## Answer

<mark>dependencies are needed to run the app in production. devDependencies are only needed to develop, test or build it.</mark>

```json
{
  "dependencies": {
    "express": "^5.3.0",
    "ioredis": "^6.0.0",
    "mongoose": "^9.11.3"
  },
  "devDependencies": {
    "eslint": "^9.0.0",
    "vitest": "^3.0.0",
    "typescript": "^5.0.0"
  }
}
```

<br><br>

### Comparison

| Aspect                         | dependencies               | devDependencies                    |
| :----------------------------- | :------------------------- | :--------------------------------- |
| Needed when                    | App is **running**         | Coding, testing, building          |
| Examples                       | express, ioredis, mongoose | eslint, jest, typescript, @types/* |
| Add with                       | `npm i express`            | `npm i -D eslint`                  |
| `npm install` (local)          | Installed                  | Installed                          |
| `npm install --omit=dev`       | Installed                  | **Skipped**                        |
| Your package used as a library | Installed for the user     | **Not installed** for the user     |

<br><br>

### Production Install

```bash
npm install --omit=dev    # npm 7+
npm ci --omit=dev         # clean install from lockfile, best for Docker / CI
bun install --production  # Bun equivalent
```

- Also skipped automatically when `NODE_ENV=production`.
- Result: smaller `node_modules`, smaller Docker image, fewer packages to attack.

<br><br>

### Common Mistake

- A runtime package placed in `devDependencies`:
  - Works locally (`npm install` installs everything).
  - **Crashes in production**: `Error: Cannot find module 'express'`.
- Rule: if the code `import`s it at runtime, it belongs in **dependencies**.

<br><br>

### Build Step Gotcha

- With TypeScript or a bundler, the build needs devDependencies (`tsc`, `vite`).
- Install **all** packages to build, then `--omit=dev` for the final run image (Docker multi-stage build).

<br><br>

### Key Points

- dependencies = **run time**, devDependencies = **dev time**.
- The split matters most for **libraries** published to npm and for **lean production images**.
- Both are recorded in the lockfile.
- Related: `peerDependencies` (the host app must provide it, e.g. `react` for a React plugin), `optionalDependencies` (install failure is allowed).

<br><br>

## Other Ways to Ask This Question

- What does `npm install -D` / `--save-dev` do?
- How do you install only production dependencies?
- Why does my app work locally but fail with "Cannot find module" in production?
- Where should `typescript` and `@types/*` go in package.json?
- What are `peerDependencies`?
- How do you keep a Node.js Docker image small?
