# Claude Cowork / Restricted Source Usage

Use this when the source machine cannot run Tailscale directly because it has no `/dev/net/tun`, no privileged networking, or limited Docker access.

## Recommended architecture

```text
Claude Cowork / restricted source
        │
        │ SSH tunnel or network access
        ▼
Your desktop running tailscale-proxy
        │
        ▼
Tailnet target
```

## Safest mode: SSH tunnel

On the restricted machine:

```bash
ssh -L 1055:127.0.0.1:1055 user@desktop
```

In another shell on the restricted machine:

```bash
export ALL_PROXY=socks5h://127.0.0.1:1055
export HTTP_PROXY=http://127.0.0.1:1055
export HTTPS_PROXY=http://127.0.0.1:1055
```

Now apps can reach tailnet hosts through your desktop.

## Direct LAN mode

On the desktop:

```bash
tailscale-proxy install --bind 0.0.0.0
tailscale-proxy up
```

On the restricted machine:

```bash
export ALL_PROXY=socks5h://DESKTOP_LAN_IP:1055
export HTTP_PROXY=http://DESKTOP_LAN_IP:1055
export HTTPS_PROXY=http://DESKTOP_LAN_IP:1055
```

Security warning:

```text
Do not expose port 1055 to the internet.
Use firewall allowlist if binding to 0.0.0.0.
```

## Test from restricted machine

```bash
curl --proxy socks5h://127.0.0.1:1055 http://server.tailnet.ts.net
```

For LAN mode:

```bash
curl --proxy socks5h://DESKTOP_LAN_IP:1055 http://server.tailnet.ts.net
```
