# container_name in Compose

## Question

What does `container_name` do, and what is a downside of setting it?

```yaml
services:
  redis:
    image: redis:latest
    container_name: chai-aur-redis
```

## Answer

<mark>`container_name` gives the container a fixed name. Downside: names must be unique, so you cannot scale the service or run two copies of the stack.</mark>

<br><br>

### What It Does

- Without it, Compose generates a name: `<project>-<service>-<index>`.

```ini
Without container_name   ->  redis-lab-redis-1
With container_name      ->  chai-aur-redis
```

- With it, the name is fixed, so commands are easier to type:

```bash
docker exec -it chai-aur-redis redis-cli
docker logs chai-aur-redis
```

<br><br>

### Downsides

- **Cannot scale:** `docker compose up --scale redis=2` fails. Two containers cannot share one name.
- **Cannot run two copies of the stack:** a second project (another folder, git worktree, or parallel CI job) fails with:

```ini
Conflict. The container name "/chai-aur-redis" is already in use
```

- **Clashes with leftovers:** an old container with the same name, from another project, blocks `up` until removed.
- **Not needed for networking:** containers already reach each other by **service name** (`redis:6379`).

<br><br>

### Better Alternative

- Use Compose commands with the **service name**, no fixed name needed:

```bash
docker compose exec redis redis-cli
docker compose logs redis
```

<br><br>

### Key Points

- `container_name` = convenience for humans, not for networking.
- Fine for a single local dev setup.
- Avoid it for services you may **scale**, or stacks that run in **multiple copies** (CI, worktrees, staging and dev on one host).

<br><br>

## Other Ways to Ask This Question

- Why does `docker compose up --scale` fail for my service?
- How does Compose name containers by default?
- Why do I get "container name is already in use" when starting a stack?
- Do you need `container_name` for containers to talk to each other?
- What is the difference between a service name and a container name in Compose?
