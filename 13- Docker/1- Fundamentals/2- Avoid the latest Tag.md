# Avoid the latest Tag

## Question

What is wrong with `image: redis:latest` and `mongo:latest`?

```yaml
redis:
  image: redis:latest
mongo:
  image: mongo:latest
```

## Answer

<mark>latest is a moving pointer, not a version. Builds are not reproducible, and one pull can silently jump a major version that cannot read your existing data. Pin a version like redis:8.0 or mongo:8.0.</mark>

<br><br>

### What `latest` Really Is

- Just a **tag name**, the default when you write no tag.
- Points to whatever the maintainer pushed most recently. It **changes over time**.
- Docker caches it locally, so `latest` on your laptop can be **months older** than `latest` in CI.

```ini
Jan:  you pull redis:latest  -> 7.4
Jun:  CI pulls redis:latest  -> 8.0     same file, different database
```

<br><br>

### What Goes Wrong

**1. Not reproducible**

- Same `docker-compose.yml`, different versions per machine and per day.
- "Works on my machine" for databases.

**2. Surprise major upgrades break data**

- **MongoDB** must upgrade **one major at a time** (6.0 → 7.0 → 8.0), setting `featureCompatibilityVersion` each step.
- Jumping several majors on an old `mongo-data` volume: **mongod refuses to start**.
- **Redis**: a newer version can write RDB/AOF files an older version cannot read, so rolling back fails.

**3. No easy rollback**

- You do not know which version you were on before, so you cannot go back to it.

**4. Hard to audit**

- Security scans and incident reports need to know the **exact** version running.

<br><br>

### Fix: Pin the Version

```yaml
redis:
  image: redis:8.0             # major.minor: gets patch fixes, no surprise majors
mongo:
  image: mongo:8.0
```

| Pin style                     | Example               | Changes when you pull          |
| :---------------------------- | :-------------------- | :----------------------------- |
| `latest`                      | `redis:latest`        | Anything, any time             |
| Major                         | `redis:8`             | Minor + patch                  |
| Major.minor (**recommended**) | `redis:8.0`           | Patch only                     |
| Exact patch                   | `redis:8.0.2`         | Never (tag could be re-pushed) |
| Digest                        | `redis@sha256:abc...` | Never, fully immutable         |

<br><br>

### Upgrade on Purpose

- Change the tag in a PR, read the release notes, test, then deploy.
- Back up the volume first.
- Tools like **Dependabot** or **Renovate** open PRs when new versions come out.

<br><br>

### Key Points

- `latest` ≠ "latest stable". It means "whatever was pushed last".
- Databases are the **worst** place for `latest`, because the data on the volume outlives the image.
- Pin `major.minor` for a good balance. Pin a **digest** when you need exact, repeatable builds.

<br><br>

## Other Ways to Ask This Question

- Why should you not use the `latest` tag in production?
- How do you make Docker builds reproducible?
- What is an image digest, and when would you pin it?
- Why did my MongoDB container stop starting after `docker compose pull`?
- How do you safely upgrade a database image in Docker?
