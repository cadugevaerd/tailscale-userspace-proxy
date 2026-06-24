# Quickstart

## 1. Install

```bash
curl -fsSL https://raw.githubusercontent.com/cadugevaerd/tailscale-userspace-proxy/main/install.py | python3
```

The installer checks each prerequisite and asks before installing or starting anything missing:

```text
Python >= 3.10
uv
Docker CLI
Docker daemon running
Docker Compose v2
port 1055
Tailscale auth key
```

If you answer `n` to any prerequisite prompt, installation is cancelled.

## 2. Start

```bash
tailscale-proxy up
```

## 3. Check status

```bash
tailscale-proxy status
```

## 4. Use the proxy

```bash
export ALL_PROXY=socks5h://127.0.0.1:1055
export HTTP_PROXY=http://127.0.0.1:1055
export HTTPS_PROXY=http://127.0.0.1:1055
```

## 5. Test

```bash
tailscale-proxy test https://ifconfig.me
```

Or test a tailnet service:

```bash
tailscale-proxy test http://server.tailnet.ts.net
```
