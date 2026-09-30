# ⚡ CodeForge-N

**Autonomous AI coding, testing, and debugging agent powered by NVIDIA Nemotron on Nebius.**

## Hackathon track
**Coding and Agentic Engineering Track**

## What it does
CodeForge-N turns a coding request into:

**Plan → Generate → Test → Execute → Diagnose → Repair → Verify**

It uses **NVIDIA Nemotron through Nebius Token Factory** for runtime inference and **Nebius ConTree** for isolated execution of generated code.

## Features
- AI coding-task understanding
- Code generation
- Automatic pytest generation
- Nebius sandbox execution
- Failure detection
- AI-assisted repair
- Iterative re-testing
- Execution trace
- Local development fallback

## Setup

### 1. Clone
```bash
git clone https://github.com/YOUR_USERNAME/codeforge-n.git
cd codeforge-n
```

### 2. Install
```bash
python -m venv .venv
```

Windows:
```powershell
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

### 3. Configure
Copy `.env.example` to `.env` and set:
```text
NEBIUS_API_KEY=your_key_here
NEBIUS_BASE_URL=https://api.tokenfactory.nebius.com/v1/
```

Never commit `.env`.

### 4. Run
```bash
streamlit run app.py
```

## Model
Default:
```text
nvidia/Nemotron-3_5-Lightning
```

Change it in the sidebar if another Nemotron model is available to your account.

## Nebius sandbox
Enable **Use Nebius ConTree sandbox** in the UI. The agent uses ConTree to run generated Python and pytest in an isolated environment.

If your account requires an explicit sandbox endpoint:
```text
CONTREE_BASE_URL=https://api.tokenfactory.nebius.com/sandboxes
CONTREE_TOKEN=your_nebius_api_key
```

For local development, if the sandbox is unavailable, the app falls back to a temporary local subprocess. For the hackathon demo, keep sandbox mode ON and verify the trace shows Nebius/ConTree execution.

## Architecture
```text
User
  ↓
Streamlit UI
  ↓
Agent Orchestrator
  ├──→ Nebius Token Factory → NVIDIA Nemotron
  ↓
Generated Code + Tests
  ↓
Nebius ConTree Sandbox
  ├── PASS → Verified Solution
  └── FAIL → Error Feedback → Nemotron Repair → Re-test
```

## Security
Generated code is untrusted. Use Nebius ConTree for the hackathon demonstration. The local fallback is only for development and is not a production security boundary.

## Demo prompt
```text
Write a Python function named longest_unique_substring(s)
that returns the length of the longest substring without repeating characters.
Include edge-case tests.
```

## License
MIT. See `LICENSE`.

## Hackathon disclosure
Describe any material updates made during the hackathon submission period in the final Devpost submission.
