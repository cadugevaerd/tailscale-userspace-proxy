# SSH Through SOCKS5

## OpenBSD netcat

Add this to `~/.ssh/config`:

```sshconfig
Host *.ts.net
  ProxyCommand nc -X 5 -x 127.0.0.1:1055 %h %p
```

Then:

```bash
ssh user@server.tailnet.ts.net
```

## Nmap ncat

Some systems use `ncat` instead of `nc`:

```sshconfig
Host *.ts.net
  ProxyCommand ncat --proxy 127.0.0.1:1055 --proxy-type socks5 %h %p
```

## Git over SSH

```bash
GIT_SSH_COMMAND='ssh -o ProxyCommand="nc -X 5 -x 127.0.0.1:1055 %h %p"' git clone git@server.tailnet.ts.net:repo.git
```

## Notes

- Use `socks5h://` for HTTP tooling so DNS resolution happens through the proxy.
- For SSH, DNS behavior depends on your `ProxyCommand` implementation.
