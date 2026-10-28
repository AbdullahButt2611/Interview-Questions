# Image vs Container

## Question

What is the difference between a Docker image and a container?

## Answer

<mark>An image is a read-only template. A container is a running (or stopped) instance of that image.</mark>

Think of it like:

```ini
Image     = Class            (blueprint)
Container = Object           (instance created from the blueprint)

Image     = Program on disk
Container = Running process
```

<br><br>

### Docker Image

- A **read-only** package with the app code, runtime, libraries, dependencies and config.
- Built from a `Dockerfile` using `docker build`.
- Made of **stacked layers**, each layer is one instruction in the Dockerfile.
- **Immutable**: to change it, you build a new image.
- Stored in a registry (Docker Hub, ECR, etc.) and shared with `docker push` / `docker pull`.
- Does nothing on its own. It just sits on disk.

<br><br>

### Docker Container

- A **live, isolated process** created from an image with `docker run`.
- Adds a thin **writable layer** on top of the image's read-only layers.
- Changes made inside the container stay in that container and **do not affect the image**.
- Has its own state: running, paused, stopped, removed.
- When the container is removed, its writable layer (and data in it) is gone, unless you use **volumes**.

<br><br>

### Key Differences

| Aspect     | Image                          | Container                           |
| :--------- | :----------------------------- | :---------------------------------- |
| Nature     | Static template                | Running instance                    |
| Mutability | Read-only                      | Writable layer on top               |
| Created by | `docker build` / `docker pull` | `docker run` / `docker create`      |
| State      | No state                       | Running, paused, stopped            |
| Count      | One image                      | Many containers from the same image |
| Storage    | Registry or local disk         | Host machine only                   |

<br><br>

### Example

```bash
docker pull redis            # downloads the redis image
docker run -d --name r1 redis  # container 1 from that image
docker run -d --name r2 redis  # container 2 from the same image

docker images                # lists images
docker ps -a                 # lists containers
```

- One `redis` image, two independent containers `r1` and `r2`.
- Data written in `r1` is not visible in `r2`.

<br><br>

### Key Points

- Image = **what** to run, Container = the thing **actually running**.
- One image can create **many** containers.
- You can create an image from a container with `docker commit`, but a Dockerfile is preferred.
- An image cannot be deleted while a container (even stopped) still uses it, unless forced.

<br><br>

## Other Ways to Ask This Question

- Docker image vs Docker container, explain.
- How is a container related to an image?
- What happens when you run `docker run` on an image?
- Can one image create multiple containers? How?
- If you change something inside a container, does the image change?
- Explain images and containers using an analogy.
