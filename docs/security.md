# Security

## Default is local only

```text
PROXY_BIND=127.0.0.1
```

Only processes on the same machine can use the proxy.

## Do not expose to the internet

This project creates a SOCKS5/HTTP proxy. It does not add user/password authentication in front of the proxy.

Dangerous:

```text
0.0.0.0:1055 open to internet
```

Safer remote access:

```text
SSH tunnel -> localhost proxy
```

## If exposing on LAN

Use all of these:

```text
Firewall allowlist
Private LAN only
No port forwarding
Ephemeral Tailscale auth key
Tags/ACLs with least privilege
```

## Auth key handling

- Do not pass real keys on shared shell history.
- Prefer the interactive prompt.
- Never commit `.env`.
- Rotate leaked keys immediately.
