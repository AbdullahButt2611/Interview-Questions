# node --watch

## Question

What does `node --watch` do, and would you use it for `dev`?

```json
"scripts": {
  "dev": "node src/index.js"
}
```

## Answer

<mark>node --watch restarts the process automatically when the entry file or anything it imports changes. Yes, use it for dev. It replaces nodemon with zero dependencies.</mark>

```bash
node --watch src/index.js
```

<br><br>

### How It Works

```ini
1. Node starts src/index.js
2. Watches index.js + every file it imports (the module graph)
3. You save a file -> Node stops the process -> starts it again
```

- Built into Node. Experimental in Node 18, **stable since Node 22**.
- Only watches files that are **imported**. Files read with `fs` (JSON, templates) or `.env` are not watched unless you use `--watch-path`.

<br><br>

### Useful Flags

| Flag                      | What it does                                         |
| :------------------------ | :--------------------------------------------------- |
| `--watch`                 | Restart on changes to the entry file and its imports |
| `--watch-path=./src`      | Watch a specific folder instead of the module graph  |
| `--watch-preserve-output` | Do not clear the console on restart                  |

<br><br>

### Would You Use It for `dev`?

**Yes.** The current script needs a manual restart after every change.

```json
"scripts": {
  "dev": "node --watch --env-file=.env src/index.js",
  "start": "node src/index.js"
}
```

- `dev` for local work, `start` for production.
- `--env-file=.env` also replaces the `dotenv` package (Node 20.6+).

<br><br>

### node --watch vs nodemon

| Aspect          | `node --watch`          | nodemon                             |
| :-------------- | :---------------------- | :---------------------------------- |
| Install         | None, built in          | Extra devDependency                 |
| Config          | A few CLI flags         | `nodemon.json`: ext, ignore, delay  |
| Non-JS files    | Only via `--watch-path` | Any extension (`.json`, `.graphql`) |
| Old Node (< 18) | Not available           | Works                               |

- Default to `node --watch`. Keep nodemon only if you need its extra config.
- For TypeScript, use `tsx watch` or Node's built-in type stripping.

<br><br>

### Never in Production

- Restarts on any file change. Production files should not change.
- Production restarts are handled by **Docker**, **Kubernetes**, **systemd** or **PM2**.

<br><br>

### Key Points

- `--watch` = auto-restart on file change, dev only.
- Every restart **reconnects** to Redis and Mongo, so connect-at-boot code runs each time.
- Restart sends `SIGTERM`, so graceful shutdown handlers also get exercised during dev.

<br><br>

## Other Ways to Ask This Question

- Do you still need nodemon in modern Node.js?
- How do you auto-restart a Node.js server on file changes?
- What is the difference between `dev` and `start` scripts?
- Why does my server not restart when I edit a JSON or `.env` file?
- How do you load a `.env` file without the `dotenv` package?
