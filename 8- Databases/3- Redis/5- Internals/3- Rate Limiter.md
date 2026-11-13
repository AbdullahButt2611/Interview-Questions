# Rate Limiter with Redis

## Question

How would you implement a rate limiter?

## Answer

<mark>Keep a counter per client in Redis and reject with 429 once it passes the limit. Simplest is a fixed window (INCR + EXPIRE). For accuracy, use a sliding window with a Sorted Set, run atomically in a Lua script.</mark>

- Redis works well because every app instance shares the **same counters**, and `INCR` is atomic.

<br><br>

### Algorithms

| Algorithm              | Redis tools          | Accuracy                    | Memory              |
| :--------------------- | :------------------- | :-------------------------- | :------------------ |
| Fixed window           | `INCR` + `EXPIRE`    | Burst of 2x at window edges | 1 key               |
| Sliding window log     | Sorted Set + Lua     | Exact                       | 1 entry per request |
| Sliding window counter | 2 counters, weighted | Close approximation         | 2 keys              |
| Token bucket           | Hash + Lua           | Smooth, allows short bursts | 1 key               |

<br><br>

### 1. Fixed Window (Express Middleware)

```js
const LIMIT = 100;   // requests per minute

async function rateLimit(req, res, next) {
  const window = Math.floor(Date.now() / 60000);
  const key = `rl:${req.ip}:${window}`;

  const [[, count]] = await redis.multi().incr(key).expire(key, 60).exec();

  res.set("X-RateLimit-Remaining", Math.max(0, LIMIT - count));
  if (count > LIMIT) {
    return res.status(429).set("Retry-After", "60").json({ error: "Too many requests" });
  }
  next();
}

app.use(rateLimit);
```

- `MULTI` runs `INCR` and `EXPIRE` together, so a key can never be left **without a TTL**.
- Weakness: 100 requests at 10:00:59 + 100 at 10:01:00 = **200 in 2 seconds**.

<br><br>

### 2. Sliding Window Log (Exact)

```lua
-- KEYS[1] = key, ARGV = now(ms), window(ms), limit, unique member
redis.call("ZREMRANGEBYSCORE", KEYS[1], 0, ARGV[1] - ARGV[2])   -- drop old requests
if redis.call("ZCARD", KEYS[1]) >= tonumber(ARGV[3]) then
  return 0                                                       -- over the limit
end
redis.call("ZADD", KEYS[1], ARGV[1], ARGV[4])                    -- record this request
redis.call("PEXPIRE", KEYS[1], ARGV[2])
return 1
```

```js
const allowed = await redis.eval(script, 1, `rl:${userId}`, Date.now(), 60000, 100, crypto.randomUUID());
```

- Counts requests in the **last 60 seconds** at any moment. No edge bursts.
- **Lua** makes the check-and-add atomic. Without it, two parallel requests can both pass at count 99.
- Cost: one Sorted Set entry per request, so memory grows with the limit.

<br><br>

### Design Decisions

- **Who to limit:** user ID or API key is better than IP. Many users can share one IP (offices, mobile networks).
- **Response:** HTTP `429 Too Many Requests` with a `Retry-After` header.
- **Redis down:** **fail open** (allow all, keep the app up) or **fail closed** (block all, protect the backend). A business decision.
- **Do not reinvent in production:** `express-rate-limit` with `rate-limit-redis` already does this.

<br><br>

### Key Points

- Shared counter in Redis = one limit across **all app instances**.
- Fixed window: simplest, allows edge bursts. Sliding window: exact, uses more memory.
- Every check-and-update must be **atomic**: `MULTI` or **Lua**.
- Always set a TTL on limiter keys, or they pile up forever.

<br><br>

## Other Ways to Ask This Question

- How do you limit API requests per user in a distributed system?
- Fixed window vs sliding window rate limiting: trade-offs?
- Why does a rate limiter need atomic operations?
- What is the token bucket algorithm?
- What status code should a rate-limited request return?
- Should a rate limiter fail open or fail closed when Redis is down?
