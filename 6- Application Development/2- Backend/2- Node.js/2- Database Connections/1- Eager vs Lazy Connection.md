# Eager vs Lazy Database Connection

## Question

The Redis client is created at startup, but Mongo connects inside the route. What are the trade-offs?

```js
const redis = new Redis(process.env.REDIS_URL || "redis://localhost:6379");   // at startup

app.get("/mongo", async (req, res) => {
  if (mongoose.connection.readyState === 0) {
    await mongoose.connect(url);                                              // inside the route
  }
  res.json({ mongo: "Connected", database: mongoose.connection.name });
});

app.listen(3000);
```

## Answer

<mark>Eager (at startup) catches problems before traffic arrives and keeps requests fast. Lazy (in the route) lets the app boot without the DB, but slows the first request, hides failures and can race.</mark>

- Best practice: **connect once at boot, fail fast, then start listening.**

<br><br>

### Eager Connection (Redis here)

**Pros**

- Connection is ready (or failing) **before** users hit the app.
- Bad URL, wrong password or DB down is caught **at deploy time**.
- One shared client, reused by every request.

**Cons**

- App **cannot start** if the DB is down. Needs retries or an orchestrator restart.
- Slightly slower boot.

<br><br>

### Lazy Connection (Mongo here)

**Pros**

- App boots even if Mongo is down.
- No connection cost if the route is never called.

**Cons**

- **First request is slow**: it pays the full connect time (up to 30s on a bad host).
- **Failures are hidden**: the server says "running", but the DB is broken until someone calls `/mongo`.
- **Race condition** on a cold start:

```ini
Request A: readyState 0 -> calls connect() -> readyState becomes 2 (connecting)
Request B: readyState 2 -> skips connect   -> responds "Connected" before it is
```

- Connection logic is **mixed into route code** and must be repeated in every route.

<br><br>

### Hidden Issue in the Redis Side Too

- `new Redis()` starts connecting, but the code **does not wait** for it.
- `app.listen()` runs immediately. Early commands sit in ioredis's **offline queue**.
- No `redis.on("error")` listener, so connection errors are not handled.

<br><br>

### Fix: Connect Both at Boot

```js
const redis = new Redis(REDIS_URL);
redis.on("error", (err) => console.error("Redis error:", err));

try {
  await Promise.all([redis.ping(), mongoose.connect(MONGO_URL)]);   // top-level await (ESM)
} catch (err) {
  console.error("Startup failed:", err);
  process.exit(1);                                                  // fail fast
}

app.listen(3000, () => console.log("Server is running on port 3000"));
```

- If lazy is really needed, **cache the connect promise** so concurrent requests share one connect call.

<br><br>

### Key Points

| Aspect               | Eager (at startup) | Lazy (in route)            |
| :------------------- | :----------------- | :------------------------- |
| First request        | Fast               | Slow                       |
| Misconfig detected   | At boot            | On first request           |
| App boots if DB down | No                 | Yes                        |
| Concurrency safe     | Yes                | Race unless promise cached |
| Code location        | One place          | Repeated per route         |

- After the first connect, both Mongoose and ioredis **reconnect automatically**. Do not call `connect()` per request.
- In Docker, `depends_on` does not mean the DB is ready, so boot-time retries or healthchecks still matter.

<br><br>

## Other Ways to Ask This Question

- Where should you connect to the database in an Express app?
- Why is calling `mongoose.connect()` inside a route handler a bad idea?
- What does "fail fast" mean for application startup?
- Two requests hit a cold `/mongo` route at the same time. What can go wrong?
- Should the server start listening before the database connection is ready?
- How do you make sure a single DB connection is shared across requests?
