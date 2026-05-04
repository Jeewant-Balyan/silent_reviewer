# 🚀 Silent Reviewer

### Multi-Agent AI Code Reviewer (Local + Parallel Inference)

---

## 🧠 What is this?

Silent Reviewer is an AI-powered code review system that simulates **multiple specialized reviewers working in parallel**.

Instead of relying on a single prompt, it splits the review into focused agents:

* Bugs
* Security
* Performance
* Code quality

These agents run **concurrently**, and their outputs are combined into a final structured review with a score and verdict.

---

## ❗ Problem It Solves

Traditional code review:

* slow
* inconsistent
* depends on reviewer expertise

Single-LLM solutions:

* mix everything in one prompt
* lose specialization
* harder to control output quality

---

## ✅ Solution Approach

We treat code review like a **distributed system of experts**.

Each agent:

* has a narrow responsibility
* uses a strict prompt format (JSON)
* produces structured, reliable output

A final synthesis agent:

* merges all findings
* assigns score + grade
* highlights top priority issue

---

## ⚙️ Key Features

* 🐛 **Bug Detection Agent** — logic errors, edge cases
* 🔒 **Security Scanner** — vulnerabilities, unsafe usage
* ⚡ **Performance Analyzer** — inefficiencies, bottlenecks
* ✨ **Style Reviewer** — best practices, maintainability
* 🧠 **Synthesis Agent** — final verdict + grading
* ⚡ **Parallel Execution** — ~4x faster than sequential
* 🌐 **GitHub Code Fetching** — analyze remote files

---

## 🏗️ System Architecture

```
        Input Code / GitHub URL
                   │
        ┌──────────┼──────────┐
        │          │          │
   Bug Agent   Security   Performance
        │          │          │
        └──────┬───┴───┬──────┘
               │       │
           Style Agent │
               │       │
               └──► Synthesis Agent
                        │
                Final Report (JSON)
```

---

## 🤖 Model Declaration (Required)

* Model: `gemma3:1b`
* Runtime: Ollama (local inference)
* Endpoint: `http://localhost:11434/api/generate`
* Temperature: 0.2
* Max tokens: 800

### Why this model?

* Lightweight → fast execution
* Runs locally → zero API cost
* Good enough for structured reasoning tasks
* Enables parallel inference without API limits

---

## 🚀 Setup & Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Ollama

```bash
ollama serve
```

### 3. Pull model

```bash
ollama pull gemma3:1b
```

### 4. Run project

```bash
python main.py
```

---

## 💡 Example Usage

* Input: Code snippet OR GitHub file URL
* Output:

  * categorized issues
  * severity levels
  * confidence score
  * final grade (A–F)

---

## 📊 Performance & Metrics

| Metric             | Value       |
| ------------------ | ----------- |
| Sequential runtime | ~80 seconds |
| Parallel runtime   | ~20 seconds |
| Speed improvement  | ~4x         |
| Cost               | $0 (local)  |
| Confidence scoring | Yes         |

---

## ⚠️ Known Limitations

* Small model → may miss deep/complex bugs
* No AST/static analysis
* Single-file focused
* Depends on prompt engineering quality

👉 These trade-offs were intentionally made for speed and cost efficiency.

---

## 🎬 Demo

(Add your demo video link here)

---

## 📂 Project Structure

```
.
├── main.py                # Core pipeline
├── agents/                # (future modularization)
├── utils/                 # helpers
└── README.md
```

---

## 🔬 Design Decisions

### Why Multi-Agent?

* Reduces prompt overload
* Improves specialization
* Easier debugging of outputs

### Why Parallel Execution?

* LLM calls are independent
* Reduces total latency dramatically

### Why Local Inference?

* No API cost
* Full control
* Offline capability

---

## 🚀 Future Improvements

* 🌐 Web UI (React / Streamlit)
* 📁 Multi-file repository analysis
* 🧠 AST-based static analysis
* ☁️ Cloud LLM fallback (OpenAI/Groq)
* 📊 Visual dashboard for results

---

## 🤝 Contribution

Open for improvements, extensions, and integrations.

---
