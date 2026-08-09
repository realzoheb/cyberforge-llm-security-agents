# 🛡️ CyberForge LLM Security Agents

A Python-based Cybersecurity LLM Agent Framework designed specifically for lab environments, virtual machine research, adversary emulation experiments, detection engineering, and purple team automation.

---

> [!CAUTION]
> **SAFETY WARNING & LAB DISCLAIMER**  
> This toolkit is designed **strictly for authorized testing, research, adversary emulation demos, and education in isolated virtual/lab environments**. Do not execute unauthorized actions or run against production systems.

---

## 🚀 Features

- **Centralized Scenario CLI**: Easily list and execute named security scenarios (`hello_agents`, `log_analysis`, `purple_team`).
- **Multi-Provider Support**: Pluggable provider architecture supporting **Google Gemini**, **NVIDIA NIM**, **OpenCode / OpenRouter**, **OpenAI**, **Anthropic**, and local **Ollama** models (with deterministic fallback mode when API keys are omitted for offline lab testing).
- **Modular Agents & Tasks**: Decoupled `BaseAgent` and `BaseTask` classes to quickly compose new roles (SOC Analyst, Detection Engineer, Purple Team Specialist).
- **Lab Server Helpers**: Built-in simple HTTP and mock FTP server commands to simulate network traffic, file downloads, or exfiltration scenarios in VM setups.
- **Jupyter Notebook Integration**: Built-in command to launch Jupyter notebooks exposed across network interfaces for VM testing.

---

## 📁 Repository Structure

```
cyberforge-llm-security-agents/
├── .env.example              # Environment configuration template
├── config.py                 # Configuration manager
├── requirements.txt          # Python dependencies
├── main.py                   # Central CLI application entry point
├── core/                     # Agent & Task framework engine
│   ├── agent.py              # BaseAgent class definition
│   ├── task.py               # BaseTask class definition
│   ├── workflow.py           # Multi-agent workflow orchestrator
│   └── llm_provider.py       # Unified Gemini / NVIDIA / OpenCode / OpenAI / Anthropic connector
├── agents/                   # Pre-defined security agents
│   └── security_agents.py    # Analyst, Detection Engineer, Purple Team agents
├── tasks/                    # Reusable security task modules
│   └── security_tasks.py     # Log triage, Sigma generation, Emulation tasks
├── scenarios/                # Registered lab scenario workflows
│   ├── registry.py           # Central scenario registry
│   ├── hello_agents.py       # Initial verification scenario
│   ├── log_analysis_scenario.py
│   └── purple_team_scenario.py
├── servers/                  # Lab utility servers
│   ├── http_server.py        # Local HTTP server helper
│   └── ftp_server.py         # Mock FTP server helper
└── notebooks/                # VM Jupyter notebook templates
    └── 01_hello_agents.ipynb
```

---

## 🛠️ Setup & Installation

### 1. Prerequisites
- Python 3.10+ installed.
- Git installed.

### 2. Windows Installation Steps
```powershell
# Clone repository
git clone https://github.com/realzoheb/cyberforge-llm-security-agents.git
cd cyberforge-llm-security-agents

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt
```

### 3. Kali Linux (WSL) Setup & Execution
```bash
# Clone repository
git clone https://github.com/realzoheb/cyberforge-llm-security-agents.git
cd cyberforge-llm-security-agents

# Ensure Python venv is installed
sudo apt update && sudo apt install -y python3-venv python3-pip

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Environment Configuration (.env)
Copy `.env.example` to `.env` and set your preferred provider:

```bash
cp .env.example .env
```

#### Provider Configuration Options inside `.env`:

##### Option A: NVIDIA NIM API
```env
DEFAULT_LLM_PROVIDER=nvidia
NVIDIA_API_KEY=your_nvidia_api_key_here
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
NVIDIA_MODEL=meta/llama-3.1-70b-instruct
```

##### Option B: OpenCode / OpenRouter API
```env
DEFAULT_LLM_PROVIDER=opencode
OPENCODE_API_KEY=your_opencode_api_key_here
OPENCODE_BASE_URL=https://openrouter.ai/api/v1
OPENCODE_MODEL=deepseek/deepseek-r1
```

##### Option C: Google Gemini API
```env
DEFAULT_LLM_PROVIDER=google
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

*Note: If no API key is specified, the toolkit automatically runs in **Lab Mock Mode** so you can test scenario wiring offline!*

---

## 💻 Usage & CLI Guide

### 1. List Available Scenarios
```bash
python main.py list
```

### 2. Run Scenarios by Name

#### Hello Agents Demo Scenario
Verify agent setup and connectivity:
```bash
python main.py run hello_agents
```

#### Log Triage & Detection Rule Pipeline
Triage Sysmon process creation logs and generate a Sigma rule:
```bash
python main.py run log_analysis
```

#### Purple Team Emulation Exercise
Plan ATT&CK T1059.001 adversary emulation tests, evaluate telemetry, and build rules:
```bash
python main.py run purple_team
```

---

## 🌐 Lab Server Helpers

### Run HTTP Test Server
Used for serving test files or capturing simulated HTTP requests:
```bash
python main.py serve-http --host 0.0.0.0 --port 8080
```

### Run Mock FTP Server
Used for network traffic simulation or mock file transfers:
```bash
python main.py serve-ftp --host 0.0.0.0 --port 2121
```

---

## 📓 Jupyter Notebook VM Setup

To run notebooks inside a Virtual Machine and access them from your host or lab network:
```bash
python main.py notebook --ip 0.0.0.0 --port 8888
```

---

## ➕ Adding New Scenarios

Adding a custom scenario takes 3 simple steps:

1. **Define your workflow file in `scenarios/my_scenario.py`**:
```python
from core.workflow import Workflow
from agents.security_agents import create_security_analyst
from core.task import BaseTask

def build_my_scenario() -> Workflow:
    analyst = create_security_analyst()
    task = BaseTask(
        name="Custom Lab Task",
        description="Analyze specific network packet metadata.",
        agent=analyst
    )
    return Workflow("My Custom Scenario", "Description here", [task])
```

2. **Register it in `scenarios/__init__.py`**:
```python
from .my_scenario import build_my_scenario

registry.register(
    name="my_scenario",
    description="Analyze custom network telemetry.",
    builder_func=build_my_scenario
)
```

3. **Run your new scenario**:
```bash
python main.py run my_scenario
```

---

## ⚙️ Code Quality & Contribution Standards

- **Type Hints**: Use standard Python `typing` annotations on functions and classes.
- **PEP 8 Formatting**: Keep code readable and PEP 8 compliant.
- **Modular Design**: Keep core logic in `core/`, agents in `agents/`, tasks in `tasks/`, and scenarios in `scenarios/`.
- **Safety First**: Never embed real production keys or run malicious payloads.
