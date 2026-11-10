#!/usr/bin/env bash
# Configura acesso remoto ao Linux pelo celular: SSH (terminal) + Tailscale (VPN segura)
# + opcional xrdp (área de trabalho gráfica). Uso: sudo bash acesso-remoto-celular.sh [--desktop]
set -euo pipefail
[ "$(id -u)" -eq 0 ] || { echo "Rode com sudo."; exit 1; }

if command -v apt-get >/dev/null; then PM="apt-get install -y"; apt-get update
elif command -v dnf >/dev/null; then PM="dnf install -y"
elif command -v pacman >/dev/null; then PM="pacman -S --noconfirm"
else echo "Gerenciador de pacotes não suportado"; exit 1; fi

# 1) SSH
$PM openssh-server || $PM openssh
SSHD=/etc/ssh/sshd_config.d/99-celular.conf
mkdir -p /etc/ssh/sshd_config.d
cat > "$SSHD" <<'CONF'
PermitRootLogin no
PubkeyAuthentication yes
MaxAuthTries 3
CONF
systemctl enable --now ssh 2>/dev/null || systemctl enable --now sshd

# 2) Tailscale (acesso de qualquer rede sem abrir portas no roteador)
command -v tailscale >/dev/null || curl -fsSL https://tailscale.com/install.sh | sh
systemctl enable --now tailscaled
tailscale up --ssh || true

# 3) Opcional: área de trabalho gráfica via RDP
if [ "${1:-}" = "--desktop" ]; then
  $PM xrdp && systemctl enable --now xrdp
fi

# 4) Firewall: libera SSH/RDP só pela interface do Tailscale
if command -v ufw >/dev/null; then
  ufw allow in on tailscale0 to any port 22 proto tcp
  [ "${1:-}" = "--desktop" ] && ufw allow in on tailscale0 to any port 3389 proto tcp
fi

echo; echo "Pronto! IP Tailscale: $(tailscale ip -4 2>/dev/null || echo '(faça login no link acima)')"
echo "Usuário: ${SUDO_USER:-$USER}"
