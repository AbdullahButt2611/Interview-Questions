# AOF Location and the /data Volume

## Question

Where does Redis write the AOF in the container, and why does it line up with the `/data` volume mount?

```yaml
redis:
  image: redis:latest
  command: ["redis-server", "--appendonly", "yes"]
  volumes:
    - redis-data:/data
```

## Answer

<mark>Redis writes persistence files to its working directory. The official image sets that to /data, so the AOF lands in /data/appendonlydir/, which is exactly where the redis-data volume is mounted.</mark>

<br><br>

### The Chain

```ini
1. Official Redis image Dockerfile:   WORKDIR /data
2. Redis config "dir" default:        ./  (current working directory)
3. So Redis writes to:                /data
4. AOF ends up in:                    /data/appendonlydir/
5. Compose mounts:                    redis-data -> /data
   => AOF is stored in the named volume, outside the container
```

<br><br>

### What Lives in /data

```ini
/data/
  appendonlydir/
    appendonly.aof.1.base.rdb
    appendonly.aof.1.incr.aof
    appendonly.aof.manifest
  dump.rdb                      <- RDB snapshot, same folder
```

- Both AOF and RDB files go to the same `dir`, so **one mount** covers all persistence.

<br><br>

### Verify It

```bash
docker exec -it chai-aur-redis redis-cli CONFIG GET dir      # "/data"
docker exec -it chai-aur-redis ls /data/appendonlydir
docker volume inspect <project>_redis-data                   # where it sits on the host
```

<br><br>

### Why It Matters

- The official image declares `VOLUME /data`. Without your own mount, Docker creates an **anonymous volume** with a random name.
- After `docker compose down`, the next `up` creates a new container with a **new, empty** anonymous volume. The old AOF is orphaned, so the data looks lost.
- Mounting a named volume at `/data` makes the data **survive** `down`, upgrades and container recreation.

<br><br>

### Common Mistakes

| Mistake                                       | Result                                   |
| :-------------------------------------------- | :--------------------------------------- |
| Mounting the wrong path (`/var/lib/redis`)    | Redis still writes to `/data`, data lost |
| Changing `--dir /backup` but mounting `/data` | Files go outside the volume, data lost   |
| `appendonly yes` with **no** volume           | AOF exists, but dies with the container  |
| Bind mount with wrong host permissions        | Redis cannot write, fails at startup     |

<br><br>

### Key Points

- Persistence path = Redis `dir` setting. In the official image that is **`/data`**.
- Volume mount path must **match** the `dir`, or persistence does nothing useful.
- Same idea for Mongo: the official image writes to `/data/db`, hence `mongo-data:/data/db`.

<br><br>

## Other Ways to Ask This Question

- Where does Redis store its data inside a Docker container?
- What does the Redis `dir` config setting control?
- Why is the Redis volume mounted at `/data` and not somewhere else?
- Why did my Redis data disappear even though AOF was enabled?
- How do you find which folder Redis is writing to?
