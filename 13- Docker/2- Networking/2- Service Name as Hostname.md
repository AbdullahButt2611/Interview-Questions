# Service Name as Hostname

## Question

If the Node app were added as a compose service, what would `REDIS_URL` be?

```js
const redis = new Redis(process.env.REDIS_URL || "redis://localhost:6379");
```

## Answer

<mark>REDIS_URL=redis://redis:6379. Inside Compose, each service name is a hostname, and the port is the container port.</mark>

- `localhost` would **not** work. Inside the app container, `localhost` is the app container itself.

<br><br>

### Why the Service Name Works

```ini
docker compose up
  -> creates network  <project>_default
  -> attaches redis, mongo, app to it
  -> built-in DNS:    "redis" -> redis container IP
                      "mongo" -> mongo container IP
```

- The hostname is the **service key** in `docker-compose.yml` (`redis:`), not the image name.

<br><br>

### Compose File with the App

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      REDIS_URL: redis://redis:6379
      MONGO_URL: mongodb://mongo:27017/chai_aur_redis
    depends_on:
      - redis
      - mongo

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

- The code already reads `process.env.REDIS_URL`, so **no code change**. The `localhost` fallback still works when running Node on the host.

<br><br>

### Which URL From Where

| App runs on                   | REDIS_URL                | Why                                  |
| :---------------------------- | :----------------------- | :----------------------------------- |
| Host machine (`npm run dev`)  | `redis://localhost:6379` | Uses the published port `6379:6379`  |
| Container in the same Compose | `redis://redis:6379`     | Service name via Docker DNS          |
| Container, wrong value        | `redis://localhost:6379` | `ECONNREFUSED`, points at app itself |

<br><br>

### Port: Container Side, Not Host Side

- Containers talk on the **container port** (right side of `ports:`).
- With `ports: "6380:6379"`, the app still uses `redis://redis:6379`.
- Once the app is inside Compose, Redis and Mongo **do not need `ports:`** at all. Removing them hides the databases from the outside world.

<br><br>

### Key Points

- Service name = hostname on the Compose network.
- Use the **container port**, not the published host port.
- `localhost` inside a container = that container.
- `depends_on` only orders startup. It does **not** wait for Redis to be ready.

<br><br>

## Other Ways to Ask This Question

- How do containers in Docker Compose talk to each other?
- Why does `localhost` not work between containers?
- Do you need `ports:` for one container to reach another?
- What network does Docker Compose create by default?
- Should the app use the container name or the service name as the host?
