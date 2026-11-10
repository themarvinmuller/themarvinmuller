# Acesso remoto ao Linux pelo celular

## No Linux
```bash
sudo bash linux/acesso-remoto-celular.sh            # terminal (SSH)
sudo bash linux/acesso-remoto-celular.sh --desktop  # + área de trabalho (RDP)
```
Abra o link de login do Tailscale que aparecer e entre com sua conta.

## No celular
1. Instale o **Tailscale** (Android/iOS) e entre com a **mesma conta**.
2. Terminal: app **Termius** (ou JuiceSSH/Termux) → host = IP Tailscale (`100.x.x.x`), porta 22, seu usuário.
3. Área de trabalho (se usou `--desktop`): app **Microsoft Remote Desktop / Windows App** → IP Tailscale, porta 3389.

## Segurança (recomendado)
- Gere uma chave SSH no Termius, adicione em `~/.ssh/authorized_keys` no Linux e então
  coloque `PasswordAuthentication no` em `/etc/ssh/sshd_config.d/99-celular.conf` e rode `sudo systemctl restart ssh`.
- Não abra a porta 22 no roteador — o Tailscale dispensa isso.
