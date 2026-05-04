# 🚀 Silent Reviewer

### Multi-Agent AI Code Reviewer using Tier-1 Models

---

## 🧠 Overview

Silent Reviewer is a multi-agent AI system that performs automated code reviews using **multiple specialized agents running in parallel**.

Instead of relying on a single large model, it uses a **lightweight Tier-1 model (`gemma3:1b`)** and improves performance through system design — task decomposition, parallel execution, and structured synthesis.

---

## ❗ Problem

Traditional code reviews are:

* slow and manual
* inconsistent across reviewers
* difficult to scale

Most AI solutions rely on a **single large model**, which mixes multiple concerns and reduces reliability.

---

## ✅ Solution

Silent Reviewer breaks code review into independent tasks:

* bug detection
* security analysis
* performance optimization
* code quality evaluation

Each task is handled by a separate agent, and all agents run **in parallel**, producing structured outputs that are combined into a final result.

---

## 🎯 Alignment with Garage Inference

This project follows the Garage Inference principle:

> **Use Tier-1 models in a system instead of relying on a single large model**

* Uses a lightweight model (`gemma3:1b`)
* Builds intelligence through **multi-agent architecture**
* Achieves better results through **parallel collaboration**

> Instead of scaling model size, this system scales structure.

---

## ⚙️ Features

* 🐛 Bug detection agent
* 🔒 Security scanner
* ⚡ Performance analyzer
* ✨ Style & best practices reviewer
* 🧠 Final synthesis (score + grade + verdict)
* ⚡ Parallel execution (~4× faster)
* 🌐 GitHub file analysis support

---

## 🏗️ Architecture

```id="arch01"
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
* Model class: **Tier-1 (lightweight, local, efficient)**
* Runtime: Ollama (local inference)
* Endpoint: `http://localhost:11434/api/generate`
* Temperature: 0.2
* Max tokens: 800

### Execution Environment

* Tested on: CPU (Intel i5), 8GB RAM
* Inference: local (no external API)
* Cost: $0

---

## ⚡ Quick Start

```bash id="qs01"
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

```python id="ex01"
def divide(a, b):
    return a / b

print(divide(10, 0))
```

### Output (excerpt)

```json id="ex02"
{
  "issues": [
    {
      "line": 2,
      "severity": "critical",
      "category": "bug",
      "message": "Division by zero possible",
      "fix": "Check if b != 0 before division",
      "confidence": 92
    }
  ],
  "overall_score": 58,
  "grade": "D"
}
```

---

## 📊 Performance & Metrics

* Sequential runtime: ~80 seconds
* Parallel runtime: ~20 seconds
* Speed improvement: ~4×
* Avg latency per agent: ~5 seconds
* Cost: $0

### Reliability

* Confidence score per issue (0–100)
* Recommended threshold: >75%
* Bottleneck: LLM inference latency

---

## 🧠 Key Design Insight

Instead of increasing model size, the system improves performance by:

* decomposing tasks
* running agents in parallel
* synthesizing structured outputs

This allows smaller models to approximate capabilities of larger systems.

---

## ❌ Known Limitations

* Large files (>500 lines) → slower or inconsistent
* Multi-file repositories not supported
* Possible false positives in security analysis
* Smaller model may miss complex issues
* Results depend on prompt design and may vary slightly

---

## 🎬 Demo

(Add your video link here)

---

## 📂 Project Structure

```id="proj01"
.
├── main.py
├── requirements.txt
└── README.md
```

---

## 🔁 Reproducibility

* Fixed temperature (0.2)
* Same input → similar structured output
* Minor variation possible due to LLM behavior

---

## 🚀 Future Improvements

* Web UI (React / Streamlit)
* Multi-file repository analysis
* AST-based validation
* Cloud model integration

---

## 🤝 Contribution

Open for improvements and extensions.

---
