# Tailscale Auth Key

Create a key in the Tailscale admin console.

Recommended settings:

```text
Reusable:       yes
Ephemeral:      yes
Pre-approved:   yes, if allowed by your tailnet policy
Tags:           optional, for example tag:proxy
Expiry:         as short as practical
```

## Why ephemeral

Ephemeral nodes are removed automatically when they stop being used. This is ideal for disposable proxy containers.

## Never commit the key

Bad:

```yaml
TS_AUTHKEY: tskey-auth-real-secret
```

Good:

```bash
tailscale-proxy install
# paste key only into the prompt
```

The CLI stores it in:

```text
~/.tailscale-userspace-proxy/.env
```

The file is set to `chmod 600` when the OS allows it.
