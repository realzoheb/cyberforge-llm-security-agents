"""
CyberForge LLM Security Agents - Interactive Web GUI Dashboard.
Runs a local Web Application on http://localhost:5000 with a modern glassmorphic interface.
"""

import http.server
import socketserver
import json
import urllib.parse
import sys
import os
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent))

from scenarios import registry
from agents.security_agents import create_security_analyst, create_detection_engineer, create_purple_team_agent
from core.llm_provider import get_llm_provider
from core.agent import BaseAgent
from config import Config

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CyberForge LLM Security Agents Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root {
            --bg-primary: #0a0e17;
            --bg-card: rgba(22, 31, 48, 0.7);
            --border-card: rgba(255, 255, 255, 0.08);
            --accent-cyan: #00f2fe;
            --accent-blue: #4facfe;
            --accent-purple: #7f00ff;
            --accent-green: #00e676;
            --accent-orange: #ff9100;
            --text-primary: #f0f4f8;
            --text-muted: #94a3b8;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-primary);
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(0, 242, 254, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(127, 0, 255, 0.08) 0%, transparent 40%);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        header {
            background: rgba(10, 14, 23, 0.85);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-card);
            padding: 18px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 800;
            font-size: 1.4rem;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .badge {
            background: rgba(0, 242, 254, 0.12);
            border: 1px solid rgba(0, 242, 254, 0.3);
            color: var(--accent-cyan);
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }

        .container {
            max-width: 1300px;
            margin: 30px auto;
            padding: 0 20px;
            width: 100%;
            flex: 1;
            display: grid;
            grid-template-columns: 320px 1fr;
            gap: 25px;
        }

        .sidebar {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .card {
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-card);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        .card-title {
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--text-primary);
        }

        .nav-btn {
            width: 100%;
            padding: 14px 16px;
            border-radius: 10px;
            border: 1px solid transparent;
            background: rgba(255, 255, 255, 0.03);
            color: var(--text-muted);
            font-weight: 600;
            font-size: 0.9rem;
            text-align: left;
            cursor: pointer;
            transition: all 0.25s ease;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .nav-btn:hover, .nav-btn.active {
            background: linear-gradient(135deg, rgba(0, 242, 254, 0.15), rgba(79, 172, 254, 0.15));
            border-color: rgba(0, 242, 254, 0.4);
            color: var(--text-primary);
            transform: translateX(4px);
        }

        .main-content {
            display: flex;
            flex-direction: column;
            gap: 25px;
        }

        .tab-panel {
            display: none;
        }

        .tab-panel.active {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .scenario-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }

        .scenario-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-card);
            border-radius: 12px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.3s ease;
        }

        .scenario-card:hover {
            border-color: var(--accent-cyan);
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0, 242, 254, 0.15);
        }

        .scenario-name {
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--accent-cyan);
            margin-bottom: 8px;
        }

        .scenario-desc {
            font-size: 0.85rem;
            color: var(--text-muted);
            line-height: 1.5;
            margin-bottom: 20px;
        }

        .btn {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            color: #000;
            font-weight: 700;
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.25s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .btn:hover {
            opacity: 0.9;
            transform: scale(1.02);
            box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4);
        }

        .output-area {
            background: #06090e;
            border: 1px solid var(--border-card);
            border-radius: 12px;
            padding: 24px;
            min-height: 250px;
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            line-height: 1.6;
            color: #e2e8f0;
            overflow-y: auto;
            max-height: 500px;
        }

        .output-area h1, .output-area h2, .output-area h3 {
            color: var(--accent-cyan);
            margin-top: 16px;
            margin-bottom: 8px;
        }

        .output-area code {
            font-family: 'Fira Code', monospace;
            background: rgba(255, 255, 255, 0.08);
            padding: 2px 6px;
            border-radius: 4px;
            color: var(--accent-green);
        }

        .output-area pre {
            background: #0d1117;
            padding: 16px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            overflow-x: auto;
            margin: 12px 0;
        }

        .output-area pre code {
            background: transparent;
            padding: 0;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 16px;
        }

        label {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
        }

        select, input, textarea {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-card);
            border-radius: 8px;
            padding: 12px;
            color: var(--text-primary);
            font-family: inherit;
            font-size: 0.9rem;
            outline: none;
            transition: border-color 0.2s ease;
        }

        select:focus, input:focus, textarea:focus {
            border-color: var(--accent-cyan);
        }

        .spinner {
            display: none;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: #000;
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>

<header>
    <div class="logo">
        🛡️ CyberForge LLM Agents
    </div>
    <div style="display: flex; gap: 15px; align-items: center;">
        <span class="badge">Localhost Web Dashboard</span>
        <span style="font-size: 0.85rem; color: var(--text-muted);">Port: 5000</span>
    </div>
</header>

<div class="container">
    <div class="sidebar">
        <div class="card">
            <div class="card-title">🎮 Navigation</div>
            <button class="nav-btn active" onclick="switchTab('scenarios')">
                🚀 Scenario Runner <span>→</span>
            </button>
            <button class="nav-btn" onclick="switchTab('sandbox')">
                🧪 Custom Agent Sandbox <span>→</span>
            </button>
            <button class="nav-btn" onclick="switchTab('config')">
                ⚙️ Provider & API Config <span>→</span>
            </button>
        </div>

        <div class="card">
            <div class="card-title">📊 System Status</div>
            <div style="font-size: 0.85rem; color: var(--text-muted); display: flex; flex-direction: column; gap: 10px;">
                <div>HTTP Server: <strong style="color: var(--accent-green)">Active (8080)</strong></div>
                <div>FTP Server: <strong style="color: var(--accent-orange)">Standby (2121)</strong></div>
                <div>Default LLM: <strong style="color: var(--accent-cyan)" id="currentProviderDisplay">...</strong></div>
            </div>
        </div>
    </div>

    <div class="main-content">
        <!-- TAB 1: SCENARIO RUNNER -->
        <div id="tab-scenarios" class="tab-panel active">
            <div class="card">
                <div class="card-title">🚀 Registered Security Scenarios</div>
                <div class="scenario-grid" id="scenarioGrid">
                    <!-- Populated dynamically -->
                </div>
            </div>

            <div class="card">
                <div class="card-title">📋 Execution Output & Terminal Stream</div>
                <div class="output-area" id="scenarioOutput">
                    <em>Click "Run Scenario" above to execute multi-agent workflows on localhost...</em>
                </div>
            </div>
        </div>

        <!-- TAB 2: CUSTOM AGENT SANDBOX -->
        <div id="tab-sandbox" class="tab-panel">
            <div class="card">
                <div class="card-title">🧪 Custom Security Agent Execution</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div class="form-group">
                        <label>Select Agent Persona</label>
                        <select id="agentSelect">
                            <option value="analyst">Analyst-Alpha (SOC Security Analyst)</option>
                            <option value="engineer">Sentinel-Beta (Detection Engineer)</option>
                            <option value="purple">Aegis-Gamma (Purple Team Specialist)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Select LLM Provider</label>
                        <select id="providerSelect">
                            <option value="nvidia">NVIDIA NIM API</option>
                            <option value="opencode">OpenCode / OpenRouter API</option>
                            <option value="google">Google Gemini API</option>
                            <option value="openai">OpenAI API</option>
                            <option value="ollama">Ollama (Local Model)</option>
                        </select>
                    </div>
                </div>

                <div class="form-group">
                    <label>Task Prompt / Security Event Log</label>
                    <textarea id="taskPrompt" rows="5" placeholder="Enter log data, incident notes, or detection rule requirements..."></textarea>
                </div>

                <button class="btn" onclick="runCustomTask()">
                    <span class="spinner" id="sandboxSpinner"></span>
                    <span>Execute Agent Task</span>
                </button>
            </div>

            <div class="card">
                <div class="card-title">📄 Agent Result</div>
                <div class="output-area" id="sandboxOutput">
                    <em>Agent response will be rendered here in markdown format...</em>
                </div>
            </div>
        </div>

        <!-- TAB 3: PROVIDER & API CONFIG -->
        <div id="tab-config" class="tab-panel">
            <div class="card">
                <div class="card-title">⚙️ LLM Provider & API Key Settings</div>
                <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 20px;">
                    Configure API keys dynamically for localhost scenario execution.
                </p>

                <div class="form-group">
                    <label>Active Default Provider</label>
                    <select id="cfgDefaultProvider">
                        <option value="google">Google Gemini</option>
                        <option value="nvidia">NVIDIA NIM</option>
                        <option value="opencode">OpenCode / OpenRouter</option>
                        <option value="openai">OpenAI</option>
                        <option value="ollama">Ollama (Local)</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>NVIDIA NIM API Key</label>
                    <input type="password" id="cfgNvidiaKey" placeholder="nvapi-...">
                </div>

                <div class="form-group">
                    <label>OpenCode / OpenRouter API Key</label>
                    <input type="password" id="cfgOpencodeKey" placeholder="sk-or-v1-...">
                </div>

                <div class="form-group">
                    <label>Google Gemini API Key</label>
                    <input type="password" id="cfgGeminiKey" placeholder="AIzaSy...">
                </div>

                <button class="btn" onclick="saveConfig()">Save Configuration</button>
            </div>
        </div>
    </div>
</div>

<script>
    function switchTab(tabName) {
        document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));

        document.getElementById(`tab-${tabName}`).classList.add('active');
        event.currentTarget.classList.add('active');
    }

    async function loadScenarios() {
        const resp = await fetch('/api/scenarios');
        const data = await resp.json();
        const grid = document.getElementById('scenarioGrid');
        grid.innerHTML = '';

        for (const [key, details] of Object.entries(data)) {
            const card = document.createElement('div');
            card.className = 'scenario-card';
            card.innerHTML = `
                <div>
                    <div class="scenario-name">🚀 ${details.name}</div>
                    <div class="scenario-desc">${details.description}</div>
                </div>
                <button class="btn" onclick="runScenario('${key}')">Run Scenario</button>
            `;
            grid.appendChild(card);
        }
    }

    async function runScenario(scenarioKey) {
        const out = document.getElementById('scenarioOutput');
        out.innerHTML = `<em>Running scenario '${scenarioKey}'... Please wait.</em>`;

        const resp = await fetch('/api/run_scenario', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({scenario: scenarioKey})
        });
        const result = await resp.json();

        let mdContent = `# Scenario Execution Output: ${scenarioKey}\n\n`;
        for (const [taskName, outputText] of Object.entries(result.results || {})) {
            mdContent += `### ✓ Task Output: ${taskName}\n\n${outputText}\n\n---\n\n`;
        }
        out.innerHTML = marked.parse(mdContent);
    }

    async function runCustomTask() {
        const agent = document.getElementById('agentSelect').value;
        const provider = document.getElementById('providerSelect').value;
        const prompt = document.getElementById('taskPrompt').value;
        const out = document.getElementById('sandboxOutput');
        const spinner = document.getElementById('sandboxSpinner');

        if (!prompt.trim()) {
            alert('Please enter a task prompt or log data.');
            return;
        }

        spinner.style.display = 'inline-block';
        out.innerHTML = '<em>Agent is generating security analysis...</em>';

        const resp = await fetch('/api/run_custom', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({agent, provider, prompt})
        });
        const result = await resp.json();
        spinner.style.display = 'none';

        out.innerHTML = marked.parse(result.output || 'No output generated.');
    }

    async function loadConfig() {
        const resp = await fetch('/api/config');
        const cfg = await resp.json();
        document.getElementById('currentProviderDisplay').innerText = cfg.default_provider.toUpperCase();
        document.getElementById('cfgDefaultProvider').value = cfg.default_provider;
    }

    async function saveConfig() {
        const default_provider = document.getElementById('cfgDefaultProvider').value;
        const nvidia_key = document.getElementById('cfgNvidiaKey').value;
        const opencode_key = document.getElementById('cfgOpencodeKey').value;
        const gemini_key = document.getElementById('cfgGeminiKey').value;

        await fetch('/api/config', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({default_provider, nvidia_key, opencode_key, gemini_key})
        });
        alert('Configuration updated successfully!');
        loadConfig();
    }

    loadScenarios();
    loadConfig();
</script>
</body>
</html>
"""

class CyberForgeWebHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
        elif parsed.path == "/api/scenarios":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            data = registry.get_all()
            serializable = {k: {"name": v["name"], "description": v["description"]} for k, v in data.items()}
            self.wfile.write(json.dumps(serializable).encode("utf-8"))
        elif parsed.path == "/api/config":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            cfg_data = {
                "default_provider": Config.DEFAULT_PROVIDER,
                "has_gemini": bool(Config.GEMINI_API_KEY),
                "has_nvidia": bool(Config.NVIDIA_API_KEY),
                "has_opencode": bool(Config.OPENCODE_API_KEY)
            }
            self.wfile.write(json.dumps(cfg_data).encode("utf-8"))
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len).decode('utf-8')
        data = json.loads(body) if body else {}

        if self.path == "/api/run_scenario":
            scenario_key = data.get("scenario", "")
            if scenario_key in registry.get_all():
                workflow = registry.get_all()[scenario_key]["builder"]()
                results = workflow.run()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "results": results}).encode("utf-8"))
            else:
                self.send_error(404, "Scenario not found")

        elif self.path == "/api/run_custom":
            agent_type = data.get("agent", "analyst")
            provider_type = data.get("provider", "google")
            prompt = data.get("prompt", "")

            llm = get_llm_provider(provider_type)
            if agent_type == "engineer":
                agent = create_detection_engineer(provider=llm)
            elif agent_type == "purple":
                agent = create_purple_team_agent(provider=llm)
            else:
                agent = create_security_analyst(provider=llm)

            output = agent.execute_task(prompt)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "output": output}).encode("utf-8"))

        elif self.path == "/api/config":
            if data.get("default_provider"):
                Config.DEFAULT_PROVIDER = data["default_provider"]
            if data.get("gemini_key"):
                Config.GEMINI_API_KEY = data["gemini_key"]
            if data.get("nvidia_key"):
                Config.NVIDIA_API_KEY = data["nvidia_key"]
            if data.get("opencode_key"):
                Config.OPENCODE_API_KEY = data["opencode_key"]

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "updated"}).encode("utf-8"))

def run_web_gui(host: str = "127.0.0.1", port: int = 5000):
    with socketserver.TCPServer((host, port), CyberForgeWebHandler) as httpd:
        print("==================================================")
        print(f"🌐 CYBERFORGE WEB DASHBOARD RUNNING")
        print(f"Localhost URL: http://{host}:{port}")
        print(f"Press CTRL+C to stop the Web Dashboard.")
        print("==================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down Web Dashboard...")
            httpd.server_close()

if __name__ == "__main__":
    run_web_gui()
