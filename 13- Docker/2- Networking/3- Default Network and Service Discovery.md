# Default Network and Service Discovery

## Question

What default network does Compose create, and how do services find each other?

## Answer

<mark>Compose creates one bridge network named &lt;project&gt;_default and attaches every service to it. Docker's built-in DNS resolves each service name to its container's IP, so services connect by name.</mark>

<br><br>

### The Default Network

```ini
docker compose up
  -> network:  <project>_default    (driver: bridge)
  -> redis, mongo, app all join it
docker compose down
  -> containers removed, network removed
```

- **Project name** = the folder name (lowercased, special characters removed), unless set with `name:` in the file, `-p`, or `COMPOSE_PROJECT_NAME`.
- Check it:

```bash
docker network ls                          # find <project>_default
docker network inspect <project>_default   # see attached containers and IPs
```

<br><br>

### How Services Find Each Other

```ini
app container:  connect to "redis:6379"
  1. asks Docker's embedded DNS server (127.0.0.11)
  2. DNS answers: "redis" -> 172.18.0.2
  3. app connects to 172.18.0.2:6379
```

- Names that resolve on the network:
  - **Service name** (`redis`), the one to use.
  - `container_name` (`chai-aur-redis`), if set.
  - Any `aliases` you define.
- IPs can change on every restart. **Names stay the same**, so never hardcode IPs.

<br><br>

### Compose Network vs Default Docker Bridge

| Network                                | DNS by name     | Created by          |
| :------------------------------------- | :-------------- | :------------------ |
| `<project>_default` (Compose)          | **Yes**         | `docker compose up` |
| User-defined (`docker network create`) | **Yes**         | You                 |
| Default `bridge` (plain `docker run`)  | **No**, IP only | Docker at install   |

- That is why two containers started with plain `docker run` cannot reach each other by name, but Compose services can.

<br><br>

### Scaling and Isolation

- `docker compose up --scale app=3`: the name `app` returns **all 3 IPs** (DNS round robin).
- Need isolation? Define custom networks and attach only some services:

```yaml
services:
  app:
    networks: [frontend, backend]
  redis:
    networks: [backend]          # app can reach redis, outside services cannot

networks:
  frontend:
  backend:
```

<br><br>

### Key Points

- One project = one default network = everyone can talk to everyone.
- Service name = hostname. Port = **container port**, not the published one.
- Built-in DNS works only on Compose and user-defined networks, not the default `bridge`.
- `ports:` is only for traffic from **outside** Docker. Container-to-container traffic does not need it.

<br><br>

## Other Ways to Ask This Question

- How does service discovery work in Docker Compose?
- Why can't my containers ping each other by name with `docker run`?
- What is the default network driver in Docker Compose?
- How does Compose decide the network name?
- How do you isolate services from each other in Compose?
- What happens to the network on `docker compose down`?
