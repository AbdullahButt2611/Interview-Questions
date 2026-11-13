# Real Health Check

## Question

`/mongo` returns `"Connected"` without checking anything. How would you write a real health check?

```js
app.get("/mongo", async (req, res) => {
  // ...
  res.json({ mongo: "Connected", database: mongoose.connection.name });   // never verified
});
```

## Answer

<mark>Actually talk to each dependency (ping), put a timeout on it, and return 200 if all pass or 503 if any fail.</mark>

- Hardcoded `"Connected"` is a lie. It returns the same answer when Mongo is dead.

<br><br>

### What a Real Check Needs

- **A live round trip:** `db.admin().ping()` for Mongo, `PING` for Redis.
- **A timeout:** a check that hangs for 30s is as bad as no check.
- **Correct status code:** `200` healthy, `503` unhealthy. Load balancers read the code, not the body.
- **Per-dependency result:** so you know **which** one failed.
- **Cheap:** no heavy queries. It runs every few seconds.

<br><br>

### Implementation

```js
const withTimeout = (promise, ms) =>
  Promise.race([
    promise,
    new Promise((_, reject) => setTimeout(() => reject(new Error(`timeout after ${ms}ms`)), ms)),
  ]);

async function check(name, fn) {
  const start = Date.now();
  try {
    await withTimeout(fn(), 1000);
    return { name, status: "up", latencyMs: Date.now() - start };
  } catch (err) {
    return { name, status: "down", error: err.message };
  }
}

app.get("/health", async (req, res) => {
  const checks = await Promise.all([
    check("mongo", () => mongoose.connection.db.admin().ping()),
    check("redis", () => redis.ping()),
  ]);

  const healthy = checks.every((c) => c.status === "up");
  res.set("Cache-Control", "no-store");
  res.status(healthy ? 200 : 503).json({ status: healthy ? "ok" : "degraded", checks });
});
```

- `Promise.all` runs both checks **in parallel**, so the total time is the slowest one, not the sum.
- If Mongo never connected, `connection.db` is `undefined`. The `TypeError` is caught and reported as `down`.

<br><br>

### Sample Responses

```ini
200 OK
{ "status": "ok", "checks": [
  { "name": "mongo", "status": "up", "latencyMs": 3 },
  { "name": "redis", "status": "up", "latencyMs": 1 } ] }

503 Service Unavailable
{ "status": "degraded", "checks": [
  { "name": "mongo", "status": "up", "latencyMs": 4 },
  { "name": "redis", "status": "down", "error": "timeout after 1000ms" } ] }
```

<br><br>

### Common Mistakes

| Mistake                                 | Problem                                  |
| :-------------------------------------- | :--------------------------------------- |
| Hardcoded `"Connected"`                 | Always green, even when the DB is down   |
| Only reading `readyState`               | Driver's view, can be stale for seconds  |
| No timeout                              | Health check hangs, probe times out      |
| Returning 200 with `"status": "down"`   | Load balancer only reads the status code |
| Real queries on large collections       | Health check itself loads the DB         |
| Exposing error details publicly         | Leaks hostnames, versions, internals     |

<br><br>

### Key Points

- Health check = **real ping + timeout + 503 on failure**.
- Check dependencies in **parallel**.
- In production, return details only to internal callers, and a plain status to the public.
- Split into **liveness** (process is alive, no DB checks) and **readiness** (dependencies are reachable) when running on Kubernetes.

<br><br>

## Other Ways to Ask This Question

- How do you check if MongoDB is actually reachable from Node.js?
- Why is `readyState` not a good health check?
- What status code should a health check return when a dependency is down?
- How do you add a timeout to a promise in JavaScript?
- How would you build one `/health` endpoint for multiple dependencies?
- What should and should not be included in a health check response?
