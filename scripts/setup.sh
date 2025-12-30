#!/bin/bash

# ==============================================================================
# GranitePi-4-Nano: Beginner-Friendly Setup Utility
# Model: jewelzufo/unsloth_granite-4.0-h-350m-GGUF
# ==============================================================================

set -e # Exit on error

# Visual styling
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() { echo -e "${BLUE}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

echo -e "${GREEN}----------------------------------------------------"
echo "  GranitePi-4-Nano: Automated Deployment"
echo -e "----------------------------------------------------${NC}"

# 1. Architecture Validation
log "Checking system compatibility..."
ARCH=$(uname -m)
if [ "$ARCH" != "aarch64" ]; then
    error "This project requires a 64-bit OS. Detected: $ARCH. Please install 64-bit Raspberry Pi OS."
fi
success "64-bit architecture confirmed."

# 2. Package Management
log "Updating system repositories..."
sudo apt update && sudo apt upgrade -y || warn "Some updates failed, but proceeding..."

# 3. Resilient Swap Configuration
log "Checking swap file management..."
if [ ! -f /etc/dphys-swapfile ]; then
    warn "Swap management tool (dphys-swapfile) missing. Attempting to install..."
    sudo apt install dphys-swapfile -y || warn "Could not install swap tool. Performance may be reduced."
fi

if [ -f /etc/dphys-swapfile ]; then
    log "Optimizing swap partition to 2048MB..."
    sudo sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=2048/' /etc/dphys-swapfile
    sudo dphys-swapfile setup
    sudo dphys-swapfile swapon
    sudo systemctl restart dphys-swapfile
    success "Swap memory optimized for LLM inference."
fi

# 4. Ollama Installation & Service Configuration
if ! command -v ollama &> /dev/null; then
    log "Installing Ollama Framework..."
    curl -fsSL https://ollama.ai/install.sh | sh
else
    success "Ollama already installed."
fi

log "Applying Raspberry Pi 5 performance overrides..."
sudo mkdir -p /etc/systemd/system/ollama.service.d
cat <<EOF | sudo tee /etc/systemd/system/ollama.service.d/override.conf > /dev/null
[Service]
Environment="OLLAMA_KEEP_ALIVE=24h"
Environment="OLLAMA_NUM_THREADS=2"
EOF

log "Restarting Ollama to apply performance settings..."
sudo systemctl daemon-reload
sudo systemctl restart ollama

# 5. Robust Connection Loop (Fixes "Server not responding" error)
log "Waiting for Ollama service to start (this may take 15 seconds)..."
RETRIES=0
MAX_RETRIES=15
while ! ollama list > /dev/null 2>&1; do
    RETRIES=$((RETRIES+1))
    if [ $RETRIES -gt $MAX_RETRIES ]; then
        error "Ollama service failed to start. Please try running 'ollama serve' manually."
    fi
    echo -n "."
    sleep 2
done
echo -e "\n"
success "Ollama service is online."

# 6. Model Acquisition
log "Downloading model: jewelzufo/unsloth_granite-4.0-h-350m-GGUF..."
ollama pull jewelzufo/unsloth_granite-4.0-h-350m-GGUF || error "Failed to download model. Check internet connection."

echo -e "\n${GREEN}===================================================="
echo "🎉 SETUP COMPLETE"
echo -e "====================================================${NC}"
echo -e "Your Raspberry Pi 5 is now ready for private AI."
echo -e "Start chatting by running:"
echo -e "${BLUE}ollama run jewelzufo/unsloth_granite-4.0-h-350m-GGUF${NC}\n"
