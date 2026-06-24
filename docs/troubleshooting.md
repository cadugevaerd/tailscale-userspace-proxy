# Troubleshooting

## Docker not found

Install Docker Desktop or Docker Engine.

Linux automatic attempt:

```bash
tailscale-proxy install --install-docker
```

## Docker daemon not reachable

Start Docker Desktop or the Docker service.

Linux:

```bash
sudo systemctl start docker
```

## Port 1055 busy

Use another port:

```bash
tailscale-proxy install --port 1080 --force
tailscale-proxy up
```

## Node does not appear in Tailscale

Check logs:

```bash
tailscale-proxy logs --tail 200
```

Common causes:

```text
expired auth key
key not reusable
tailnet policy rejects tag
network cannot reach Tailscale control plane
```

## MagicDNS does not resolve

Use `socks5h://` instead of `socks5://` with HTTP tools:

```bash
curl --proxy socks5h://127.0.0.1:1055 http://server.tailnet.ts.net
```

Also ensure:

```text
TS_ACCEPT_DNS=true
```

## curl works but SSH does not

Your `nc` may not support `-X` and `-x`.

Try `ncat`:

```sshconfig
ProxyCommand ncat --proxy 127.0.0.1:1055 --proxy-type socks5 %h %p
```

## App ignores proxy variables

Try setting all common variables:

```bash
export ALL_PROXY=socks5h://127.0.0.1:1055
export all_proxy=socks5h://127.0.0.1:1055
export HTTP_PROXY=http://127.0.0.1:1055
export http_proxy=http://127.0.0.1:1055
export HTTPS_PROXY=http://127.0.0.1:1055
export https_proxy=http://127.0.0.1:1055
```
