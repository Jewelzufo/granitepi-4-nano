<h1 align="center">GranitePi-4-Nano</h1>

<p align="center">
  <img src="https://github.com/Jewelzufo/granitepi-4-nano/blob/main/granitepi4.jpg?raw=true" width="600" height="400" alt="GranitePi-4-Nano Banner">
</p>

<div align="center">

**Date**: 11-01-2025 | **Version**: 1.1

**Designed by**: *Julian A. Gonzalez* - ([LinkedIn](https://www.linkedin.com/in/julian-g-7b533129a))  
**Co-Contributor**: *Thomas Mertens* - ([LinkedIn](https://www.linkedin.com/in/tgmertens/))

---

![Raspberry Pi 5](https://img.shields.io/badge/Hardware-Raspberry%20Pi%205-red?logo=raspberrypi)
![Ollama](https://img.shields.io/badge/Framework-Ollama-yellow)
![IBM Granite](https://img.shields.io/badge/Model-IBM%20Granite%204.0-blue)
![License](https://img.shields.io/badge/License-Apache%202.0-green)

</div>

**Run a full-featured large language model entirely on your Raspberry Pi 5 with zero cloud dependency.**

This repository contains a complete, beginner-friendly guide to setting up **IBM Granite 4.0 (350M)** on a Raspberry Pi 5 using **Ollama** for 100% local, private AI inference. It utilizes a highly optimized GGUF quantization (`unsloth_granite-4.0-h-350m-GGUF`) to ensure smooth performance on edge hardware.

## ✨ Highlights

- 🔒 **100% Private** — All data stays on your device. No cloud, no tracking.
- 🚀 **One-Click Setup** — Automated script handles dependencies, safety checks, and installation.
- ⚡ **Optimized Performance** — Uses specific quantization and thread settings for the Pi 5 CPU.
- 💰 **Cost-Effective** — Turn a standard Raspberry Pi into an AI workstation.
- 🌐 **Fully Offline** — Works without internet after initial setup.

## 📊 Model Specs

| Aspect | Details |
|--------|---------|
| **Model** | `jewelzufo/unsloth_granite-4.0-h-350m-GGUF` |
| **Parameters** | 350 Million |
| **Architecture** | Hybrid Mamba-2 (SSM) |
| **Download Size** | ~366 MB |
| **Loaded Size** | ~1.2 GB RAM |
| **Inference Memory** | ~800 MB - 1.2 GB |
| **License** | Apache 2.0 (Open Source) |
| **Languages** | 12+ (English, Spanish, French, German, Japanese, etc.) |

---

## System Architecture

<div align="center">
  <img src="https://github.com/Jewelzufo/granitepi-4-nano/blob/main/architecture-pi.jpg?raw=true" alt="system diagram" height="900" width="900">
</div>

---

## 🎯 Quick Start (TL;DR)

We provide an automated setup script that verifies your hardware (RAM, Disk, Thermals) and installs the necessary components.

```bash
# 1. Clone the repository
git clone [https://github.com/Jewelzufo/granitepi-4-nano.git](https://github.com/Jewelzufo/granitepi-4-nano.git)
cd granitepi-4-nano

# 2. Make the setup script executable
chmod +x setup.sh

# 3. Run the automated installer
./setup.sh

# 4. Start chatting
ollama run jewelzufo/unsloth_granite-4.0-h-350m-GGUF

```

Done! 🎉

## 🛠️ Requirements

### Hardware

* **Raspberry Pi 5**
* **RAM**: 8GB recommended (4GB minimum supported with warnings).
* **Storage**: At least 5GB free space required (SSD preferred for speed).
* **Cooling**: Active cooling (heatsink + fan) is **strongly recommended** to prevent thermal throttling during inference.


* **Power**: Official USB-C power supply (5V 5A).

### Software

* **Raspberry Pi OS 64-bit** (Bookworm or later).
* Basic terminal familiarity.

## 🚀 Detailed Installation

### 1. Automated Setup (`setup.sh`)

The included `setup.sh` script is the safest way to deploy. It performs the following actions:

* **Validates Architecture**: Ensures you are running on a 64-bit OS.
* **Checks Hardware**: Verifies sufficient RAM, disk space, and safe CPU temperatures.
* **Optimizes Swap**: Configures a 2GB swap file to prevent out-of-memory crashes.
* **Installs Ollama**: Sets up the inference engine and applies performance overrides (2 threads, 24h keep-alive).
* **Downloads Model**: Pulls the optimized GGUF version of Granite 4.0.

### 2. Manual Verification

If you prefer to check your system manually before running the script:

```bash
# Verify 64-bit architecture
uname -m  # Output: aarch64

# Check available RAM
free -h   # Look for 'Available' column

# Check CPU temperature
vcgencmd measure_temp # Should be < 75°C

```

## 💻 Usage Examples

### Command Line

Once installed, interact with the model directly using the model ID configured in the setup:

```bash
# Ask a question
ollama run jewelzufo/unsloth_granite-4.0-h-350m-GGUF "How do neural networks work?"

# Multi-line prompt
ollama run jewelzufo/unsloth_granite-4.0-h-350m-GGUF "
Write a Python function that:
1. Takes a list of numbers
2. Returns the average
3. Handles empty lists
"

```

### Python Integration

You can integrate Granite 4.0 into your Python scripts using the Ollama API. See `examples/basic_query.py` for a starter script.

```python
import requests

def query_ai(prompt):
    response = requests.post('http://localhost:11434/api/generate', 
        json={
            'model': 'jewelzufo/unsloth_granite-4.0-h-350m-GGUF',
            'prompt': prompt,
            'stream': False
        }
    )
    return response.json()['response']

print(query_ai("What is quantum entanglement?"))

```

## 📊 Performance Benchmarks

On **Raspberry Pi 5 (8GB, active cooling)**:

| Task | Speed | Notes |
| --- | --- | --- |
| Model load | ~8-12 seconds | Cached after first run |
| Question answer | ~2-5 seconds | For typical 100-token response |
| Throughput | ~30-50 tokens/sec | Excellent for ARM edge device |
| Temperature | 55-65°C | With proper cooling |
| Memory usage | ~1.2 GB peak | Model + buffers |

## 🔒 Privacy & Security

This setup is **100% private** by design:
✅ **No cloud uploads** — Everything runs locally.

✅ **No internet required** — Works offline after initial download.

✅ **No account needed** — No tracking, no sign-ups.

Your data (medical records, proprietary documents, code) **never leaves your device**.

## 🐛 Troubleshooting

**Setup script fails on "Insufficient disk space"**
Free up space or expand your partition. The script requires 5GB safety buffer.

**Model is slow or system freezes**

* Check your temperature: `vcgencmd measure_temp`.
* Ensure the setup script successfully configured the 2GB swap file.
* Try reducing threads manually: `OLLAMA_NUM_THREADS=1 ollama run ...`

**"Server not responding"**
The setup script includes a wait loop, but if it fails, try restarting the service:

```bash
sudo systemctl restart ollama

```

## 🤝 Contributing

**Contributions welcome!**

* Found a bug? Open an issue.
* Have a better approach? Submit a PR.
* Benchmarked different hardware? Share your results.

## 📝 License

This tutorial and code examples are **Apache 2.0 licensed**. The **IBM Granite model** is also **Apache 2.0 licensed**.

---

**Made with ❤️ for privacy advocates, AI learners, and Raspberry Pi enthusiasts.**
