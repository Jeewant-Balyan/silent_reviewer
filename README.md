# 🔍 Silent Reviewer

> **Multi-agent AI code reviewer that runs 100% locally on a 1B model.**  
> No internet. No API key. No cloud. Just your laptop and Ollama.

---

## What it does

Drop any code file. Four specialized AI agents — each focused on ONE job — review it in parallel and produce a PR-style report with severity ratings, confidence scores, and exact fixes.

| Agent | Job |
|---|---|
| 🐛 Bug Hunter | Logical bugs, null errors, off-by-one, wrong conditions |
| 🔒 Security Scanner | SQL injection, hardcoded secrets, unsafe deserialization |
| ⚡ Performance Analyzer | Nested loops, inefficient structures, repeated computation |
| ✨ Style & Practices | Naming, magic numbers, god functions, missing docstrings |
| 🧠 Synthesis Agent | Final score /100, grade, top priority fix |

**Model:** Gemma3 1B via Ollama — **Tier 1** (≤4B params)  
**Runs:** 100% offline, zero cloud calls, works on any laptop with 8GB RAM

---

## Quick start (5 minutes)

### 1. Install Ollama
```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows: download from https://ollama.com
```

### 2. Pull the model
```bash
ollama pull gemma3:1b
```

### 3. Install Python deps
```bash
pip install flask requests
```

### 4. Run the web app
```bash
python app.py
# Open http://localhost:5000
```

### Or use the CLI
```bash
python cli.py your_code.py
python cli.py demo_buggy_code.py   # Try the demo!
```

---

## Demo

Run the included demo file to see the reviewer catch real issues:
```bash
python cli.py demo_buggy_code.py
```

It will find:
- SQL injection vulnerability (security, critical)
- Hardcoded password (security, critical)  
- Off-by-one error in loop (bug, critical)
- MD5 password hashing (security, warning)
- Unsafe pickle deserialization (security, critical)
- Inefficient list concatenation in loop (performance)
- God function with 6 responsibilities (style)

---

## Engineering highlights

### Why multi-agent works on a 1B model
A single 1B model asked to "review all issues" gets confused and misses things.  
Four agents each with ONE strict job = dramatically better results.  
Each agent's system prompt forbids it from looking at other categories — this forces focus.

### Confidence scores
Every issue includes a confidence % (50–100%). This is honest about model limitations.  
High confidence (>75%) = reliable finding. Low confidence = flag for human review.

### Structured JSON output with retry
Each agent is prompted to return strict JSON. If parsing fails, the code extracts  
JSON from anywhere in the response, then falls back to safe defaults. Zero crashes.

### Context trimming
Code is trimmed to 8000 chars before sending to the model — prevents context overflow  
which is the #1 cause of bad output from tiny models.

---

## Project structure
```
silent_reviewer/
├── app.py              # Flask web server + UI
├── cli.py              # Terminal CLI version
├── reviewer.py         # Multi-agent pipeline (core logic)
├── demo_buggy_code.py  # Demo file with intentional issues
└── requirements.txt
```

---

## Hackathon submission notes

**Model tier:** Tier 1 — Gemma3 1B (1 billion parameters, ~800MB)  
**Key techniques:**
- Multi-agent pipeline (4 specialized agents + synthesis)
- Strict JSON structured output with validation retry loop
- Confidence scoring for honest limitation disclosure
- Context window management for tiny models

**Where the model still fails:**  
- Complex multi-file logic bugs (only reviews one file at a time)  
- Language-specific idioms beyond common patterns  
- Very long functions (>200 lines) where context gets fragmented  

These are known limitations addressed by: file-by-file review, context trimming, and confidence scores that flag uncertain findings for human verification.
