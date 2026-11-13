# When ports Is Needed

## Question

If containers talk over the internal network, do you still need `ports:`?

```yaml
redis:
  ports:
    - "6379:6379"
mongo:
  ports:
    - "27017:27017"
```

## Answer

<mark>No. ports: is only for traffic coming from outside Docker (your host, the internet). Containers on the same network reach each other directly on the container port.</mark>

<br><br>

### Two Kinds of Traffic

```ini
Container -> Container   app -> redis:6379        Compose network, ports: NOT needed
Outside   -> Container   laptop -> localhost:6379 needs ports: "6379:6379"
```

<br><br>

### When You Do Need `ports:`

- The app's **public entry point** (`app: "3000:3000"`), so users and browsers can reach it.
- Running Node **on the host** (`npm run dev`) instead of in a container.
- Host tools: `redis-cli` from your laptop, MongoDB Compass, RedisInsight.

<br><br>

### When You Do Not

- Databases and caches that only the app talks to, once the app runs **inside** Compose.

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"        # only the app is published
    environment:
      REDIS_URL: redis://redis:6379

  redis:
    image: redis:latest    # no ports, reachable only inside the network
```

<br><br>

### Why Remove Them

- **Security:** a published Redis or Mongo with no password is a top target for attackers.
- **Firewall bypass:** on Linux, Docker writes its own iptables rules, so published ports can be reachable even when `ufw` says they are blocked.
- **Port clashes:** a local Redis already on 6379 makes `up` fail.
- Less exposure = smaller attack surface.

<br><br>

### Safer Options When You Need Host Access

| Option                                | Effect                                        |
| :------------------------------------ | :-------------------------------------------- |
| `"127.0.0.1:6379:6379"`               | Reachable only from this machine, not the LAN |
| `docker compose exec redis redis-cli` | Use the CLI inside the container, no port     |
| `compose.override.yml` with `ports:`  | Publish in dev only, not in prod              |

<br><br>

### `ports` vs `expose`

| Key       | Publishes to host | What it does                                      |
| :-------- | :---------------- | :------------------------------------------------ |
| `ports:`  | **Yes**           | Maps host port to container port                  |
| `expose:` | No                | Documentation only, containers can connect anyway |

<br><br>

### Key Points

- Container-to-container traffic **never** needs `ports:`.
- Publish only what **outside** clients must reach, usually just the app.
- In this lab, `ports:` exists because Node runs on the host. Move the app into Compose, and the DB ports can go.

<br><br>

## Other Ways to Ask This Question

- What is the difference between `ports` and `expose` in Docker Compose?
- Why is publishing database ports a security risk?
- How do you make a container reachable only from localhost?
- Does Docker bypass `ufw` firewall rules?
- How do you publish ports only in development?
