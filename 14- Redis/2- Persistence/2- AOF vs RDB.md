# AOF vs RDB

## Question

AOF vs RDB: trade-offs?

## Answer

<mark>RDB takes periodic snapshots: compact and fast to restore, but you lose writes since the last snapshot. AOF logs every write: loses at most ~1 second, but files are bigger and restarts slower.</mark>

- Production default: use **both** (hybrid). Pure cache: often **neither**.

<br><br>

### How Each Works

```ini
RDB (snapshot)
  Every N seconds if M keys changed -> fork a child -> write dump.rdb
  Default: save 3600 1   300 100   60 10000

AOF (log)
  Every write command -> append to the AOF -> fsync once per second
```

<br><br>

### Comparison

| Aspect         | RDB                                          | AOF                                |
| :------------- | :------------------------------------------- | :--------------------------------- |
| What is saved  | Point-in-time snapshot of all data           | Log of every write command         |
| Data loss      | Everything since the last snapshot (minutes) | About 1 second (`everysec`)        |
| File size      | Small, compact binary                        | Larger, grows until rewritten      |
| Restart speed  | **Fast**, load one file                      | Slower, replay commands            |
| Write overhead | Low, child process does the work             | Small cost on every write (fsync)  |
| Backups        | **Easy**, copy one file offsite              | Harder, multiple files + manifest  |
| Big datasets   | `fork()` can cause latency spikes            | Rewrite also forks, but less often |
| Human readable | No (binary)                                  | Yes (Redis commands)               |

<br><br>

### RDB: Pros and Cons

**Pros**

- One compact file, perfect for **backups** and disaster recovery.
- **Fastest restart** for large datasets.
- Main thread barely affected, the forked child does the I/O.

**Cons**

- **Data loss window**: a crash loses all writes since the last snapshot.
- `fork()` on a large dataset can pause Redis for milliseconds to seconds, and copy-on-write can use **extra memory**.

<br><br>

### AOF: Pros and Cons

**Pros**

- **Durable**: at most ~1 second lost with `everysec`.
- Append-only, so a half-written line on crash is easy to repair (`redis-check-aof --fix`).
- Readable log. An accidental `FLUSHALL` can be removed from the AOF before a rewrite happens.

**Cons**

- **Bigger** files than RDB for the same data.
- **Slower restart**: commands must be replayed.
- Slightly slower writes, depending on `appendfsync`.

<br><br>

### Hybrid (Best of Both)

- `aof-use-rdb-preamble yes` (default): the AOF **base** file is stored in RDB format, followed by incremental AOF commands.
- Fast restart from the RDB part + only ~1 second of loss from the AOF part.
- When both are enabled, Redis restores from the **AOF** on startup.

<br><br>

### Which to Pick

| Use case                            | Choice                   |
| :---------------------------------- | :----------------------- |
| Pure cache, data can be rebuilt     | None (or RDB only)       |
| Can tolerate a few minutes of loss  | RDB                      |
| Sessions, queues, counters you need | AOF (`everysec`)         |
| Redis as a primary store            | AOF + RDB, plus replicas |

<br><br>

### Key Points

- RDB = **snapshot**, AOF = **write log**.
- RDB wins on **size, restart speed and backups**. AOF wins on **durability**.
- Neither replaces **replication** for high availability.
- Both need a **volume** in Docker, or the files die with the container.

<br><br>

## Other Ways to Ask This Question

- What are the two persistence options in Redis?
- How much data can Redis lose on a crash?
- Why can `BGSAVE` cause latency spikes on a large Redis instance?
- When would you disable Redis persistence completely?
- What is hybrid persistence (`aof-use-rdb-preamble`)?
- If both AOF and RDB exist, which one does Redis load on restart?
