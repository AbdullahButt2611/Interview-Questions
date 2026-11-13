# What is a Lockfile For

## Question

What is a lockfile for? Should it be committed?

## Answer

<mark>A lockfile records the exact version of every installed package (including dependencies of dependencies), so every install produces the same node_modules. Yes, commit it.</mark>

<br><br>

### The Problem It Solves

```ini
package.json      "express": "^5.3.0"     <- a RANGE (>=5.3.0 <6.0.0)

Monday install    express 5.3.0
Friday install    express 5.4.1           <- new release, same package.json
```

- `package.json` lists **ranges**. Without a lockfile, two installs can get different code.
- Your direct dependencies have their own dependencies (transitive), often **hundreds** of packages. Any of them can change.

<br><br>

### What It Stores

```json
"node_modules/express": {
  "version": "5.3.0",
  "resolved": "https://registry.npmjs.org/express/-/express-5.3.0.tgz",
  "integrity": "sha512-..."
}
```

- **version**: the exact version installed.
- **resolved**: where it was downloaded from.
- **integrity**: a hash. If the downloaded file does not match, the install **fails** (tampering protection).
- Covers the **whole tree**, not just your direct dependencies.

<br><br>

### Why It Matters

- **Reproducible:** same versions on every laptop, CI and production.
- **Secure:** integrity hashes catch modified packages.
- **Reviewable:** dependency changes show up in the PR diff.
- **Faster:** no need to resolve ranges again.

<br><br>

### Lockfile per Tool

| Tool | Lockfile            | Frozen install                   |
| :--- | :------------------ | :------------------------------- |
| npm  | `package-lock.json` | `npm ci`                         |
| yarn | `yarn.lock`         | `yarn install --immutable`       |
| pnpm | `pnpm-lock.yaml`    | `pnpm install --frozen-lockfile` |
| bun  | `bun.lock`          | `bun install --frozen-lockfile`  |

<br><br>

### npm install vs npm ci

| Command       | Uses lockfile                       | Can change lockfile | Out of sync with package.json |
| :------------ | :---------------------------------- | :------------------ | :---------------------------- |
| `npm install` | Yes, but may update it              | Yes                 | Updates the lockfile          |
| `npm ci`      | Exactly, deletes node_modules first | **Never**           | **Fails** with an error       |

- Use `npm install` while developing, `npm ci` in CI and Docker.

<br><br>

### Should It Be Committed?

- **Applications: Yes, always.** It is what makes deploys reproducible.
- **Libraries: Yes, for your own dev and CI.** It is **not** published, so users of your library resolve their own versions.
- Never commit `node_modules`. Commit the lockfile instead.

<br><br>

### Key Points

- `package.json` = what you **allow**. Lockfile = what you **got**.
- Do not hand-edit it. On a merge conflict, fix `package.json`, then rerun the install.
- Use **one** package manager per project, so there is one lockfile.
- `npm-shrinkwrap.json` is a lockfile that **is** published with a package. Used for CLI tools, not libraries.

<br><br>

## Other Ways to Ask This Question

- What is `package-lock.json` and why does it exist?
- What is the difference between `npm install` and `npm ci`?
- Why do builds differ even when `package.json` did not change?
- Should a library commit its lockfile?
- How do you resolve a merge conflict in `package-lock.json`?
- What does the `integrity` field in a lockfile do?
