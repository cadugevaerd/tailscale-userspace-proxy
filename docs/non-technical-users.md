# Non-Technical User Guide

## Install

Copy and paste this:

```bash
curl -fsSL https://raw.githubusercontent.com/cadugevaerd/tailscale-userspace-proxy/main/install.py | python3
```

When asked for a Tailscale auth key, paste the key from your administrator.

## Start

```bash
tailscale-proxy up
```

## Stop

```bash
tailscale-proxy down
```

## Check if it is working

```bash
tailscale-proxy status
```

## Send this to your app

```text
SOCKS5 proxy: socks5h://127.0.0.1:1055
HTTP proxy:   http://127.0.0.1:1055
```

## If something breaks

Send your admin this output:

```bash
tailscale-proxy status
tailscale-proxy logs --tail 100
```
