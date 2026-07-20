#!/bin/bash

echo "========================================"
echo "📊 GranitePi-4 Quantized Benchmark"
echo "========================================"

# 1. System Health Checks
echo -e "\n1. Checking Hardware Stability..."
vcgencmd measure_temp && vcgencmd get_throttled

# 2. Model Pull
echo -e "\n2. Ensuring Quantized Model is local..."
ollama pull jewelzufo/unsloth_granite-4.0-h-350m-GGUF

# 3. Model Inference Test
echo -e "\n3. Running Test Inference..."
echo "   Prompt: 'Explain quantum computing in 3 sentences'"
echo "   ----------------------------------------"

START_TIME=$(date +%s%N)

# Run query
ollama run jewelzufo/unsloth_granite-4.0-h-350m-GGUF "Explain quantum computing in 3 sentences"

END_TIME=$(date +%s%N)
DURATION=$((($END_TIME - $START_TIME)/1000000))

echo -e "\n   ----------------------------------------"
echo "   ✅ Benchmark Complete."
echo "   ⏱️ Total Execution Time: ${DURATION}ms"
