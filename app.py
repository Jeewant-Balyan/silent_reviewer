"""
Silent Reviewer — Flask Web App
Run: python app.py
UPDATED: GitHub URL support + parallel agents
"""

import os
from flask import Flask, request, jsonify, render_template_string
from reviewer import review_code, fetch_github_code

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1MB max

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Silent Reviewer — AI Code Review</title>
<style>
  :root {
    --bg: #0f1117; --surface: #1a1d26; --surface2: #22263a;
    --border: #2d3148; --text: #e2e8f0; --muted: #8892a4;
    --green: #22c55e; --red: #ef4444; --yellow: #f59e0b;
    --blue: #3b82f6; --purple: #a855f7;
    --radius: 10px; --mono: 'Fira Code', 'Courier New', monospace;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg); color: var(--text); font-family: system-ui, sans-serif;
         min-height: 100vh; padding: 24px 16px; }
  .wrap { max-width: 960px; margin: 0 auto; }

  /* Header */
  .header { text-align: center; margin-bottom: 32px; }
  .header h1 { font-size: 28px; font-weight: 700; letter-spacing: -0.5px; }
  .header h1 span { color: var(--purple); }
  .header p { color: var(--muted); margin-top: 6px; font-size: 14px; }
  .badges-row { display: flex; gap: 8px; justify-content: center; margin-top: 10px; flex-wrap: wrap; }
  .model-badge { display: inline-block; background: var(--surface2); border: 1px solid var(--border);
    padding: 4px 12px; border-radius: 20px; font-size: 12px; color: var(--muted); }
  .model-badge b { color: var(--purple); }
  .speed-badge { display: inline-block; background: rgba(34,197,94,.1); border: 1px solid rgba(34,197,94,.3);
    padding: 4px 12px; border-radius: 20px; font-size: 12px; color: var(--green); }

  /* Tab switcher */
  .tabs { display: flex; gap: 0; margin-bottom: 0; border-radius: var(--radius) var(--radius) 0 0;
          overflow: hidden; border: 1px solid var(--border); border-bottom: none; }
  .tab { flex: 1; padding: 12px 16px; background: var(--surface2); color: var(--muted);
    font-size: 13px; font-weight: 600; cursor: pointer; border: none; transition: all .15s;
    display: flex; align-items: center; justify-content: center; gap: 8px; }
  .tab:hover { background: var(--surface); color: var(--text); }
  .tab.active { background: var(--surface); color: var(--purple); border-bottom: 2px solid var(--purple); }

  /* Input area */
  .input-card { background: var(--surface); border: 1px solid var(--border);
    border-radius: 0 0 var(--radius) var(--radius); padding: 20px; margin-bottom: 16px; }

  /* GitHub URL input */
  .github-panel { display: none; }
  .github-panel.active { display: block; }
  .paste-panel { display: none; }
  .paste-panel.active { display: block; }

  .url-input-wrap { position: relative; margin-bottom: 12px; }
  .url-input-wrap .gh-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%);
    font-size: 16px; pointer-events: none; }
  .gh-url-input { width: 100%; background: var(--surface2); border: 1px solid var(--border);
    color: var(--text); padding: 12px 12px 12px 38px; border-radius: 8px;
    font-size: 13px; outline: none; font-family: var(--mono); }
  .gh-url-input:focus { border-color: var(--purple); }
  .gh-url-input::placeholder { color: var(--muted); font-family: system-ui, sans-serif; }

  .url-examples { font-size: 11px; color: var(--muted); margin-bottom: 14px; line-height: 1.8; }
  .url-examples code { background: var(--surface2); padding: 2px 6px; border-radius: 4px;
    color: var(--text); font-family: var(--mono); font-size: 11px; }
  .url-status { font-size: 12px; padding: 8px 12px; border-radius: 6px; margin-bottom: 12px;
    display: none; }
  .url-status.fetching { display: block; background: rgba(168,85,247,.1);
    border: 1px solid rgba(168,85,247,.3); color: var(--purple); }
  .url-status.ok { display: block; background: rgba(34,197,94,.1);
    border: 1px solid rgba(34,197,94,.3); color: var(--green); }
  .url-status.err { display: block; background: rgba(239,68,68,.1);
    border: 1px solid rgba(239,68,68,.3); color: var(--red); }

  /* Paste panel */
  .input-row { display: flex; gap: 10px; margin-bottom: 12px; align-items: center; }
  .input-row label { font-size: 13px; color: var(--muted); white-space: nowrap; }
  input[type=text] { background: var(--surface2); border: 1px solid var(--border); color: var(--text);
    padding: 8px 12px; border-radius: 6px; font-size: 13px; flex: 1; outline: none; }
  input[type=text]:focus { border-color: var(--purple); }
  textarea { width: 100%; background: var(--surface2); border: 1px solid var(--border);
    color: var(--text); padding: 14px; border-radius: var(--radius); font-family: var(--mono);
    font-size: 13px; line-height: 1.6; resize: vertical; outline: none; min-height: 260px; }
  textarea:focus { border-color: var(--purple); }

  .btn { background: var(--purple); color: white; border: none; padding: 12px 28px;
    border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer;
    transition: opacity .15s; width: 100%; margin-top: 12px; }
  .btn:hover { opacity: .85; }
  .btn:disabled { opacity: .4; cursor: not-allowed; }

  /* Loading */
  #loading { display: none; text-align: center; padding: 40px; }
  .spinner { display: inline-block; width: 36px; height: 36px; border: 3px solid var(--border);
    border-top-color: var(--purple); border-radius: 50%; animation: spin 1s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }
  .loading-steps { margin-top: 16px; font-size: 13px; color: var(--muted); }
  .loading-parallel-note { font-size: 11px; color: var(--green); margin-bottom: 12px; }
  .steps-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; max-width: 380px;
    margin: 0 auto; text-align: left; }
  .step { padding: 6px 10px; border-radius: 6px; transition: all .3s;
    background: var(--surface2); }
  .step.active { background: rgba(168,85,247,.15); color: var(--purple); }
  .step.done { background: rgba(34,197,94,.1); color: var(--green); }
  .step-synth { grid-column: 1 / -1; text-align: center; margin-top: 4px; }

  /* Score card */
  .score-card { background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 24px; margin-bottom: 16px;
    display: flex; gap: 24px; align-items: center; }
  .score-circle { width: 80px; height: 80px; border-radius: 50%; display: flex;
    flex-direction: column; align-items: center; justify-content: center;
    border: 3px solid var(--border); flex-shrink: 0; }
  .score-num { font-size: 24px; font-weight: 700; }
  .score-lbl { font-size: 11px; color: var(--muted); }
  .score-info h2 { font-size: 18px; font-weight: 600; margin-bottom: 6px; }
  .score-info p { font-size: 13px; color: var(--muted); line-height: 1.6; }
  .priority { background: var(--surface2); border-left: 3px solid var(--yellow);
    padding: 10px 14px; border-radius: 0 6px 6px 0; margin-top: 10px;
    font-size: 13px; color: var(--text); }
  .priority span { color: var(--yellow); font-weight: 600; }
  .source-info { background: var(--surface2); border: 1px solid var(--border);
    border-radius: 6px; padding: 8px 12px; font-size: 11px; color: var(--muted);
    margin-top: 8px; font-family: var(--mono); word-break: break-all; }
  .source-info a { color: var(--blue); text-decoration: none; }
  .source-info a:hover { text-decoration: underline; }

  /* Agent sections */
  .agents { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px; }
  @media(max-width:640px){ .agents { grid-template-columns: 1fr; } }
  .agent-card { background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 16px; }
  .agent-header { display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 12px; }
  .agent-name { font-size: 13px; font-weight: 600; }
  .agent-count { font-size: 12px; color: var(--muted); }

  /* Issues */
  .issue { background: var(--surface2); border-radius: 8px; padding: 12px;
    margin-bottom: 8px; border-left: 3px solid var(--border); }
  .issue.critical { border-left-color: var(--red); }
  .issue.warning  { border-left-color: var(--yellow); }
  .issue.suggestion { border-left-color: var(--blue); }
  .issue-top { display: flex; justify-content: space-between; align-items: flex-start;
    margin-bottom: 6px; gap: 8px; }
  .issue-msg { font-size: 13px; color: var(--text); line-height: 1.5; flex: 1; }
  .badges { display: flex; gap: 5px; flex-shrink: 0; flex-wrap: wrap; }
  .badge { font-size: 10px; font-weight: 600; padding: 2px 7px; border-radius: 20px; }
  .badge-critical  { background: rgba(239,68,68,.2);  color: var(--red); }
  .badge-warning   { background: rgba(245,158,11,.2); color: var(--yellow); }
  .badge-suggestion{ background: rgba(59,130,246,.2); color: var(--blue); }
  .badge-conf      { background: var(--surface); color: var(--muted); border: 1px solid var(--border); }
  .issue-fix { font-size: 12px; color: var(--green); margin-top: 6px; line-height: 1.5; }
  .issue-fix::before { content: "✓ "; }
  .issue-line { font-size: 11px; color: var(--muted); margin-top: 4px; font-family: var(--mono); }
  .no-issues { font-size: 13px; color: var(--green); text-align: center; padding: 16px 0; }

  /* Disclaimer */
  .disclaimer { background: var(--surface2); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 14px 16px; font-size: 12px;
    color: var(--muted); line-height: 1.6; margin-bottom: 16px; }
  .disclaimer b { color: var(--text); }

  #results { display: none; }
  .error-msg { background: rgba(239,68,68,.1); border: 1px solid rgba(239,68,68,.3);
    border-radius: var(--radius); padding: 16px; color: var(--red); font-size: 14px;
    margin-bottom: 16px; }
</style>
</head>
<body>
<div class="wrap">

  <div class="header">
    <h1>🔍 <span>Silent</span> Reviewer</h1>
    <p>Multi-agent AI code review • Runs 100% locally • No internet required</p>
    <div class="badges-row">
      <div class="model-badge">Powered by <b>Gemma3 1B</b> via Ollama</div>
      <div class="speed-badge">⚡ Parallel agents — ~20s reviews</div>
    </div>
  </div>

  <!-- Tab switcher -->
  <div class="tabs">
    <button class="tab active" id="tabGithub" onclick="switchTab('github')">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
      GitHub URL
    </button>
    <button class="tab" id="tabPaste" onclick="switchTab('paste')">
      📋 Paste Code
    </button>
  </div>

  <div class="input-card">

    <!-- GitHub URL panel -->
    <div class="github-panel active" id="panelGithub">
      <div class="url-input-wrap">
        <span class="gh-icon">🔗</span>
        <input class="gh-url-input" type="text" id="githubUrl"
          placeholder="https://github.com/user/repo/blob/main/path/to/file.py">
      </div>
      <div class="url-examples">
        Supported formats:<br>
        <code>github.com/user/repo/blob/main/file.py</code> — file blob URL<br>
        <code>raw.githubusercontent.com/user/repo/main/file.py</code> — raw URL<br>
        <code>gist.github.com/user/gistid</code> — GitHub Gist
      </div>
      <div class="url-status" id="urlStatus"></div>
    </div>

    <!-- Paste panel -->
    <div class="paste-panel" id="panelPaste">
      <div class="input-row">
        <label>Filename:</label>
        <input type="text" id="filename" value="main.py" placeholder="e.g. app.py, index.js">
      </div>
      <textarea id="code" placeholder="Paste your code here...&#10;&#10;The reviewer will check for bugs, security issues, performance problems, and bad practices."></textarea>
    </div>

    <button class="btn" id="reviewBtn" onclick="startReview()">
      🚀 Run Silent Review
    </button>
  </div>

  <!-- Loading -->
  <div id="loading">
    <div class="spinner"></div>
    <div class="loading-steps">
      <div class="loading-parallel-note">⚡ All 4 agents running in parallel</div>
      <div class="steps-grid">
        <div class="step" id="s1">🐛 Bug Hunter</div>
        <div class="step" id="s2">🔒 Security Scanner</div>
        <div class="step" id="s3">⚡ Performance</div>
        <div class="step" id="s4">✨ Style & Practices</div>
        <div class="step step-synth" id="s5">🧠 Synthesis Agent</div>
      </div>
    </div>
  </div>

  <!-- Results -->
  <div id="results">
    <div id="error-area"></div>

    <!-- Score -->
    <div class="score-card" id="scoreCard">
      <div class="score-circle" id="scoreCircle">
        <span class="score-num" id="scoreNum">-</span>
        <span class="score-lbl">/ 100</span>
      </div>
      <div class="score-info" style="flex:1">
        <h2 id="verdict"></h2>
        <p id="verdictText"></p>
        <div class="priority"><span>⚡ Top priority:</span> <span id="topPriority"></span></div>
        <div class="source-info" id="sourceInfo" style="display:none"></div>
      </div>
    </div>

    <!-- Agent cards -->
    <div class="agents">
      <div class="agent-card">
        <div class="agent-header"><span class="agent-name">🐛 Bug Hunter</span><span class="agent-count" id="cntBugs"></span></div>
        <div id="issuesBugs"></div>
      </div>
      <div class="agent-card">
        <div class="agent-header"><span class="agent-name">🔒 Security Scanner</span><span class="agent-count" id="cntSec"></span></div>
        <div id="issuesSec"></div>
      </div>
      <div class="agent-card">
        <div class="agent-header"><span class="agent-name">⚡ Performance</span><span class="agent-count" id="cntPerf"></span></div>
        <div id="issuesPerf"></div>
      </div>
      <div class="agent-card">
        <div class="agent-header"><span class="agent-name">✨ Style & Practices</span><span class="agent-count" id="cntStyle"></span></div>
        <div id="issuesStyle"></div>
      </div>
    </div>

    <!-- Disclaimer -->
    <div class="disclaimer" id="disclaimerBox"></div>
  </div>

</div>

<script>
let currentTab = 'github';
let stepTimer = null;

function switchTab(tab) {
  currentTab = tab;
  document.getElementById('tabGithub').className = 'tab' + (tab === 'github' ? ' active' : '');
  document.getElementById('tabPaste').className  = 'tab' + (tab === 'paste'  ? ' active' : '');
  document.getElementById('panelGithub').className = 'github-panel' + (tab === 'github' ? ' active' : '');
  document.getElementById('panelPaste').className  = 'paste-panel'  + (tab === 'paste'  ? ' active' : '');
}

function setUrlStatus(type, msg) {
  const el = document.getElementById('urlStatus');
  el.className = 'url-status ' + type;
  el.textContent = msg;
}

function animateSteps() {
  // All 4 agents start at once (parallel), synth starts after
  ['s1','s2','s3','s4'].forEach(s => {
    document.getElementById(s).className = 'step active';
  });
  document.getElementById('s5').className = 'step';

  // After estimated agent time, show synth starting
  stepTimer = setTimeout(() => {
    ['s1','s2','s3','s4'].forEach(s => {
      document.getElementById(s).className = 'step done';
    });
    document.getElementById('s5').className = 'step active';
  }, 18000); // ~18s estimate for agents
}

function renderIssues(issues, containerId, countId) {
  const el = document.getElementById(containerId);
  const cnt = document.getElementById(countId);
  cnt.textContent = issues.length + ' issue' + (issues.length !== 1 ? 's' : '');
  if (!issues.length) {
    el.innerHTML = '<div class="no-issues">✓ No issues found</div>';
    return;
  }
  el.innerHTML = issues.map(i => `
    <div class="issue ${i.severity}">
      <div class="issue-top">
        <div class="issue-msg">${i.message}</div>
        <div class="badges">
          <span class="badge badge-${i.severity}">${i.severity}</span>
          <span class="badge badge-conf">${i.confidence}%</span>
        </div>
      </div>
      ${i.fix ? `<div class="issue-fix">${i.fix}</div>` : ''}
      ${i.line ? `<div class="issue-line">Line ${i.line}</div>` : ''}
    </div>
  `).join('');
}

async function startReview() {
  let code = '', filename = 'code.py', githubUrl = '';

  if (currentTab === 'github') {
    githubUrl = document.getElementById('githubUrl').value.trim();
    if (!githubUrl) { alert('Please enter a GitHub URL.'); return; }
  } else {
    code = document.getElementById('code').value.trim();
    filename = document.getElementById('filename').value.trim() || 'code.py';
    if (!code) { alert('Please paste some code first!'); return; }
  }

  document.getElementById('reviewBtn').disabled = true;
  document.getElementById('loading').style.display = 'block';
  document.getElementById('results').style.display = 'none';
  document.getElementById('error-area').innerHTML = '';
  setUrlStatus('', '');
  animateSteps();

  try {
    const payload = currentTab === 'github'
      ? { github_url: githubUrl }
      : { code, filename };

    const resp = await fetch('/review', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await resp.json();

    clearTimeout(stepTimer);
    document.getElementById('loading').style.display = 'none';
    document.getElementById('results').style.display = 'block';

    if (data.error) {
      document.getElementById('error-area').innerHTML =
        `<div class="error-msg">❌ ${data.error}</div>`;
      return;
    }

    // Score
    const score = data.summary.overall_score || 0;
    const grade = data.summary.grade || '?';
    const scoreEl = document.getElementById('scoreCircle');
    const color = score >= 80 ? '#22c55e' : score >= 60 ? '#f59e0b' : '#ef4444';
    scoreEl.style.borderColor = color;
    document.getElementById('scoreNum').style.color = color;
    document.getElementById('scoreNum').textContent = score;
    document.getElementById('verdict').textContent = `Grade ${grade} — ${data.filename}`;
    document.getElementById('verdictText').textContent = data.summary.verdict || '';
    document.getElementById('topPriority').textContent = data.summary.top_priority || 'None';

    // Show source URL if from GitHub
    const srcEl = document.getElementById('sourceInfo');
    if (data.github_url) {
      srcEl.style.display = 'block';
      srcEl.innerHTML = `📎 Source: <a href="${data.github_url}" target="_blank">${data.github_url}</a>`;
    } else {
      srcEl.style.display = 'none';
    }

    // Issues per agent
    const agentMap = {
      bugs: ['issuesBugs', 'cntBugs'],
      security: ['issuesSec', 'cntSec'],
      performance: ['issuesPerf', 'cntPerf'],
      style: ['issuesStyle', 'cntStyle']
    };
    for (const [key, [cid, cnt]] of Object.entries(agentMap)) {
      renderIssues(data.agents[key]?.issues || [], cid, cnt);
    }

    document.getElementById('disclaimerBox').innerHTML =
      `<b>⚠️ Model disclaimer:</b> ${data.summary.model_disclaimer || ''}
       &nbsp;|&nbsp; ${data.line_count} lines reviewed &nbsp;|&nbsp; Model: ${data.model}
       &nbsp;|&nbsp; <b style="color:var(--green)">⚡ Parallel agents</b>`;

  } catch(e) {
    clearTimeout(stepTimer);
    document.getElementById('loading').style.display = 'none';
    document.getElementById('results').style.display = 'block';
    document.getElementById('error-area').innerHTML =
      `<div class="error-msg">❌ Connection error. Is Ollama running? Run: <code>ollama serve</code></div>`;
  } finally {
    document.getElementById('reviewBtn').disabled = false;
  }
}
</script>
</body>
</html>"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/review", methods=["POST"])
def review():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        github_url = data.get("github_url", "").strip()
        code = data.get("code", "").strip()
        filename = data.get("filename", "code.py").strip()

        # Fetch from GitHub if URL provided
        if github_url:
            try:
                code, filename = fetch_github_code(github_url)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

        if not code:
            return jsonify({"error": "No code provided"}), 400

        if len(code) > 8000:
            code = code[:8000]  # Trim for tiny model context

        result = review_code(code, filename)

        # Serialize issues to dicts
        for key in result["agents"]:
            agent = result["agents"][key]
            result["agents"][key] = {
                "agent": agent.agent,
                "issues": [vars(i) for i in agent.issues],
                "error": agent.error
            }
        result["all_issues"] = [vars(i) for i in result["all_issues"]]

        # Pass back the GitHub URL so UI can show it
        if github_url:
            result["github_url"] = github_url

        return jsonify(result)

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500


if __name__ == "__main__":
    print("\n🔍 Silent Reviewer")
    print("=" * 40)
    print("Make sure Ollama is running: ollama serve")
    print("Make sure model is pulled:   ollama pull gemma3:1b")
    print("=" * 40)
    print("Open: http://localhost:5000\n")
    app.run(debug=False, port=5000)