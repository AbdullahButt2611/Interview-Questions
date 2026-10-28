# Choosing a TTL

## Question

How do you choose a TTL? What does a stale read cost?

## Answer

<mark>The TTL is the longest staleness the business can accept for that data. Pick it by weighing how often the data changes and what a stale read costs against how much the cache saves.</mark>

- Longer TTL = higher hit ratio, less DB load, **more staleness**.
- Shorter TTL = fresher data, **more misses** and DB load.

<br><br>

### Questions to Ask

- **How often does the data change?** Rarely changing data can live longer.
- **What does a stale read cost?** Cosmetic, annoying, or money and security?
- **Is the cache invalidated on write?** If yes, the TTL is only a safety net and can be longer.
- **How expensive is a miss?** A slow aggregation is worth caching longer than a quick `findById`.
- **How hot is the key?** A key read once an hour gains little from caching.

<br><br>

### What a Stale Read Costs

| Level     | Example                                        | Cost                       |
| :-------- | :--------------------------------------------- | :------------------------- |
| Harmless  | View count, "trending" list a minute old       | Nobody notices             |
| Annoying  | User edits their name, still sees the old one  | Confusion, support tickets |
| Expensive | Wrong price at checkout, oversold stock        | Lost money, refunds        |
| Dangerous | Revoked permission or banned user still cached | **Security hole**          |

- Annoying case: the writer should **read their own writes**. Invalidate on update, or skip the cache for that user right after the write.
- Expensive and dangerous cases: **do not trust the cache** for the decision. Read the source of truth.

<br><br>

### Typical TTLs

| Data                                | TTL                       | Why                                    |
| :---------------------------------- | :------------------------ | :------------------------------------- |
| Trending, feeds, leaderboards       | 30 to 60 s                | Changes constantly, slight lag is fine |
| Feature flags, config               | 30 to 60 s                | Changes rarely, but should apply fast  |
| Product catalog, descriptions       | 1 to 24 h                 | Rarely changes, invalidate on edit     |
| User profile (invalidated on write) | 1 to 24 h                 | TTL is only a safety net               |
| Sessions                            | Session lifetime, sliding | Expiry **is** the logout               |
| Price / stock at checkout           | **No cache**              | Must be exact                          |
| Permissions / auth checks           | Very short, or none       | Stale = security risk                  |

<br><br>

### Tune With Data

- Start **short**, then raise the TTL while watching:
  - **Hit ratio:** `keyspace_hits / (keyspace_hits + keyspace_misses)` from `INFO stats`.
  - **DB load:** queries per second on Mongo.
  - **Staleness complaints:** bugs and support tickets.
- Add **jitter** to whatever TTL you choose.

<br><br>

### Key Points

- TTL = **acceptable staleness**, decided per data type, not one global value.
- Invalidate on write for correctness. Use the TTL as a **safety net**.
- Never cache the final check for **money, stock or permissions**.
- Measure hit ratio and DB load, then adjust.

<br><br>

## Other Ways to Ask This Question

- How long should you cache data in Redis?
- What is the trade-off between cache freshness and hit ratio?
- What is "read your own writes", and how does caching break it?
- Which data should never be cached?
- How do you measure if a cache TTL is working?
- What happens if a user's permissions are cached and then revoked?
