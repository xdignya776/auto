#!/usr/bin/env python3
"""
Automated Content Generator for Hugo AdSense Site
Generates SEO content using AI (Groq free tier: 14400 req/day)
Supports: Ollama (free/local), Gemini (free tier), Groq (free tier), OpenAI
"""
import os
import time
import hashlib
from datetime import datetime
from pathlib import Path
import requests

# Configuration
HUGO_CONTENT_DIR = Path("/home/dgwgo/opencode/2/adsense-automation/content/posts")
NICHE = "personal finance and insurance"

# High-CPM topics for content generation
TOPIC_LIST = [
    "Term life insurance vs whole life insurance comparison 2026",
    "Best credit cards for cash back rewards 2026",
    "How to choose car insurance for electric vehicles",
    "Personal finance tips for college students 2026",
    "Understanding health insurance deductibles and copays",
    "Best investment apps for beginners 2026",
    "Home insurance tips for first-time buyers",
    "How to improve your credit score fast 2026",
    "Retirement planning strategies for millennials",
    "Top 10 personal finance mistakes to avoid",
]

# AI Backend Selection (set via env var AI_BACKEND: ollama, gemini, groq, openai)
AI_BACKEND = os.getenv("AI_BACKEND", "groq")

# Ollama (free, local)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# Gemini (free tier: 1500 requests/day)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# Groq (free tier: 14400 requests/day)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

# OpenAI (paid)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

def generate_content_with_ai(topic):
    """Generate SEO content for a given topic using selected AI backend"""
    prompt = f"""Write a comprehensive, SEO-optimized blog post about: {topic}

Requirements:
- Title: Create an SEO-friendly H1 title
- Length: 800-1200 words
- Structure: Use H1, H2, H3 headings
- Include a disclaimer: "This content is for informational purposes only and does not constitute financial advice."
- Add a "Key Takeaways" section at the end with 3-5 bullet points
- Write in a professional, authoritative tone
- Include relevant keywords naturally
- Make it unique and original (pass plagiarism checks)
"""

    if AI_BACKEND == "ollama":
        return generate_with_ollama(prompt)
    elif AI_BACKEND == "gemini":
        return generate_with_gemini(prompt)
    elif AI_BACKEND == "groq":
        return generate_with_groq(prompt)
    elif AI_BACKEND == "openai":
        return generate_with_openai(prompt)
    else:
        return generate_with_groq(prompt)  # Default to Groq

def generate_with_ollama(prompt):
    """Generate using local Ollama (free)"""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=60
        )
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        print(f"Ollama error: {e}")
        return None

def generate_with_gemini(prompt):
    """Generate using Gemini free tier"""
    if not GEMINI_API_KEY:
        return None
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(GEMINI_URL, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"Gemini error: {e}")
        return None

def generate_with_groq(prompt):
    """Generate using Groq free tier (14400 req/day)"""
    if not GROQ_API_KEY:
        return None
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": GROQ_MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
    try:
        response = requests.post(GROQ_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Groq error: {e}")
        return None

def generate_with_openai(prompt):
    """Generate using OpenAI API (paid)"""
    if not OPENAI_API_KEY:
        return None
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
    try:
        response = requests.post(OPENAI_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"OpenAI error: {e}")
        return None

def extract_title(content):
    """Extract H1 title from generated content"""
    for line in content.split('\n'):
        if line.startswith('# ') or line.startswith('Title: '):
            return line.replace('# ', '').replace('Title: ', '').strip()
    return "Untitled Post"

def generate_slug(title):
    """Generate URL-friendly slug from title"""
    import re
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')[:80]

def save_to_hugo(title, content, tags=None):
    """Save generated content as Hugo Markdown file"""
    HUGO_CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    slug = generate_slug(title)
    
    # Add frontmatter if not present
    if not content.startswith("---"):
        frontmatter = f"""---
title: "{title}"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}
draft: false
tags: {tags or ['finance', 'insurance']}
---

"""
        content = frontmatter + content
    
    filepath = HUGO_CONTENT_DIR / f"{slug}.md"
    
    # Avoid duplicates
    if filepath.exists():
        hash_suffix = hashlib.md5(title.encode()).hexdigest()[:6]
        filepath = HUGO_CONTENT_DIR / f"{slug}-{hash_suffix}.md"
    
    filepath.write_text(content, encoding="utf-8")
    print(f"Saved: {filepath}")
    return filepath

def main():
    """Main automation loop"""
    print(f"[{datetime.now()}] Starting content generation with {AI_BACKEND}...")
    
    total_generated = 0
    for topic in TOPIC_LIST[:3]:  # Generate 3 posts per run
        print(f"\nProcessing topic: {topic}")
        content = generate_content_with_ai(topic)
        
        if content:
            title = extract_title(content)
            save_to_hugo(title, content)
            total_generated += 1
            time.sleep(2)  # Rate limiting
        else:
            print(f"Failed to generate content for: {topic}")
    
    print(f"\nGenerated {total_generated} articles")
    
    # Git commit if in a git repo
    os.system("cd /home/dgwgo/opencode/2/adsense-automation && git add content/posts/ && git commit -m 'Auto-generated content' && git push 2>/dev/null || true")

if __name__ == "__main__":
    main()
