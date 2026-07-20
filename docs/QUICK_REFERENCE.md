# Quick Reference Card: Granite 4.0 on Raspberry Pi 5

**Date**: 11-01-2025 |
**Version**: 1.0

**Designed by**: *Julian A. Gonzalez* - {[Linkedin](www.linkedin.com/in/julian-g-7b533129a))

**Co-Contributor**: *Thomas Mertens* - ([Linkedin](https://www.linkedin.com/in/tgmertens/))

---

## Installation (One-Time Setup)

```bash
# 1. Update system
sudo apt update && sudo apt full-upgrade -y

# 2. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 3. Verify
ollama --version

# 4. Download model (~366MB)
ollama pull ibm/granite4:350m-h

# 5. Verify download
ollama list
```

---

## Basic Commands

### Interactive Chat Mode

```bash
ollama run ibm/granite4:350m-h
# Type your questions, /exit to quit
```

### Single Query

```bash
ollama run ibm/granite4:350m-h "Your question here"
```

### With Temperature (Creativity Level)

```bash
ollama run ibm/granite4:350m-h --temperature 0.8 "Be creative!"
```

### See All Models

```bash
ollama list
```

### Remove a Model

```bash
ollama rm ibm/granite4:350m-h
```

### Service Control

```bash
sudo systemctl start ollama      # Start service
sudo systemctl stop ollama       # Stop service
sudo systemctl restart ollama    # Restart service
sudo systemctl status ollama     # Check status
sudo systemctl enable ollama     # Auto-start on boot
```

---

## Performance Tuning

### Keep Model Loaded (No Reload Delay)

```bash
OLLAMA_KEEP_ALIVE=24h ollama run ibm/granite4:350m-h
```

### Limit CPU Threads (Pi 5 = 4 cores, use 2-3)

```bash
OLLAMA_NUM_THREADS=2 ollama run ibm/granite4:350m-h
```

### Combined

```bash
OLLAMA_KEEP_ALIVE=24h OLLAMA_NUM_THREADS=2 ollama run ibm/granite4:350m-h
```

### Make It Permanent

```bash
sudo systemctl edit ollama
# Add under [Service]:
# Environment="OLLAMA_KEEP_ALIVE=24h"
# Environment="OLLAMA_NUM_THREADS=2"
# Save and exit (Ctrl+X, Y, Enter)

sudo systemctl restart ollama
```

---

## System Monitoring

### Check CPU Temperature

```bash
vcgencmd measure_temp
# Safe: < 60°C | Warm: 60-70°C | Throttling: > 80°C
```

### Check for Thermal Throttling

```bash
vcgencmd get_throttled
# Expected: throttled=0x0 (no throttling)
```

### Real-Time Temperature Monitoring

```bash
watch -n 1 'vcgencmd measure_temp && vcgencmd get_throttled'
# Press Ctrl+C to exit
```

### Check RAM Usage

```bash
free -h
# Should show ~7-8GB available
```

### Check Storage Space

```bash
df -h
# Ensure at least 3-4GB free for model
```

### Check Running Processes

```bash
ps aux | grep ollama
```

---

## Troubleshooting Quick Fixes

### "ollama: command not found"

```bash
export PATH=$PATH:/usr/local/bin
# Or restart your terminal
```

### Model Won't Download

```bash
# Retry (resumes from checkpoint)
ollama pull ibm/granite4:350m-h

# Or clear and re-download
rm -rf ~/.ollama/models/*
ollama pull ibm/granite4:350m-h
```

### Out of Memory / System Unresponsive

```bash
# Increase swap
sudo nano /etc/dphys-swapfile
# Change: CONF_SWAPSIZE=2048

sudo dphys-swapfile setup && sudo dphys-swapfile swapon
```

### Very Slow Inference (< 10 tokens/sec)

```bash
# 1. Check temperature (should be < 70°C)
vcgencmd measure_temp

# 2. Reduce threads
OLLAMA_NUM_PARALLEL=1 ollama run ibm/granite4:350m-h

# 3. Kill background processes
killall chromium python3 node  # Be careful!
```

### Model Loaded But Won't Generate

```bash
# Check if service is running
systemctl status ollama

# Restart service
sudo systemctl restart ollama

# Try again
ollama run ibm/granite4:350m-h "test"
```

---

## REST API (Programmatic Access)

### Query via curl

```bash
curl http://localhost:11434/api/generate \
  -d '{
    "model": "ibm/granite4:350m-h",
    "prompt": "Your question here",
    "stream": false
  }'
```

### Streaming (Real-Time Tokens)

```bash
curl http://localhost:11434/api/generate \
  -d '{
    "model": "ibm/granite4:350m-h",
    "prompt": "Your question here",
    "stream": true
  }'
```

### Python Query

```python
import requests

response = requests.post('http://localhost:11434/api/generate',
    json={
        'model': 'ibm/granite4:350m-h',
        'prompt': 'Your question',
        'stream': False
    }
)

print(response.json()['response'])
```

---

## Model Information

| Property | Value |
|----------|-------|
| Model Name | IBM Granite 4.0 (350M-H) |
| Parameters | 350 Million |
| Architecture | Hybrid Mamba-2 (SSM) |
| Download Size | ~366 MB |
| Loaded Size | ~1.2 GB |
| Context Length | 1 Million tokens |
| License | Apache 2.0 |
| Speed (Pi 5) | ~30-50 tokens/sec |
| Languages | English, Spanish, French, German, Japanese, Portuguese, Arabic, Czech, Italian, Korean, Dutch, Chinese |

---

## File Locations

```
Ollama binary:       /usr/local/bin/ollama
Model cache:         ~/.ollama/models/
System service:      /etc/systemd/system/ollama.service
Config:              ~/.ollama/ollama
```

---

## Useful Resources

- **Ollama Docs**: <https://ollama.ai>
- **Granite Docs**: <https://www.ibm.com/granite/docs/>
- **Ollama API**: <https://github.com/ollama/ollama/blob/main/docs/api.md>
- **Pi Docs**: <https://www.raspberrypi.com/documentation/>
- **GitHub**: <https://github.com/ollama/ollama>

---

## Environment Variables (Advanced)

```bash
OLLAMA_HOST                    # API server address (default: localhost:11434)
OLLAMA_KEEP_ALIVE              # How long to keep model in RAM (default: 5m)
OLLAMA_NUM_PARALLEL            # Parallel requests (default: 1)
OLLAMA_NUM_THREADS             # CPU threads (default: all cores)
OLLAMA_MAX_LOADED_MODELS       # Max models in memory (default: 1)
OLLAMA_MODELS                  # Custom models directory
```

Example:

```bash
OLLAMA_KEEP_ALIVE=24h OLLAMA_NUM_THREADS=3 ollama serve
```

---

## Performance Benchmarks

### Expected Performance on Pi 5 (8GB, Active Cooling)

```
First prompt:     ~15-20 seconds (includes model load)
Subsequent:       ~2-5 seconds (warm model)
Speed:            ~30-50 tokens/sec
Memory peak:      ~1.2 GB
Temperature:      55-70°C (normal)
CPU usage:        80-95% during inference
```

---

## 🔒 Privacy Checkpoints

✅ No data sent to cloud  
✅ No internet required after setup  
✅ No account/login needed  
✅ Everything runs locally  
✅ Open source code  
✅ Apache 2.0 license  

**Your data stays on your Pi device! 🛡️**

---

## Common Prompts to Try

```bash
# General knowledge
ollama run ibm/granite4:350m-h "What is photosynthesis?"

# Code generation
ollama run ibm/granite4:350m-h "Write a Python function to check if a number is prime"

# Analysis
ollama run ibm/granite4:350m-h "Analyze the pros and cons of remote work"

# Creative
ollama run ibm/granite4:350m-h "Write a haiku about technology"

# Problem solving
ollama run ibm/granite4:350m-h "How do I troubleshoot a Raspberry Pi that won't boot?"
```

---

## 📞 Support

- **Full Tutorial**: See TUTORIAL.md
- **Issues**: GitHub Issues
- **Community**: r/ollama, r/raspberry_pi
- **Documentation**: <https://ollama.ai>

---

**Bookmark this card! It has everything you need at a glance. 📌**

*Last updated: November 2025*
