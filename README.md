# Granitepi-4-Nano

**Date**: 11-01-2025 |
**Version**: 1.0

**Designed by**: *Julian A. Gonzalez* - {[Linkedin](www.linkedin.com/in/julian-g-7b533129a))

**Co-Contributor**: *Thomas Mertens* - ([Linkedin](https://www.linkedin.com/in/tgmertens/))

---

![Raspberry Pi 5](https://img.shields.io/badge/Hardware-Raspberry%20Pi%205-red?logo=raspberrypi)
![Ollama](https://img.shields.io/badge/Framework-Ollama-yellow)
![IBM Granite](https://img.shields.io/badge/Model-IBM%20Granite%204.0-blue)

---

**Run a full-featured large language model entirely on your Raspberry Pi 5 with zero cloud dependency.**

This repository contains a complete, beginner-friendly guide to setting up **IBM Granite 4.0 (350M)** on a Raspberry Pi 5 using **Ollama** for 100% local, private AI inference.

## ✨ Highlights

- 🔒 **100% Private** — All data stays on your device. No cloud, no tracking.
- 🚀 **Blazingly Fast Setup** — From zero to AI in under 45 minutes.
- 💰 **Cost-Effective** — Turn a $80-100 Raspberry Pi into an AI workstation.
- 🌐 **Fully Offline** — Works without internet after initial setup.
- 🎓 **Learn by Doing** — Understand LLMs and edge AI hands-on.


## 📊 Model Specs

| Aspect | Details |
|--------|---------|
| **Model** | IBM Granite 4.0 (350M-H) |
| **Parameters** | 350 Million |
| **Architecture** | Hybrid Mamba-2 (SSM) |
| **Download Size** | ~366 MB |
| **Loaded Size** | ~1.2 GB RAM |
| **Inference Memory** | ~800 MB - 1.2 GB |
| **License** | Apache 2.0 (Open Source) |
| **Languages** | 12+ (English, Spanish, French, German, Japanese, etc.) |

## 🎯 Quick Start (TL;DR)

```bash
# 1. Update system
sudo apt update && sudo apt full-upgrade -y

# 2. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 3. Pull IBM Granite 4.0 model
ollama pull ibm/granite4:350m-h

# 4. Run queries
ollama run ibm/granite4:350m-h "Explain quantum computing in 3 sentences"

# 5. Start interactive chat
ollama run ibm/granite4:350m-h
```

Done! 🎉

## 📖 Full Tutorial

For detailed, step-by-step instructions with troubleshooting, see [**TUTORIAL.md**](TUTORIAL.md).

**Sections covered:**
- System prerequisites and verification
- Ollama installation and setup
- Model download and caching
- Interactive chat and API usage
- Performance optimization
- Comprehensive troubleshooting
- Python integration examples

## 🛠️ Requirements

### Hardware

- **Raspberry Pi 5** with **8GB RAM** (strictly recommended)
- **Official USB-C power supply** (5V 5A)
- **32GB+ SD card** or **NVMe M.2 SSD** (SSD preferred for speed)
- **Active cooling** (heatsink + fan)  (**Recommended**)

### Software

- **Raspberry Pi OS 64-bit** (Bookworm or later)
- **~4GB free storage** (for model)
- Basic terminal familiarity

## 🚀 Getting Started

### Prerequisites Check

Verify 64-bit architecture:

```bash
uname -m  # Should output: aarch64
getconf LONG_BIT  # Should output: 64
```

Check available RAM:

```bash
free -h  # Should show ~7-8GB available
```

### Installation (5 minutes)

1. **Update system:**
   ```bash
   sudo apt update && sudo apt full-upgrade -y
   ```

2. **Install Ollama:**
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

3. **Verify installation:**
   ```bash
   ollama --version
   ```

### Download Model (2-5 minutes)

```bash
ollama pull ibm/granite4:350m-h
```

### Test It

```bash
# Single query
ollama run ibm/granite4:350m-h "What is Python?"

# Interactive mode
ollama run ibm/granite4:350m-h
```

### Performance Tips

```bash
# Keep model loaded (faster subsequent queries)
OLLAMA_KEEP_ALIVE=24h ollama run ibm/granite4:350m-h

# Limit threads for stability (Pi 5 has 4 cores)
OLLAMA_NUM_THREADS=2 ollama run ibm/granite4:350m-h

# Monitor temperature
watch -n 1 'vcgencmd measure_temp'
```

## 💻 Usage Examples

### Command Line

```bash
# Ask a question
ollama run ibm/granite4:350m-h "How do neural networks work?"

# Multi-line prompt
ollama run ibm/granite4:350m-h "
Write a Python function that:
1. Takes a list of numbers
2. Returns the average
3. Handles empty lists
"

# With custom temperature (more creative: 0.0-1.0)
ollama run ibm/granite4:350m-h --temperature 0.8 "Write a haiku about AI"
```

### REST API

```bash
# Query via curl
curl http://localhost:11434/api/generate \
  -d '{
    "model": "ibm/granite4:350m-h",
    "prompt": "Explain dark matter",
    "stream": false
  }'
```

### Python

```python
import requests
import json

def query_ai(prompt):
    response = requests.post('http://localhost:11434/api/generate', 
        json={
            'model': 'ibm/granite4:350m-h',
            'prompt': prompt,
            'stream': False
        }
    )
    return response.json()['response']

result = query_ai("What is quantum entanglement?")
print(result)
```

See [TUTORIAL.md](TUTORIAL.md#api-usage) for more examples.

## 📊 Performance Benchmarks

On **Raspberry Pi 5 (8GB, active cooling)**:

| Task | Speed | Notes |
|------|-------|-------|
| Model load | ~8-12 seconds | Cached after first run |
| Question answer | ~2-5 seconds | For typical 100-token response |
| Throughput | ~30-50 tokens/sec | Decent for ARM edge device |
| Temperature | 55-65°C (normal) | With proper cooling |
| Memory usage | ~1.2 GB peak | Model + buffers |

*Actual performance depends on prompt complexity, ambient temperature, and thermal management.*

## 🔒 Privacy & Security

This setup is **100% private** by design:

✅ **No cloud uploads** — Everything runs locally  
✅ **No internet required** — Works offline  
✅ **No account needed** — No tracking, no sign-ups  
✅ **Open source** — Auditable code  
✅ **Apache 2.0 licensed** — Free for commercial use  

Your data (medical records, proprietary documents, code, personal notes) **never leaves your device**.

## 🐛 Troubleshooting

### Model won't download

```bash
# Retry (resumes from checkpoint)
ollama pull ibm/granite4:350m-h

# Or clear cache and retry
rm -rf ~/.ollama/models/*
ollama pull ibm/granite4:350m-h
```

### System becomes unresponsive

```bash
# Check temperature
vcgencmd measure_temp

# Increase swap (if needed)
sudo nano /etc/dphys-swapfile  # Set CONF_SWAPSIZE=2048

# Restart swap
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### Very slow inference

1. Check CPU temp: `vcgencmd measure_temp` (should be < 70°C)
2. Reduce parallel threads: `OLLAMA_NUM_THREADS=1 ollama run ibm/granite4:350m-h`
3. Add more swap space
4. Use SSD instead of SD card

## 📚 Learn More

### Official Resources

- [Ollama Documentation](https://ollama.ai)
- [IBM Granite Documentation](https://www.ibm.com/granite/docs/)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)

### Related Projects

- [Ollama on GitHub](https://github.com/ollama/ollama)
- [IBM Granite on HuggingFace](https://huggingface.co/ibm-granite)
- [LM Studio (GUI for Ollama models)](https://lmstudio.ai/)
- [Open WebUI (Web interface for Ollama)](https://github.com/open-webui/open-webui)

## 🎓 Advanced Topics

Once you've got the basics working:

1. **Fine-tune Granite 4.0** on your domain data
2. **Build a web interface** using Flask + Ollama API
3. **Integrate with Home Assistant** for smart home voice commands
4. **Deploy multiple Pi's** for distributed inference
5. **Experiment with other models** (TinyLlama, Phi, LLaMA)
6. **Create local RAG pipelines** for document Q&A

## 🤝 Contributing

**Contributions welcome!**

- Found a bug? Open an issue.
- Have a better approach? Submit a PR.
- Benchmarked different hardware? Share your results.
- Created an interesting application? Link it in issues.

## 📝 License

This tutorial and code examples are **Apache 2.0 licensed** — free to use, modify, and distribute.

The **IBM Granite model** is **Apache 2.0 licensed**.

## 🙋 FAQ

**Q: Will this work on older Pi models (Pi 4, Pi 3)?**  
A: Pi 4 *might* work with smaller models (TinyLlama, Phi). Pi 3 is too slow. Pi 5 is strongly recommended.

**Q: How much electricity does it use?**  
A: ~5-7 watts during inference. Very efficient compared to GPUs.

**Q: Do I need a GPU?**  
A: No. This runs on CPU only. Granite 4.0 is designed for ARM processors.

**Q: Why Granite instead of LLaMA or Mistral?**  
A: Granite 4.0 is specifically optimized for small devices with its hybrid Mamba architecture. 350M model fits perfectly on Pi 5. After testing many small models on the RPI 5 Granite models have continously performed well under limited hardware resources.

**Q: Can I run multiple models?**  
A: Yes, but one at a time (memory limited). You can swap between them instantly.

**Q: How do I integrate this into my application?**  
A: Use the REST API. See [Python examples in TUTORIAL.md](TUTORIAL.md#query-via-python).

## 📞 Support

- **Issues/Bugs:** Open a GitHub issue
- **Community:** Join r/ollama, r/raspberry_pi on Reddit, IBM TechXchange
- **Discussions:** GitHub Discussions in this repo

## 🎯 Project Status

✅ **Production Ready** — Tested on Raspberry Pi 5 (8GB)  
✅ **Actively Maintained** — Following Ollama updates  
✅ **Community Supported** — Feedback and contributions welcome  

Last tested: November 2025  
Ollama version: 0.1.20+  
Raspberry Pi OS: Bookworm 64-bit  

---

*Your project here? Create a PR to add it!*

---

**Made with ❤️ for privacy advocates, AI learners, and Raspberry Pi enthusiasts.**

**Ready to get started? Jump to [TUTORIAL.md](TUTORIAL.md)! 🚀**
