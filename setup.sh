#!/bin/bash
set -e

echo "==================================="
echo "   Auto Setup Python & Node.js"
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
        ;;
    redhat)
        echo "[*] Updating yum..."
        sudo yum update -y

        echo "[*] Installing Python..."
        sudo yum install -y python3 python3-pip

        echo "[*] Installing Node.js..."
        curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
        sudo yum install -y nodejs gcc-c++ make
        ;;
    alpine)
        echo "[*] Updating apk..."
        sudo apk update
        sudo apk upgrade

        echo "[*] Installing Python..."
        sudo apk add --no-cache python3 py3-pip

        echo "[*] Installing Node.js..."
        sudo apk add --no-cache nodejs npm
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
echo "==================================="
