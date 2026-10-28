# depends_on and Readiness

## Question

Why doesn't `depends_on` by itself guarantee the database is ready?

```yaml
app:
  depends_on:
    - redis
    - mongo
```

## Answer

<mark>Short-form depends_on only waits until the container has started, not until the database inside is accepting connections. "Running" is not "ready".</mark>

<br><br>

### Started vs Ready

```ini
t0   mongo container starts          <- depends_on is satisfied HERE
t0   app container starts, connects  -> ECONNREFUSED
t3s  mongod finishes startup, opens port 27017   <- actually ready
```

- Redis is ready in milliseconds, so the bug often hides.
- Mongo can take **seconds** (storage engine startup, init scripts on first run).
- Docker cannot know when the process inside is "ready" unless you tell it how to check.

<br><br>

### What `depends_on` Does and Does Not Do

| Does                                    | Does not                               |
| :-------------------------------------- | :------------------------------------- |
| Starts `redis` and `mongo` before `app` | Wait for the DB to accept connections  |
| Stops `app` before them on `down`       | Restart `app` if the DB crashes later  |
| Works only within `docker compose up`   | Exist in Kubernetes or other platforms |

<br><br>

### Fix 1: Healthcheck + `service_healthy`

```yaml
services:
  app:
    depends_on:
      redis:
        condition: service_healthy
      mongo:
        condition: service_healthy

  redis:
    image: redis:8.0
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  mongo:
    image: mongo:8.0
    healthcheck:
      test: ["CMD", "mongosh", "--quiet", "--eval", "db.adminCommand('ping')"]
      interval: 5s
      timeout: 5s
      retries: 10
      start_period: 10s
```

- Compose now waits for each DB to report **healthy** before starting `app`.
- Other conditions: `service_started` (the default) and `service_completed_successfully` (for one-off jobs like migrations).

<br><br>

### Fix 2: Retry in the App (Still Needed)

- Healthchecks only help at **startup**. The DB can restart at any time later.
- The app should **retry the connection** with backoff, not crash on the first failure.
- ioredis and Mongoose already reconnect after the first connection. Add a retry loop around the **initial** connect.

<br><br>

### Key Points

- `depends_on` = **start order**. `condition: service_healthy` = **readiness**.
- A healthcheck tells Docker **how** to test readiness.
- Always add app-side retries too. Orchestrators like Kubernetes have no `depends_on` at all.
- `docker compose up --wait` blocks until all services are healthy, which is handy in CI.

<br><br>

## Other Ways to Ask This Question

- My app starts before the database is ready in Docker Compose. How do you fix it?
- What is the difference between a container being "running" and "healthy"?
- How do you add a healthcheck for Redis and MongoDB in Compose?
- What does `condition: service_healthy` do?
- Why should an app retry its database connection on startup?
