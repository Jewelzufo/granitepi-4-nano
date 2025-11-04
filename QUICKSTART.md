# Quickstart

This quick setup Guide will take less than 30 minutes to install `ibm/granite4:350m-h` locally on your `RPI 5`

## Setup

```
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