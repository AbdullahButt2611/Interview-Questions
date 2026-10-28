# Compose Down vs Down -v

## Question

What happens to Redis data after `docker compose down`? After `docker compose down -v`?

```yaml
services:
  redis:
    image: redis:latest
    command: ["redis-server", "--appendonly", "yes"]
    volumes:
      - redis-data:/data

volumes:
  redis-data:
```

## Answer

<mark>`down` keeps the data (volume survives). `down -v` deletes the volume, so the data is gone for good.</mark>

<br><br>

### `docker compose down`

- Stops and **removes containers** and the default **network**.
- **Named volumes are kept**, so `redis-data` is untouched.
- Next `docker compose up` creates a new container, mounts the same volume, and Redis **reloads the AOF** from `/data`.
- Result: <mark>all keys come back.</mark>

<br><br>

### `docker compose down -v`

- Does everything `down` does, **plus removes volumes**:
  - Named volumes declared in the top-level `volumes:` key (`redis-data`).
  - Anonymous volumes attached to the containers.
- Next `up` creates a **fresh, empty** volume.
- Result: Redis starts with **no data**. This cannot be undone.

<br><br>

### Comparison

| Command                  | Containers | Network | Named volumes | Redis data after `up`  |
| :----------------------- | :--------- | :------ | :------------ | :--------------------- |
| `docker compose stop`    | Kept       | Kept    | Kept          | Same container, intact |
| `docker compose down`    | Removed    | Removed | Kept          | Intact                 |
| `docker compose down -v` | Removed    | Removed | **Removed**   | **Empty**              |

<br><br>

### Why Redis Data Is Safe on `down`

- `down` sends `SIGTERM`, so Redis shuts down **gracefully** and flushes the AOF to disk.
- `--appendonly yes` logs every write, so the volume has a full record.
- Without a volume, the data would live in the container's writable layer and be **lost on `down`** too.

<br><br>

### Key Points

- Data lives in the **volume**, not the container. Removing the container is safe.
- `-v` is the dangerous flag. Use it only when you want a clean reset.
- Volumes marked `external: true` are **never removed**, even with `-v`.
- `down` never removes images unless you add `--rmi`.

<br><br>

## Other Ways to Ask This Question

- Does `docker compose down` delete my database data?
- How do you reset a Compose stack's data completely?
- What is the difference between `docker compose stop` and `docker compose down`?
- What does the `-v` / `--volumes` flag do in `docker compose down`?
- I ran `down` and `up` and my data is still there. Why?
- How do you protect a volume from being deleted by `down -v`?
