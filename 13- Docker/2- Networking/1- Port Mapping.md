# Port Mapping (Host vs Container)

## Question

What does `ports: "6379:6379"` mean? Which side is the host?

## Answer

<mark>Format is HOST:CONTAINER. The left side is the host port, the right side is the container port.</mark>

```ini
ports:
  - "6379:6379"
     ^^^^ ^^^^
     host container
```

- Traffic hitting **port 6379 on the host machine** is forwarded to **port 6379 inside the container**.
- Same thing with the CLI: `docker run -p 6379:6379 redis`.

<br><br>

### Why It Is Needed

- A container has its **own isolated network**. Redis listens on 6379 **inside** the container only.
- Without a mapping, your laptop (or any app outside Docker) cannot reach it.
- Port mapping opens a door from the host into the container.

<br><br>

### Different Numbers Make It Clear

```yaml
ports:
  - "6380:6379"
```

- Redis still runs on **6379 inside** the container.
- From the host you connect on **6380**: `redis-cli -p 6380`.
- Useful when the host port is already taken, or to run **two Redis containers** side by side (`6379:6379` and `6380:6379`).

<br><br>

### Who Uses Which Port

| Client location                  | Connects to                             |
| :------------------------------- | :-------------------------------------- |
| Host machine (laptop, browser)   | `localhost:<host port>`                 |
| Another container, same network  | `<service name>:<container port>`       |

- Containers on the same Docker network talk directly using the **container port**, no mapping needed.
- Example: an app container connects to `redis:6379`, even if the mapping is `6380:6379`.

<br><br>

### Other Forms

```ini
"6379"                    # container port only, Docker picks a random host port
"127.0.0.1:6379:6379"     # only reachable from this machine, not the network
"6379:6379/udp"           # UDP instead of the default TCP
```

<br><br>

### Key Points

- **Left = host, right = container.** Easy memory trick: outside to inside, left to right.
- Always **quote** ports in Compose. YAML can read unquoted `xx:yy` (values under 60) as a base-60 number.
- Binding `0.0.0.0` (the default) exposes Redis to the whole network. Use `127.0.0.1:6379:6379` for local-only access.
- `EXPOSE` in a Dockerfile is only documentation, it does **not** publish the port.

<br><br>

## Other Ways to Ask This Question

- In `-p 8080:80`, which port is the host and which is the container?
- What is port mapping (port publishing) in Docker?
- Why can't I connect to my Redis container from my laptop?
- What is the difference between `EXPOSE` and `ports` / `-p`?
- How do you run two containers that both listen on the same port?
- How does one container connect to another container's port?
