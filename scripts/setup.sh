#!/bin/bash

# ==============================================================================
# GranitePi-4-Nano: Automated Setup Utility
# Refactored for Robustness, Safety, and Performance
# ==============================================================================

# Configuration
MODEL_NAME="jewelzufo/unsloth_granite-4.0-h-350m-GGUF"
SWAP_SIZE_MB=2048
MIN_RAM_GB=4       # Warn if below this
MIN_DISK_GB=5      # Required free space
MAX_TEMP_C=75      # Warn if CPU is hotter than this

# Visual styling
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\133[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------

log() { echo -e "${BLUE}[INFO] $(date +'%H:%M:%S')${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN] $(date +'%H:%M:%S')${NC} $1"; }
success() { echo -e "${GREEN}[OK]   $(date +'%H:%M:%S')${NC} $1"; }
error() { echo -e "${RED}[ERR]  $(date +'%H:%M:%S')${NC} $1"; exit 1; }

check_internet() {
    log "Checking internet connectivity..."
    if ! ping -c 1 google.com &> /dev/null; then
        error "No internet connection detected. Please connect and try again."
    fi
}

cleanup() {
    if [ $? -ne 0 ]; then
        echo -e "\n${RED}Script failed or was interrupted. Check messages above.${NC}"
    fi
}
trap cleanup EXIT

# ------------------------------------------------------------------------------
# Pre-flight Checks
# ------------------------------------------------------------------------------

echo -e "${GREEN}===================================================="
echo "   GranitePi-4-Nano Setup Assistant"
echo -e "====================================================${NC}"

# 1. Architecture Check
ARCH=$(uname -m)
if [ "$ARCH" != "aarch64" ]; then
    error "Architecture mismatch. Required: aarch64. Detected: $ARCH"
fi

# 2. Hardware Resource Validation
log "Validating hardware resources..."

# Check RAM
TOTAL_MEM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
TOTAL_MEM_GB=$((TOTAL_MEM_KB / 1024 / 1024))
if [ "$TOTAL_MEM_GB" -lt "$MIN_RAM_GB" ]; then
    warn "Detected ${TOTAL_MEM_GB}GB RAM. 8GB is recommended for optimal performance."
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Yy]$ ]] && exit 1
fi

# Check Disk Space
FREE_DISK_KB=$(df . --output=avail | tail -1)
FREE_DISK_GB=$((FREE_DISK_KB / 1024 / 1024))
if [ "$FREE_DISK_GB" -lt "$MIN_DISK_GB" ]; then
    error "Insufficient disk space. Free: ${FREE_DISK_GB}GB. Required: ${MIN_DISK_GB}GB."
fi

# Check Temperature
if command -v vcgencmd &> /dev/null; then
    CURRENT_TEMP=$(vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*')
    CURRENT_TEMP_INT=${CURRENT_TEMP%.*}
    if [ "$CURRENT_TEMP_INT" -gt "$MAX_TEMP_C" ]; then
        warn "CPU Temperature is high (${CURRENT_TEMP}°C). Ensure active cooling is working."
    else
        success "System check passed: ${TOTAL_MEM_GB}GB RAM, ${FREE_DISK_GB}GB Free, ${CURRENT_TEMP}°C"
    fi
else
    warn "vcgencmd not found. Skipping thermal check."
fi

check_internet

# ------------------------------------------------------------------------------
# Installation Steps
# ------------------------------------------------------------------------------

# 3. System Updates
log "Updating package lists (this may take a moment)..."
sudo apt update || warn "apt update encountered errors."
# Note: Full upgrade is skipped to prevent unexpected long wait times or breakage,
# but dependencies will be installed as needed.

# 4. Swap Configuration
log "Configuring swap memory (${SWAP_SIZE_MB}MB)..."
if ! command -v dphys-swapfile &> /dev/null; then
    log "Installing dphys-swapfile..."
    sudo apt install -y dphys-swapfile
fi

# Backup config before editing
if [ -f /etc/dphys-swapfile ]; then
    sudo cp /etc/dphys-swapfile /etc/dphys-swapfile.bak
    # Use generic regex to replace any existing swap size definition
    sudo sed -i "s/^CONF_SWAPSIZE=.*/CONF_SWAPSIZE=${SWAP_SIZE_MB}/" /etc/dphys-swapfile

    sudo dphys-swapfile setup
    sudo dphys-swapfile swapon
    success "Swap configured."
else
    warn "/etc/dphys-swapfile not found. Skipping swap optimization."
fi

# 5. Ollama Installation
if ! command -v ollama &> /dev/null; then
    log "Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
else
    success "Ollama is already installed."
fi

# 6. Service Optimization (Pi 5 Specifics)
log "Applying service overrides..."
SERVICE_DIR="/etc/systemd/system/ollama.service.d"
OVERRIDE_FILE="${SERVICE_DIR}/override.conf"

if [ ! -f "$OVERRIDE_FILE" ] || ! grep -q "OLLAMA_NUM_THREADS=2" "$OVERRIDE_FILE"; then
    sudo mkdir -p "$SERVICE_DIR"
    cat <<EOF | sudo tee "$OVERRIDE_FILE" > /dev/null
[Service]
Environment="OLLAMA_KEEP_ALIVE=24h"
Environment="OLLAMA_NUM_THREADS=2"
EOF
    log "Reloading systemd daemon..."
    sudo systemctl daemon-reload
    sudo systemctl restart ollama
    success "Service overrides applied."
else
    success "Service overrides already present."
fi

# 7. Service Health Check
log "Waiting for Ollama API..."
RETRIES=0
MAX_RETRIES=15
while ! ollama list &> /dev/null; do
    RETRIES=$((RETRIES+1))
    if [ $RETRIES -gt $MAX_RETRIES ]; then
        error "Ollama failed to start after 30 seconds. Check 'systemctl status ollama'."
    fi
    echo -n "."
    sleep 2
done
echo ""
success "Ollama is responding."

# 8. Model Acquisition
if ollama list | grep -q "${MODEL_NAME}"; then
    success "Model already downloaded: ${MODEL_NAME}"
else
    log "Pulling model: ${MODEL_NAME}..."
    log "This might take a few minutes depending on your internet speed."
    ollama pull "${MODEL_NAME}" || error "Failed to pull model."
fi

# ------------------------------------------------------------------------------
# Completion
# ------------------------------------------------------------------------------

echo -e "\n${GREEN}===================================================="
echo "🎉 SETUP COMPLETED SUCCESSFULLY"
echo -e "====================================================${NC}"
echo -e "Model installed: ${YELLOW}${MODEL_NAME}${NC}"
echo -e "To start chatting, run:"
echo -e "${BLUE}ollama run ${MODEL_NAME}${NC}"
echo ""
