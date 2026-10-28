# command Override in Compose

## Question

What does `command:` override?

```yaml
services:
  redis:
    image: redis:latest
    command: ["redis-server", "--appendonly", "yes"]
```

## Answer

<mark>`command:` overrides the image's default CMD. It does not touch ENTRYPOINT.</mark>

- Same as adding arguments after the image name in `docker run`:

```bash
docker run redis redis-server --appendonly yes
```

<br><br>

### How the Redis Image Starts

```ini
ENTRYPOINT ["docker-entrypoint.sh"]     # kept
CMD        ["redis-server"]             # replaced by command:

Final process:
docker-entrypoint.sh redis-server --appendonly yes
```

- The entrypoint script still runs (it sets up permissions, then starts Redis).
- `command:` only changes **what arguments** it gets.
- Here it turns on **AOF persistence**, which the default CMD does not do.

<br><br>

### command vs entrypoint

| Compose key   | Overrides  | Effect                                                  |
| :------------ | :--------- | :------------------------------------------------------ |
| `command:`    | CMD        | Changes the default arguments, entrypoint kept          |
| `entrypoint:` | ENTRYPOINT | Replaces the executable, and the image's CMD is dropped |

<br><br>

### List Form vs String Form

```yaml
command: ["redis-server", "--appendonly", "yes"]   # list form, exact arguments
command: redis-server --appendonly yes             # string form, split on spaces
```

- Prefer the **list form**, no surprises with quoting.
- Neither form runs a shell. For `&&`, pipes or `$VARS`, use:

```yaml
command: ["sh", "-c", "redis-server --appendonly yes"]
```

<br><br>

### Key Points

- `command:` = **CMD** override, `entrypoint:` = **ENTRYPOINT** override.
- Image defaults stay unless you override them.
- Use `command:` to pass flags and config to the main process without building a new image.

<br><br>

## Other Ways to Ask This Question

- What is the difference between `command` and `entrypoint` in Compose?
- How do you pass extra flags to Redis in `docker-compose.yml`?
- What is the difference between CMD and ENTRYPOINT in a Dockerfile?
- How do you override the default command of an image in `docker run`?
- How do you enable Redis AOF persistence in Docker?
