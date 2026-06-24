# Tailscale Userspace Proxy

Run the official `tailscale/tailscale` Docker image in **userspace networking mode** and expose a local **SOCKS5/HTTP proxy** for restricted environments that cannot create `/dev/net/tun`.

> **Upstream / projeto principal:** this repository is a helper installer/CLI around the official Tailscale project. Use [`tailscale/tailscale`](https://github.com/tailscale/tailscale) as the primary reference for Tailscale behavior, Docker image features, and userspace networking support.

```text
Restricted app / Claude Cowork / CI
        │
        │ ALL_PROXY / HTTP_PROXY
        ▼
Desktop / server with Docker
        │
        ▼
tailscale/tailscale in userspace mode
        │
        ▼
SOCKS5 + HTTP proxy on :1055
        │
        ▼
Tailnet target: SSH, HTTP apps, private services
```

## Why

Some environments cannot run a normal Tailscale client because they lack `/dev/net/tun` or privileged networking. Tailscale userspace mode lets `tailscaled` act as a proxy instead.

This repo provides:

- Python CLI installed with `uv`.
- Docker Compose stack using the official Tailscale image.
- SOCKS5 and HTTP proxy on the same port.
- Safe default bind: `127.0.0.1`.
- One-command bootstrap for non-technical users.

## Easy install

For users without `git`:

```bash
curl -fsSL https://raw.githubusercontent.com/cadugevaerd/tailscale-userspace-proxy/main/install.py | python3
```

Then start:

```bash
tailscale-proxy up
```

During setup, every missing prerequisite gets its own prompt. If the user answers `n`, installation is cancelled.

The installer also offers an optional Claude Code integration: if accepted, it registers the Docker MCP server as `docker-mcp` using:

```bash
claude mcp add docker-mcp -s user -- uvx docker-mcp
```

This MCP option is currently Claude Code only. It is skipped by default in `--non-interactive` or `--yes` runs; use `--install-claude-code-docker-mcp` to force it.

## UV install

```bash
uv tool install git+https://github.com/cadugevaerd/tailscale-userspace-proxy
tailscale-proxy install
tailscale-proxy up
```

## One command after first install

```bash
tailscale-proxy up
```

If config is missing:

```bash
tailscale-proxy up --init
```

## Commands

```bash
tailscale-proxy install      # create config and check prerequisites
tailscale-proxy up           # start Docker Compose stack
tailscale-proxy down         # stop stack
tailscale-proxy restart      # restart stack
tailscale-proxy status       # show Docker/Tailscale status
tailscale-proxy logs -f      # follow logs
tailscale-proxy test         # test https://ifconfig.me via SOCKS5
tailscale-proxy config       # show config paths; auth key is masked
tailscale-proxy update       # update CLI via uv
tailscale-proxy uninstall    # remove container and config
```

## Tailscale auth key

Create an auth key in the Tailscale admin console.

Recommended:

```text
Reusable:       yes
Ephemeral:      yes
Pre-approved:   yes, if your policy allows it
Tags:           tag:proxy, optional
Expiry:         short when possible
```

Never commit the auth key.

## Proxy URLs

Default:

```text
SOCKS5: socks5h://127.0.0.1:1055
HTTP:   http://127.0.0.1:1055
```

Use `socks5h://`, not only `socks5://`, when you want DNS names like `server.tailnet.ts.net` resolved through Tailscale/MagicDNS.

## Use with curl

```bash
curl --proxy socks5h://127.0.0.1:1055 http://server.tailnet.ts.net
```

## Use with apps

```bash
export ALL_PROXY=socks5h://127.0.0.1:1055
export HTTP_PROXY=http://127.0.0.1:1055
export HTTPS_PROXY=http://127.0.0.1:1055
```

## Use with SSH

See [`docs/ssh-through-socks.md`](docs/ssh-through-socks.md).

Short example:

```sshconfig
Host *.ts.net
  ProxyCommand nc -X 5 -x 127.0.0.1:1055 %h %p
```

## Use with Claude Cowork / restricted source

See [`docs/claude-cowork.md`](docs/claude-cowork.md).

Recommended remote pattern:

```text
Cowork machine ──SSH tunnel──► Desktop 127.0.0.1:1055 ──► Tailnet
```

```bash
ssh -L 1055:127.0.0.1:1055 user@desktop
export ALL_PROXY=socks5h://127.0.0.1:1055
```

## Security defaults

The proxy binds to localhost only:

```text
PROXY_BIND=127.0.0.1
```

Do not expose this proxy to the public internet. SOCKS5/HTTP proxy mode does not add client authentication.

If you intentionally expose it on LAN:

```bash
tailscale-proxy install --bind 0.0.0.0
```

Use firewall/IP allowlist.

## Config location

```text
~/.tailscale-userspace-proxy/
├── compose.yaml
└── .env
```

`~/.tailscale-userspace-proxy/.env` is created with `chmod 600` when possible.

## Manual development

```bash
git clone https://github.com/cadugevaerd/tailscale-userspace-proxy
cd tailscale-userspace-proxy
uv run tailscale-proxy --help
uv run tailscale-proxy validate --home /tmp/tsp-test
```

## References

- Tailscale userspace networking mode: `tailscaled --tun=userspace-networking`
- Official Docker image supports `TS_USERSPACE`
- Official image environment variables include `TS_AUTHKEY`, `TS_SOCKS5_SERVER`, and `TS_OUTBOUND_HTTP_PROXY_LISTEN`
