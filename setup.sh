#!/bin/bash
set -e

echo "==================================="
echo "   Auto Setup Python, Node.js, Cloudflare Tunnel (Ubuntu/Debian)"
echo "==================================="

# Update system
echo "[*] Updating apt..."
sudo apt update -y
sudo apt upgrade -y

# Install Python
echo "[*] Installing Python..."
sudo apt install -y python3 python3-pip

# Install Node.js 20.x
echo "[*] Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs build-essential

# Install Cloudflared
echo "[*] Installing Cloudflared..."
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
chmod +x cloudflared
sudo mv cloudflared /usr/local/bin/

# Verify install
echo "==================================="
echo " Installed versions:"
echo "Python: $(python3 --version)"
echo "Pip:    $(pip3 --version)"
echo "Node:   $(node -v)"
echo "NPM:    $(npm -v)"
echo "Cloudflared: $(cloudflared --version)"
echo "==================================="

# Run Cloudflare Tunnel on port 6009
echo "[*] Starting Cloudflare Tunnel on port 6009..."
cloudflared tunnel --url http://localhost:6009 > cloudflared.log 2>&1 &
sleep 5

# Extract public URL
TUNNEL_URL=$(grep -oE "https://[a-zA-Z0-9.-]+\.trycloudflare.com" cloudflared.log | head -n 1)

echo "==================================="
if [ -n "$TUNNEL_URL" ]; then
    echo " Cloudflare Tunnel is running!"
    echo " Public URL: $TUNNEL_URL"
else
    echo " Could not detect tunnel URL. Check logs:"
    echo "   tail -f cloudflared.log"
fi
echo "==================================="
