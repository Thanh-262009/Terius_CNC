#!/bin/bash
set -e

echo "==================================="
echo "   Auto Setup Python, Node.js, Cloudflare Tunnel"
echo "==================================="

# Detect OS
if [ -f /etc/debian_version ]; then
    OS="debian"
elif [ -f /etc/redhat-release ]; then
    OS="redhat"
elif [ -f /etc/alpine-release ]; then
    OS="alpine"
else
    OS="unknown"
fi

echo "Detected OS: $OS"

# Update & install
case $OS in
    debian)
        echo "[*] Updating apt..."
        sudo apt update -y
        sudo apt upgrade -y

        echo "[*] Installing Python..."
        sudo apt install -y python3 python3-pip

        echo "[*] Installing Node.js..."
        curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
        sudo apt install -y nodejs build-essential

        echo "[*] Installing Cloudflared..."
        wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
        sudo dpkg -i cloudflared-linux-amd64.deb || sudo apt -f install -y
        ;;
    redhat)
        echo "[*] Updating yum..."
        sudo yum update -y

        echo "[*] Installing Python..."
        sudo yum install -y python3 python3-pip

        echo "[*] Installing Node.js..."
        curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
        sudo yum install -y nodejs gcc-c++ make

        echo "[*] Installing Cloudflared..."
        wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-x86_64.rpm
        sudo rpm -i cloudflared-linux-x86_64.rpm
        ;;
    alpine)
        echo "[*] Updating apk..."
        sudo apk update
        sudo apk upgrade

        echo "[*] Installing Python..."
        sudo apk add --no-cache python3 py3-pip

        echo "[*] Installing Node.js..."
        sudo apk add --no-cache nodejs npm

        echo "[*] Installing Cloudflared..."
        wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64
        mv cloudflared-linux-arm64 cloudflared
        chmod +x cloudflared
        sudo mv cloudflared /usr/local/bin/
        ;;
    *)
        echo "Unsupported OS. Please install manually."
        exit 1
        ;;
esac

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
