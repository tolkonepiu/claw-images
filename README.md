# claw-images

Unofficial container image definitions for claw projects that do not publish
official images.

## Supported images

| Name                                                                                                    | Description                               | Project                                          | Docker image                                  | Versions                                                                                 |
| ------------------------------------------------------------------------------------------------------- | ----------------------------------------- | ------------------------------------------------ | --------------------------------------------- | ---------------------------------------------------------------------------------------- |
| [`copaw`](https://github.com/agentscope-ai/CoPaw/blob/main/deploy/Dockerfile)                           | Personal AI assistant, easy to deploy     | [CoPaw](https://github.com/agentscope-ai/CoPaw)  | `ghcr.io/tolkonepiu/copaw`                    | [All](https://github.com/tolkonepiu/claw-images/pkgs/container/copaw)                    |
| [`ironclaw`](https://github.com/nearai/ironclaw/blob/main/Dockerfile)                                   | OpenClaw-inspired Rust implementation     | [ironclaw](https://github.com/nearai/ironclaw)   | `ghcr.io/tolkonepiu/ironclaw`                 | [All](https://github.com/tolkonepiu/claw-images/pkgs/container/ironclaw)                 |
| [`ironclaw-worker`](https://github.com/nearai/ironclaw/blob/main/Dockerfile.worker)                     | Worker image for ironclaw                 | [ironclaw](https://github.com/nearai/ironclaw)   | `ghcr.io/tolkonepiu/ironclaw-worker`          | [All](https://github.com/tolkonepiu/claw-images/pkgs/container/ironclaw-worker)          |
| [`nanobot`](https://github.com/HKUDS/nanobot/blob/main/Dockerfile)                                      | Ultra-lightweight OpenClaw implementation | [nanobot](https://github.com/HKUDS/nanobot)      | `ghcr.io/tolkonepiu/nanobot`                  | [All](https://github.com/tolkonepiu/claw-images/pkgs/container/nanobot)                  |
| [`openclaw-node22`](https://github.com/openclaw/openclaw/blob/main/Dockerfile)                          | OpenClaw base image with Node.js 22       | [OpenClaw](https://github.com/openclaw/openclaw) | `ghcr.io/tolkonepiu/openclaw-node22`          | [All](https://github.com/tolkonepiu/claw-images/pkgs/container/openclaw-node22)          |
| [`openclaw-node22-slim`](https://github.com/openclaw/openclaw/blob/main/Dockerfile)                     | OpenClaw slim image with Node.js 22       | [OpenClaw](https://github.com/openclaw/openclaw) | `ghcr.io/tolkonepiu/openclaw-node22-slim`     | [All](https://github.com/tolkonepiu/claw-images/pkgs/container/openclaw-node22-slim)     |
| [`openclaw-sandbox`](https://github.com/openclaw/openclaw/blob/main/Dockerfile.sandbox)                 | OpenClaw sandbox base image               | [OpenClaw](https://github.com/openclaw/openclaw) | `ghcr.io/tolkonepiu/openclaw-sandbox`         | [All](https://github.com/tolkonepiu/claw-images/pkgs/container/openclaw-sandbox)         |
| [`openclaw-sandbox-browser`](https://github.com/openclaw/openclaw/blob/main/Dockerfile.sandbox-browser) | OpenClaw sandbox image with browser       | [OpenClaw](https://github.com/openclaw/openclaw) | `ghcr.io/tolkonepiu/openclaw-sandbox-browser` | [All](https://github.com/tolkonepiu/claw-images/pkgs/container/openclaw-sandbox-browser) |

> [!NOTE]
>
> Images are published for `amd64` and `arm64`. Tags like `v0.23.0-amd64` and
> `v0.23.0-arm64` are architecture-specific, while `v0.23.0` and `latest` are
> multi-arch tags.

## Docker examples

Use `ironclaw` as a reference for the available tag formats:

```bash
# Latest multi-arch image
docker pull ghcr.io/tolkonepiu/ironclaw:latest

# Versioned multi-arch image
docker pull ghcr.io/tolkonepiu/ironclaw:v0.23.0

# Architecture-specific image for amd64
docker pull ghcr.io/tolkonepiu/ironclaw:v0.23.0-amd64

# Architecture-specific image for arm64
docker pull ghcr.io/tolkonepiu/ironclaw:v0.23.0-arm64
```

## Adding a new image definition

1. Create a new file in `images/`, for example `images/<project>.json`.
2. Set `version`, `source.repo`, and `source.tag` to the upstream release you
   want to build.
3. Add one or more entries under `images[]` with the final image name and the
   Dockerfile path in the upstream repository.
4. If the upstream Dockerfile expects build arguments, add an optional `args`
   object to the image entry. Each key/value pair is passed through as a Docker
   build argument. Keys and values must be single-line strings.
5. Open a pull request to validate the build.
