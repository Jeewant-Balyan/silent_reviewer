# 🚀 Silent Reviewer

Multi-Agent AI Code Reviewer (Local + Parallel Inference)

---

## 🧠 Overview

Silent Reviewer is an AI-based code review system that uses multiple specialized agents (bugs, security, performance, style) running in parallel to analyze code and generate a structured review with a final score and verdict.

---

## ❗ Problem

Manual code reviews are slow and inconsistent. Single-LLM solutions lack specialization and produce mixed-quality outputs.

---

## ✅ Solution

We use a **multi-agent architecture**:

* Each agent focuses on one aspect
* Runs in parallel
* Outputs structured JSON
* Final synthesis agent combines results

---

## ⚙️ Features

* 🐛 Bug detection
* 🔒 Security analysis
* ⚡ Performance optimization
* ✨ Code quality review
* 🧠 Final scoring & grading
* ⚡ Parallel execution (~4× faster)
* 🌐 GitHub file support

---

## 🏗️ Architecture

```
Input Code / GitHub URL
        │
 ┌──────┼─────────────┐
 │      │             │
Bug   Security   Performance
 │      │             │
 └──────┬──────┬──────┘
        │      │
     Style   (merge)
        │
   Synthesis Agent
        │
   Final Report (JSON)
```

---

## 🤖 Model & Infrastructure

* Model: `gemma3:1b`
* Runtime: Ollama (local)
* Endpoint: `http://localhost:11434/api/generate`
* Temperature: 0.2
* Max tokens: 800

### Execution Environment

* Tested on: CPU (Intel i5), 8GB RAM
* Inference: local
* Cost: $0

---

## ⚡ Quick Start (30 seconds)

```bash
git clone <your-repo-url>
cd <repo-name>
pip install -r requirements.txt

ollama serve
ollama pull gemma3:1b

python main.py
```

> ⚠️ Requires Ollama running locally on port 11434

---

## 💡 Example

### Input

```python
def divide(a, b):
    return a / b

print(divide(10, 0))
```

### Output (excerpt)

```json
{
  "issues": [
    {
      "line": 2,
      "severity": "critical",
      "category": "bug",
      "message": "Division by zero possible",
      "fix": "Check if b != 0",
      "confidence": 92
    }
  ],
  "overall_score": 58,
  "grade": "D"
}
```

---

## 📊 Metrics

* Sequential runtime: ~80s
* Parallel runtime: ~20s
* Speed improvement: ~4×
* Avg latency per agent: ~5s
* Cost: $0

### Reliability

* Confidence score per issue (0–100)
* Recommended threshold: >75%

---

## ❌ Known Limitations

* Large files (>500 lines) → slower/inconsistent
* Multi-file projects not supported
* Possible false positives in security checks
* Small model may miss complex bugs

---

## 🎬 Demo

(Add your video link here)

---

## 📂 Project Structure

```
.
├── main.py
├── requirements.txt
└── README.md
```

---

## 🔁 Reproducibility

* Fixed temperature (0.2)
* Same input → similar output
* Minor variation possible due to LLM behavior

---

## 🚀 Future Improvements

* Web UI (Streamlit/React)
* Multi-file repo analysis
* AST-based validation
* Cloud model integration

---

## 🤝 Contribution

Open for improvements and extensions.
