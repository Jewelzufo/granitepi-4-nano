# Running IBM Granite 4.0 Nano Locally on Raspberry Pi 5 with Ollama

**Date**: 11-01-2025 |
**Version**: 1.0

**Designed by**: *Julian A. Gonzalez* - {[Linkedin](www.linkedin.com/in/julian-g-7b533129a))

**Co-Contributor**: *Thomas Mertens* - ([Linkedin](https://www.linkedin.com/in/tgmertens/))

---

## About

A comprehensive step-by-step guide to set up **privacy-focused**, **local AI inference** on your Raspberry Pi 5 using the lightweight IBM Granite 4.0 (350M) model.

## Table of Contents

- [Why Run AI Locally on Raspberry Pi?](#why-run-ai-locally-on-raspberry-pi)
- [Prerequisites](#prerequisites)
- [Pre-Installation System Setup](#pre-installation-system-setup)
- [Step 1: Install Ollama](#step-1-install-ollama)
- [Step 2: Verify Ollama Installation](#step-2-verify-ollama-installation)
- [Step 3: Pull the Granite 4.0 Model](#step-3-pull-the-granite-40-model)
- [Step 4: Run Your First Query](#step-4-run-your-first-query)
- [Step 5: Interactive Chat Mode](#step-5-interactive-chat-mode)
- [Performance Optimization](#performance-optimization)
- [Troubleshooting](#troubleshooting)
- [API Usage](#api-usage)
- [Resources](#resources)

---

## Why Run AI Locally on Raspberry Pi?

**Privacy First:** Your data never leaves your device. No cloud uploads, no tracking, no third-party inference servers.

**Zero Internet Required:** Once the model is downloaded, run queries completely offline.

**Low Cost:** A Raspberry Pi 5 with 8GB RAM (~$80-100) replaces expensive cloud AI subscriptions.

**Learning:** Understand how LLMs work at the edge with a real, functioning AI model running on consumer hardware.

**Portability:** Create a portable AI workstation that fits in your pocket.

---

## Prerequisites

### Hardware Requirements

- **Raspberry Pi 5** with **8GB RAM** (absolutely recommended; 4GB is possible but tight)
- **USB-C Power Supply:** Official 5V 5A power adapter or equivalent USB-C PD supply
- **Storage:** 32GB+ microSD card (U3 or A2-class recommended) OR **NVMe M.2 SSD + adapter** (preferred for faster model loading)
- **Active Cooling:** Heatsink + fan strongly recommended (Granite 4.0 on ARM is CPU-intensive)
- **Stable Internet Connection** (for initial setup and model download only)

### Software Requirements

- **Raspberry Pi OS 64-bit** (Bookworm or later) — 32-bit will NOT work
- **Terminal access** (keyboard/monitor or SSH)
- Basic comfort with Linux command line

### What We're Installing

- **Ollama:** Lightweight framework for running LLMs locally
- **IBM Granite 4.0 (350M-H):** A 350-million-parameter model (~366MB download) with hybrid Mamba-2 architecture
  - Excellent instruction following
  - Supports 12+ languages
  - Apache 2.0 licensed (fully open source)
  - Minimal memory footprint (~800MB-1.2GB RAM during inference)

---

## Pre-Installation System Setup

### Step 1: Verify 64-bit OS and Architecture

Open a terminal and run:

```bash
uname -m
```

**Expected output:** `aarch64`

If you see `armv7l`, your OS is 32-bit. You must install 64-bit Raspberry Pi OS.

Verify the bit size:

```bash
getconf LONG_BIT
```

**Expected output:** `64`

### Step 2: Check Available Resources

Check RAM availability:

```bash
free -h
```

You should see ~7-8GB available (after OS overhead).

Check storage:

```bash
df -h
```

Ensure at least 3-4GB free space for the model.

### Step 3: Update System Packages

Keep your system current:

```bash
sudo apt update && sudo apt full-upgrade -y
```

This may take several minutes. It's worth it for security and compatibility.

### Step 4: Check CPU Temperature (Important!)

```bash
vcgencmd measure_temp
```

Verify your Pi isn't thermally throttled before we start:

```bash
vcgencmd get_throttled
```

**Expected output:** `throttled=0x0`

If you see a different value, your system is throttling. Install better cooling before proceeding.

### Step 5: Increase Swap Space (Optional but Recommended)

Raspberry Pi's default swap is limited. For better stability during model inference, increase it:

```bash
sudo nano /etc/dphys-swapfile
```

Find the line `CONF_SWAPSIZE=100` and change it to `CONF_SWAPSIZE=2048` (2GB of swap).

Save and exit (`Ctrl+X`, then `Y`, then `Enter`).

Apply the change:

```bash
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

Restart the swap service:

```bash
sudo systemctl restart dphys-swapfile
```

---

## Step 1: Install Ollama

Ollama provides an official installation script optimized for ARM64 (Raspberry Pi's architecture).

### Download and Run the Ollama Installer

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

The script will:

- Download the ARM64 binary bundle
- Create an `ollama` system user
- Set up systemd service for auto-start
- Configure permissions

Wait for completion (takes 1-3 minutes depending on internet speed).

---

## Step 2: Verify Ollama Installation

Check if Ollama installed correctly:

```bash
ollama --version
```

You should see something like: `ollama version is 0.X.X`

Verify the Ollama service is running:

```bash
systemctl status ollama
```

You should see: `Active: active (running)`

If it's not running, start it:

```bash
sudo systemctl start ollama
```

### Optional: Enable Auto-Start on Boot

```bash
sudo systemctl enable ollama
```

---

## Step 3: Pull the Granite 4.0 Model

Now download and configure the IBM Granite 4.0 (350M-H) model. This is a one-time download (~366MB, unpacks to ~1.2GB).

```bash
ollama pull ibm/granite4:350m-h
```

**What's happening:**

- Ollama connects to the Ollama registry
- Downloads the quantized model weights
- Caches them locally in `~/.ollama/models/`
- Sets up tokenizers and configs

⏱️ **Estimated time:** 2-5 minutes (depends on internet speed)

**Verify the download completed:**

```bash
ollama list
```

You should see:

```
NAME                        ID          SIZE      MODIFIED
ibm/granite4:350m-h         ...         366 MB    5 minutes ago
```

---

## Step 4: Run Your First Query

Test the model with a simple query:

```bash
ollama run ibm/granite4:350m-h "Explain quantum computing in 3 sentences"
```

**First run behavior:** The model loads into memory (this takes 10-30 seconds), then processes your prompt.

You'll see output like:

```
Quantum computing is a type of computing that uses quantum bits (qubits) 
instead of classical bits, allowing it to process information in a fundamentally 
different way. Unlike classical bits that are either 0 or 1, qubits can exist in 
a state called superposition, where they are both 0 and 1 simultaneously. This 
enables quantum computers to solve certain problems exponentially faster than 
classical computers, particularly in areas like cryptography, optimization, and 
drug discovery.
```

At the bottom, you'll see timing metrics:

```
total duration:       12.34s
load duration:        8.12s    (model loading into RAM)
prompt eval count:    25 token(s)
prompt eval duration: 1.23s
eval count:           120 token(s)
eval duration:        2.79s
eval rate:           43.01 tokens/sec
```

This is normal on Raspberry Pi (slower than GPUs, but respectable for ARM).

---

## Step 5: Interactive Chat Mode

For multi-turn conversations, run the model in interactive mode:

```bash
ollama run ibm/granite4:350m-h
```

You'll enter an interactive shell:

```
>>> Send a message (/? for help)
```

Type your prompt and press Enter:

```
>>> What are the best practices for Python exception handling?
```

The model generates a response. Continue the conversation:

```
>>> Can you give me a code example?
```

The model maintains context from previous messages in the session.

**Available commands in interactive mode:**

- Type your question normally to get a response
- `/exit` — Exit the chat
- `/?` — Show help

Try it:

```
>>> /? 
```

To exit, type:

```
>>> /exit
```

---

## Performance Optimization

### 1. Reduce Model Load Time

By default, Ollama unloads the model after 5 minutes of inactivity. Keep it loaded:

```bash
OLLAMA_KEEP_ALIVE=24h ollama run ibm/granite4:350m-h
```

Or set it permanently in the Ollama service:

```bash
sudo systemctl edit ollama
```

Add under `[Service]`:

```
Environment="OLLAMA_KEEP_ALIVE=24h"
```

Save and restart:

```bash
sudo systemctl restart ollama
```

### 2. Optimize CPU Threading

Check your Pi's CPU count:

```bash
nproc
```

By default, Ollama uses all cores. For stability, limit to half:

```bash
OLLAMA_NUM_THREADS=2 ollama run ibm/granite4:350m-h
```

(Raspberry Pi 5 has 4 cores, so 2 threads provides good balance)

### 3. Monitor Temperature During Use

In another terminal, watch the CPU temperature while running queries:

```bash
watch -n 1 'vcgencmd measure_temp && vcgencmd get_throttled'
```

Temperatures:

- ✅ **Under 60°C:** Safe and normal
- ⚠️ **60-70°C:** Getting warm, consider better cooling
- 🔴 **Over 80°C:** Thermal throttling occurring, reduce load

### 4. Use Faster Storage (If Possible)

If you're using a microSD card, model loading is slow. Consider upgrading to **NVMe M.2 SSD** with a USB adapter for dramatically faster load times.

### 5. Adjust Swap Size for Heavy Use

If running multiple simultaneous queries, increase swap:

```bash
sudo nano /etc/dphys-swapfile
```

Set `CONF_SWAPSIZE=4096` for 4GB swap (trades speed for stability).

---

## Troubleshooting

### Issue: "command not found: ollama"

**Solution:** Ollama isn't in your PATH. Either:

1. Restart your terminal session
2. Or add Ollama to PATH manually:

```bash
export PATH=$PATH:/usr/local/bin
```

### Issue: Model fails to download ("connection timeout")

**Possible causes:**

- Weak WiFi signal
- Network congestion
- Ollama registry temporarily unavailable

**Solution:** Retry the pull:

```bash
ollama pull ibm/granite4:350m-h
```

Ollama resumes from where it left off.

### Issue: "Error: out of memory" or system becomes unresponsive

**Possible causes:**

- Insufficient available RAM
- Too many other processes running
- Swap not configured

**Solutions:**

1. Check memory:

```bash
free -h
```

2. Close unnecessary applications (e.g., stop GUI desktop)

3. Increase swap space (see Performance Optimization section)

4. Try a smaller batch size:

```bash
OLLAMA_NUM_PARALLEL=1 ollama run ibm/granite4:350m-h
```

### Issue: Model runs very slowly (tokens/sec < 5)

**Possible causes:**

- Thermal throttling (CPU overheating)
- Insufficient swap
- Running other heavy processes

**Solutions:**

1. Check thermal status:

```bash
vcgencmd measure_temp && vcgencmd get_throttled
```

If `throttled != 0x0`, improve cooling.

2. Verify swap is configured:

```bash
free -h
```

Look for swap space in the `Swap:` row.

3. Kill background processes:

```bash
ps aux | grep -E '(node|python|java)'
```

### Issue: "ollama pull" returns "failed to resolve host"

**Problem:** Network connectivity issue

**Solution:**

```bash
ping 8.8.8.8
```

If ping fails, check your WiFi connection or ethernet cable.

### Issue: Granite model won't run with error "GGML format not supported"

**Cause:** Ollama version mismatch or corrupt cache

**Solution:** Clear Ollama cache and retry:

```bash
rm -rf ~/.ollama/models/*
ollama pull ibm/granite4:350m-h
```

Then run again:

```bash
ollama run ibm/granite4:350m-h
```

---

## API Usage

Once Ollama is running, you can query it programmatically via REST API. This is powerful for building applications.

### Start Ollama Service (If Not Running)

```bash
ollama serve
```

Or if you've set up systemd, it runs automatically in the background.

### Query via curl (Terminal)

```bash
curl http://localhost:11434/api/generate \
  -d '{
    "model": "ibm/granite4:350m-h",
    "prompt": "What is machine learning?",
    "stream": false
  }' \
  | python3 -m json.tool
```

Example response:

```json
{
  "response": "Machine learning is a subset of artificial intelligence...",
  "context": [1, 2, 3, ...],
  "total_duration": 5234000000,
  "load_duration": 1234000000,
  "prompt_eval_count": 10,
  "eval_count": 85
}
```

### Query via Python

Create a file `query_granite.py`:

```python
#!/usr/bin/env python3

import requests
import json

def query_granite(prompt, model="ibm/granite4:350m-h"):
    """Query the Granite model via Ollama API"""
    
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        
        # Print the response
        print(f"\n{'='*60}")
        print(f"Model: {data.get('model')}")
        print(f"{'='*60}")
        print(data.get('response', 'No response'))
        print(f"{'='*60}")
        
        # Print timing stats
        total_duration_ms = data.get('total_duration', 0) / 1_000_000
        eval_count = data.get('eval_count', 0)
        tokens_per_sec = (eval_count / (total_duration_ms / 1000)) if total_duration_ms > 0 else 0
        
        print(f"Total time: {total_duration_ms:.2f}ms")
        print(f"Tokens generated: {eval_count}")
        print(f"Speed: {tokens_per_sec:.2f} tokens/sec")
        print(f"{'='*60}\n")
        
        return data.get('response')
    
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to Ollama. Is it running? Try: ollama serve")
        return None
    except requests.exceptions.Timeout:
        print("Error: Request timed out")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    # Example queries
    prompts = [
        "What is the capital of France?",
        "Explain photosynthesis briefly",
        "Write a Python function to check if a number is prime"
    ]
    
    for prompt in prompts:
        print(f"\nPrompt: {prompt}")
        query_granite(prompt)
```

Run it:

```bash
python3 query_granite.py
```

### Streaming Responses (Long Outputs)

For longer generations, enable streaming:

```bash
curl http://localhost:11434/api/generate \
  -d '{
    "model": "ibm/granite4:350m-h",
    "prompt": "Write a short story about a robot",
    "stream": true
  }'
```

The API returns tokens in real-time (useful for large responses).

---

## Resources

### Official Documentation

- **Ollama**: <https://ollama.ai/>
- **IBM Granite Docs**: <https://www.ibm.com/granite/docs/>
- **Ollama Granite Model Page**: <https://ollama.com/library/granite4>
- **Ollama API Reference**: <https://github.com/ollama/ollama/blob/main/docs/api.md>

### Model Information

- **Model License:** Apache 2.0 (fully open source)
- **Parameters:** 350 million (hybrid Mamba-2 architecture)
- **Context Length:** 1M tokens (very long context support)
- **Supported Languages:** English, German, Spanish, French, Japanese, Portuguese, Arabic, Czech, Italian, Korean, Dutch, Chinese

### Community

- **GitHub:** <https://github.com/ollama/ollama>
- **Discussions:** <https://github.com/ollama/ollama/discussions>
- **Reddit:** r/ollama, r/raspberry_pi

---

## Privacy & Security Notes

This setup is entirely **local and private**:

✅ **No data sent to the cloud** — Everything runs on your Pi
✅ **No account required** — No login, no tracking
✅ **Works offline** — No internet needed after model download
✅ **Open source** — Transparent, auditable code
✅ **Apache 2.0 licensed** — Commercial use allowed

Your sensitive documents, code, medical records, etc. never leave your device.

---

## What's Next?

1. **Fine-tune the model** on your domain-specific data
2. **Build a web UI** using Flask/FastAPI + Ollama API
3. **Integrate into Home Assistant** for voice commands
4. **Deploy to multiple Pis** for distributed inference
5. **Experiment with other models** (TinyLlama, Phi, LLaMA 3)
6. **Contribute to the community** with your insights and projects

---

## Support & Feedback

- Found a bug or have suggestions? Open an issue on GitHub
- Want to showcase your project? Share in the Ollama community
- Struggling? Check the troubleshooting section or ask in Reddit communities

---

**Happy local AI'ing! 🚀**

Your Raspberry Pi is now a privacy-first AI workstation.
