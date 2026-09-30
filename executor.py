import base64
import os
import subprocess
import tempfile
from pathlib import Path

def _local_execute(code, tests):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "solution.py").write_text(code, encoding="utf-8")
        (root / "test_solution.py").write_text(
            "from solution import *\n\n" + tests, encoding="utf-8"
        )
        p = subprocess.run(
            ["python", "-m", "pytest", "-q", "test_solution.py"],
            cwd=root, capture_output=True, text=True, timeout=30
        )
        return {"passed": p.returncode == 0,
                "output": (p.stdout + "\n" + p.stderr).strip()}

def _contree_execute(code, tests):
    from contree_sdk import ContreeSync

    token = os.getenv("CONTREE_TOKEN") or os.getenv("NEBIUS_API_KEY")
    if not token:
        raise RuntimeError("Set NEBIUS_API_KEY or CONTREE_TOKEN.")

    kwargs = {"token": token}
    if os.getenv("CONTREE_BASE_URL"):
        kwargs["base_url"] = os.getenv("CONTREE_BASE_URL")

    client = ContreeSync(**kwargs)
    image = client.images.use(os.getenv("CONTREE_IMAGE", "python:3.12-slim"))

    code_b64 = base64.b64encode(code.encode()).decode()
    tests_b64 = base64.b64encode(
        ("from solution import *\n\n" + tests).encode()
    ).decode()

    shell = (
        "mkdir -p /workspace && "
        f"echo {code_b64} | base64 -d > /workspace/solution.py && "
        f"echo {tests_b64} | base64 -d > /workspace/test_solution.py && "
        "cd /workspace && pip install -q pytest && "
        "python -m pytest -q test_solution.py"
    )

    result = image.run(shell=shell).wait()
    output = ((getattr(result, "stdout", "") or "") + "\n" +
              (getattr(result, "stderr", "") or "")).strip()
    return {"passed": getattr(result, "exit_code", 1) == 0, "output": output}

def execute_python(code, tests, use_nebius_sandbox=True):
    if use_nebius_sandbox:
        try:
            return _contree_execute(code, tests)
        except Exception as exc:
            local = _local_execute(code, tests)
            local["output"] = (
                "[Nebius sandbox unavailable; local development fallback]\n"
                f"{type(exc).__name__}: {exc}\n\n{local['output']}"
            )
            return local
    return _local_execute(code, tests)
