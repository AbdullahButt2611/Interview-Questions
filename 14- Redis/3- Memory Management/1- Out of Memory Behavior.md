# Out of Memory Behavior

## Question

What happens when Redis runs out of memory?

## Answer

<mark>It depends on maxmemory-policy. With the default noeviction, Redis rejects writes with an OOM error but keeps serving reads. With an eviction policy like allkeys-lru, it deletes keys to make room.</mark>

- If `maxmemory` is **not set** (default `0` = no limit), Redis keeps growing until the OS or Docker **kills** it.

<br><br>

### Two Settings Decide Everything

```ini
maxmemory          how much RAM Redis may use     (default 0 = unlimited)
maxmemory-policy   what to do when it is full     (default noeviction)
```

<br><br>

### Case 1: No maxmemory (Default)

- Redis uses as much RAM as the machine gives it.
- When RAM runs out:
  - Linux **OOM killer** kills the Redis process, or
  - Docker kills the container (exit code `137`), or
  - The OS starts **swapping**, and latency jumps from microseconds to milliseconds.
- All data not yet persisted is **lost**.

<br><br>

### Case 2: maxmemory Set + noeviction (Default Policy)

```ini
127.0.0.1:6379> SET key value
(error) OOM command not allowed when used memory > 'maxmemory'.
```

- **Writes fail** (`SET`, `LPUSH`, `HSET`).
- **Reads still work** (`GET`), and `DEL` still works to free space.
- No data is lost, but the app sees errors.

<br><br>

### Case 3: maxmemory Set + Eviction Policy

| Policy            | Evicts from     | Which keys                       |
| :---------------- | :-------------- | :------------------------------- |
| `noeviction`      | Nothing         | Rejects writes instead (default) |
| `allkeys-lru`     | All keys        | Least recently used              |
| `allkeys-lfu`     | All keys        | Least frequently used            |
| `allkeys-random`  | All keys        | Random                           |
| `volatile-lru`    | Keys with a TTL | Least recently used              |
| `volatile-lfu`    | Keys with a TTL | Least frequently used            |
| `volatile-random` | Keys with a TTL | Random                           |
| `volatile-ttl`    | Keys with a TTL | Shortest time to live left       |

- `volatile-*` with **no TTL keys** has nothing to evict, so it behaves like `noeviction`.
- LRU and LFU are **approximate**: Redis samples a few keys (`maxmemory-samples 5`) instead of tracking all of them.

<br><br>

### Which Policy to Pick

| Use case                                | Policy                         |
| :-------------------------------------- | :----------------------------- |
| Pure cache                              | `allkeys-lru` or `allkeys-lfu` |
| Cache keys (with TTL) + permanent keys  | `volatile-lru`                 |
| Primary data store, nothing may be lost | `noeviction` + alerts          |

<br><br>

### Set It in Docker

```yaml
command: ["redis-server", "--appendonly", "yes",
          "--maxmemory", "256mb", "--maxmemory-policy", "allkeys-lru"]
```

<br><br>

### Monitor It

```bash
redis-cli INFO memory   # used_memory_human, maxmemory_human
redis-cli INFO stats    # evicted_keys (rising = eviction is happening)
```

<br><br>

### Key Points

- Always set `maxmemory` in production. Unlimited means the OS decides, usually by killing Redis.
- Leave headroom: RDB/AOF rewrites `fork()` and can need extra memory (copy-on-write).
- Default `noeviction` protects data but **breaks writes**. Caches should evict instead.
- Rising `evicted_keys` means the cache is too small, or TTLs are missing.

<br><br>

## Other Ways to Ask This Question

- What does "OOM command not allowed when used memory > 'maxmemory'" mean?
- What are Redis eviction policies?
- LRU vs LFU in Redis: which would you choose for a cache?
- What is the default `maxmemory-policy` in Redis?
- Why does `volatile-lru` still give OOM errors?
- How do you limit Redis memory in Docker?
