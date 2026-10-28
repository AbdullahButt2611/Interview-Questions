# Append Only File (AOF)

## Question

What does `--appendonly yes` do?

```yaml
redis:
  image: redis:latest
  command: ["redis-server", "--appendonly", "yes"]
  volumes:
    - redis-data:/data
```

## Answer

<mark>It turns on AOF persistence: Redis logs every write command to a file on disk and replays it on restart, so data survives a restart or crash.</mark>

- Default is `appendonly no`. Without it, Redis relies only on periodic **RDB snapshots**, and can lose minutes of writes.

<br><br>

### How It Works

```ini
Client:  SET user:1 "Ali"
Redis:   1. apply to memory
         2. append "SET user:1 Ali" to the AOF
         3. fsync to disk (every second by default)

Restart: read the AOF from top to bottom -> replay commands -> data rebuilt
```

- Only **write** commands are logged (`SET`, `INCR`, `HSET`, `DEL`). Reads are not.

<br><br>

### fsync Policy (`appendfsync`)

| Value                | When data hits disk | Max data loss on power cut | Speed   |
| :------------------- | :------------------ | :------------------------- | :------ |
| `always`             | After every write   | Almost none                | Slowest |
| `everysec` (default) | Once per second     | About 1 second             | Fast    |
| `no`                 | When the OS decides | Up to ~30 seconds          | Fastest |

- A Redis **process** crash loses nothing with `everysec`, since the OS still holds the data. Only an OS crash or power cut loses the last second.

<br><br>

### Files on Disk (Redis 7+)

```ini
/data/appendonlydir/
  appendonly.aof.1.base.rdb      <- compact snapshot (base)
  appendonly.aof.1.incr.aof      <- writes since the base
  appendonly.aof.manifest        <- lists which files make up the AOF
```

- `/data` is the mounted `redis-data` volume, so the AOF survives `docker compose down`.

<br><br>

### AOF Rewrite

- The log keeps growing (`INCR counter` 1 million times = 1 million lines).
- Redis **rewrites** it in the background to the smallest set of commands that rebuild the current data.
- Triggered automatically when the file doubles in size (`auto-aof-rewrite-percentage 100`), or manually with `BGREWRITEAOF`.

<br><br>

### Verify It Is On

```bash
docker exec -it chai-aur-redis redis-cli CONFIG GET appendonly   # "yes"
docker exec -it chai-aur-redis redis-cli INFO persistence         # aof_enabled:1
```

<br><br>

### Key Points

- AOF = **write log**, RDB = **point-in-time snapshot**.
- AOF loses at most about 1 second of writes. RDB can lose everything since the last snapshot.
- Costs: bigger files, slightly more disk I/O, slower restart than loading an RDB.
- If both exist, Redis loads the **AOF** on startup, because it is more complete.
- AOF needs a **volume**. Without one, the file dies with the container.

<br><br>

## Other Ways to Ask This Question

- How does Redis persist data to disk?
- What is AOF in Redis and how does it work?
- What does `appendfsync everysec` mean? How much data can you lose?
- Why does the AOF file keep growing, and how does Redis shrink it?
- How do you enable persistence for Redis in Docker?
- What happens to Redis data on restart without AOF?
