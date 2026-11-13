# Named Volumes

## Question

What is a named volume, and why do `redis-data` and `mongo-data` exist?

```yaml
services:
  redis:
    image: redis:latest
    command: ["redis-server", "--appendonly", "yes"]
    volumes:
      - redis-data:/data

  mongo:
    image: mongo:latest
    volumes:
      - mongo-data:/data/db

volumes:
  redis-data:
  mongo-data:
```

## Answer

<mark>A named volume is storage managed by Docker that lives outside the container, so data survives when the container is removed.</mark>

- A container's writable layer is **temporary**. Remove the container and its data is gone.
- A named volume stores data on the host, under Docker's control (`/var/lib/docker/volumes/<name>` on Linux).
- You refer to it by **name**, not by a host path.

<br><br>

### Why `redis-data` and `mongo-data` Exist

- They hold the **database files** for Redis and Mongo.
- Without them, `docker compose down` (or recreating the container) would **wipe all data**.

| Volume       | Mounted at | What lives there                                       |
| :----------- | :--------- | :----------------------------------------------------- |
| `redis-data` | `/data`    | Redis AOF file (from `--appendonly yes`) and RDB dumps |
| `mongo-data` | `/data/db` | Mongo's database files                                 |

- `/data` and `/data/db` are the default data folders of the official images, so the volume catches everything they write.
- `redis-data:/data` follows the same **left = host side, right = container side** rule as ports.

<br><br>

### The Top-Level `volumes:` Key

- Declares the named volumes so Compose can **create** them.
- Each service then mounts a volume by name.
- Compose prefixes the project name, so the real name is like `<project>_redis-data`.

<br><br>

### Lifecycle

```bash
docker compose down        # containers removed, volumes kept, data survives
docker compose down -v     # containers AND volumes removed, data gone
docker volume ls           # list volumes
docker volume inspect <project>_redis-data   # see where it is stored
```

<br><br>

### Named Volume vs Bind Mount vs Anonymous Volume

| Type             | Syntax             | Managed by           | Best for                         |
| :--------------- | :----------------- | :------------------- | :------------------------------- |
| Named volume     | `redis-data:/data` | Docker               | Database and app data            |
| Bind mount       | `./data:/data`     | You (host path)      | Source code in dev, config files |
| Anonymous volume | `/data`            | Docker (random name) | Throwaway data                   |

- A source starting with `/` or `.` is a **bind mount**. A bare name is a **named volume**.
- Named volumes avoid host path and file permission issues, and work the same on every OS.

<br><br>

### Key Points

- Containers are **disposable**, data should not be.
- Named volume = data persists across `down`, `up`, image upgrades and container recreation.
- Only `down -v` or `docker volume rm` deletes it.
- A named volume lives on **one Docker host**. Sharing across machines needs shared storage or backups.

<br><br>

## Other Ways to Ask This Question

- How do you persist data in Docker?
- What happens to a database's data when its container is removed?
- What is the difference between a named volume and a bind mount?
- What does the top-level `volumes:` key do in `docker-compose.yml`?
- What is the difference between `docker compose down` and `docker compose down -v`?
- Where does Docker store named volume data on the host?
