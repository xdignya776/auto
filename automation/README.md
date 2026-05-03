# AI Backend Options (All Free Options Available)

## Option 1: Ollama (Completely Free, Local)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3.2

# Run script
export AI_BACKEND=ollama
python automation/generate_content.py
```

## Option 2: Gemini (Free Tier - 1500 req/day)
1. Get free API key: https://aistudio.google.com/app/apikey
2. Set environment:
```bash
export AI_BACKEND=gemini
export GEMINI_API_KEY="your-key"
python automation/generate_content.py
```

## Option 3: Groq (Free Tier - 14400 req/day)
1. Get free API key: https://console.groq.com/keys
2. Set environment:
```bash
export AI_BACKEND=groq
export GROQ_API_KEY="your-key"
python automation/generate_content.py
```

## Option 4: OpenAI (Paid)
```bash
export AI_BACKEND=openai
export OPENAI_API_KEY="your-key"
python automation/generate_content.py
```

## Recommended: Gemini (best free option)
- 1500 requests/day free
- Good quality output
- No server setup needed
