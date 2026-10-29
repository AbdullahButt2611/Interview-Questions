# Is Redis a Database or a Cache?

## Question

Is Redis a database or a cache?

## Answer

<mark>Both. Redis is an in-memory data store. Configuration decides its role: no persistence + eviction makes it a cache, AOF/RDB persistence + noeviction + replication makes it a database.</mark>

- Official description: an in-memory **data structure store**, used as a database, cache, message broker and streaming engine.

<br><br>

### Same Redis, Different Settings

| Setting            | As a cache                    | As a database                  |
| :----------------- | :---------------------------- | :----------------------------- |
| Persistence        | Off, or RDB only              | AOF (`everysec`) + RDB         |
| `maxmemory-policy` | `allkeys-lru` / `allkeys-lfu` | `noeviction`                   |
| TTL on keys        | On almost every key           | Only where data should expire  |
| Source of truth    | Another DB (Mongo, Postgres)  | **Redis itself**               |
| Data loss on crash | Fine, rebuilt from the DB     | Must be minimal                |
| Replication        | Optional                      | Required (replicas + failover) |

<br><br>

### Common Roles

- **Cache:** query results, API responses, rendered pages.
- **Primary store:** sessions, leaderboards, counters, rate limits, feature flags.
- **Message broker:** Streams, Pub/Sub, job queues (BullMQ).
- **Coordination:** distributed locks, deduplication.

<br><br>

### Limits as a Primary Database

- **RAM-bound:** all data must fit in memory, which costs far more per GB than disk.
- **Queries by key:** no joins, no ad-hoc filters like SQL or Mongo (unless you add the Redis Query Engine).
- **Durability:** AOF `everysec` can lose about **1 second** of writes on a power cut.
- **Async replication:** a failover can drop recently acknowledged writes.
- **Transactions:** `MULTI` has no rollback. If one command fails, the others still run.

<br><br>

### When Redis Is a Good Primary Store

- Data **fits in RAM** and grows predictably.
- Access is **by key** (or simple ranges, like a leaderboard).
- Losing the last second of writes is **acceptable**.
- Speed matters more than complex querying.

<br><br>

### In This Project

- Redis runs with `--appendonly yes` and a named volume, so it **persists**.
- But Mongo holds the real documents, so Redis's role is the **cache / fast layer**.

<br><br>

### Key Points

- Redis is a **data store**. "Cache" or "database" is a **role**, set by configuration.
- Cache = eviction + TTLs + a separate source of truth.
- Database = persistence + `noeviction` + replication, with RAM and query limits.
- Interview answer: "Both, depending on how it is configured and what is the source of truth."

<br><br>

## Other Ways to Ask This Question

- Can Redis be used as a primary database?
- What configuration turns Redis into a pure cache?
- What are the risks of using Redis as your only database?
- Is Redis persistent?
- What is Redis used for besides caching?
