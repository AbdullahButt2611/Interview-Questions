# Lockfile and Runtime Mismatch

## Question

There's a `bun.lock`, but the `dev` script runs `node`. What can go wrong?

```json
{
  "scripts": {
    "dev": "node src/index.js"
  }
}
```

```ini
project/
  bun.lock          <- installed with Bun
  package.json      <- "dev": "node ..."  (runs on Node)
```

## Answer

<mark>Bun installs, Node runs. That combo can work, but the team has no single source of truth: npm users ignore bun.lock and get different versions, and code may behave differently between Bun and Node.</mark>

<br><br>

### Package Manager vs Runtime

| Role            | Options              | Here                    |
| :-------------- | :------------------- | :---------------------- |
| Package manager | npm, pnpm, yarn, bun | **bun** (`bun.lock`)    |
| Runtime         | node, bun, deno      | **node** (`dev` script) |

- `bun install` + `node` runtime is a **valid** setup. The risk is that nobody wrote that down.

<br><br>

### What Can Go Wrong

**1. Different versions per developer**

- A teammate runs `npm install`. npm **ignores `bun.lock`**.
- It resolves fresh versions inside `^` ranges (`express ^5.3.0` can become `5.4.x`).
- Now two lockfiles (`bun.lock` + `package-lock.json`) drift apart. "Works on my machine."

**2. CI / Docker breaks**

- `npm ci` **fails** without a `package-lock.json`.
- A `node:` base image has no Bun, so it cannot do a frozen install from `bun.lock`.

**3. `bun run dev` still runs Node**

- `bun run dev` executes the script as written: `node src/index.js`.
- Developer thinks they are on Bun, but the app runs on **Node**. (Only `bun --bun run dev` forces Bun.)

**4. Bun-only behavior silently missing**

- **`.env` loading:** Bun loads `.env` automatically, Node does not. `process.env.REDIS_URL` is set under Bun and `undefined` under Node.
- **Bun APIs:** `Bun.serve`, `bun:sqlite` and other Bun globals crash under Node.

**5. Install script differences**

- Bun does not run dependency `postinstall` scripts unless the package is trusted (`trustedDependencies`). npm runs them. Native packages can behave differently.

<br><br>

### Fix: Pick One Tool and Make It Explicit

```jsonc
// Option A: Bun all the way
"scripts": { "dev": "bun --watch src/index.js" }
// CI: bun install --frozen-lockfile

// Option B: npm + Node all the way (delete bun.lock, commit package-lock.json)
"scripts": { "dev": "node --watch --env-file=.env src/index.js" }
// CI: npm ci
```

- Commit **one** lockfile only. Delete the other.
- CI and Docker must use the **same** tool as local dev.
- Note the choice in the README.

<br><br>

### Key Points

- **Package manager** (installs) and **runtime** (executes) are separate choices.
- A lockfile only helps if **everyone uses the tool that reads it**.
- Mixing tools silently is what breaks reproducibility, not the tools themselves.

<br><br>

## Other Ways to Ask This Question

- Can you use Bun as a package manager and Node as the runtime?
- What happens if a project has both `bun.lock` and `package-lock.json`?
- Why does `npm ci` fail in my pipeline?
- Does `bun run` use Bun or Node to execute scripts?
- Why is `process.env` empty when I switch from Bun to Node?
- How do you enforce one package manager across a team?
