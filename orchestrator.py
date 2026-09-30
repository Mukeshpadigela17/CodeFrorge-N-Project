import re
from agent.nemotron import ask, extract_json
from agent.prompts import PLANNER, GENERATOR, REPAIR
from sandbox.executor import execute_python

def count_tests(text):
    return len(re.findall(r"^\s*def\s+test_", text, flags=re.M))

def run_agent(task, model, max_rounds=3, use_nebius_sandbox=True):
    trace = ["1. Planning task with NVIDIA Nemotron"]
    plan = ask(model, PLANNER, task)
    trace.append("2. Generating implementation and tests with Nemotron")
    generated = extract_json(ask(model, GENERATOR, f"TASK:\n{task}\n\nPLAN:\n{plan}"))
    code, tests_code = generated["code"], generated["tests"]

    last_output, passed, rounds = "", False, 0
    for round_no in range(1, max_rounds + 1):
        rounds = round_no
        trace.append(f"3.{round_no}. Executing tests in {'Nebius ConTree' if use_nebius_sandbox else 'local subprocess'}")
        result = execute_python(code, tests_code, use_nebius_sandbox)
        last_output, passed = result["output"], result["passed"]
        if passed:
            trace.append(f"4.{round_no}. All tests passed.")
            break
        trace.append(f"4.{round_no}. Failure detected; asking Nemotron to diagnose and repair.")
        repaired = extract_json(ask(
            model, REPAIR,
            f"TASK:\n{task}\n\nIMPLEMENTATION:\n{code}\n\nTESTS:\n{tests_code}\n\nEXECUTION OUTPUT:\n{last_output}"
        ))
        code = repaired["code"]

    return {
        "code": code, "tests_code": tests_code, "execution_output": last_output,
        "passed": passed, "rounds": rounds, "tests": count_tests(tests_code),
        "trace": trace,
    }
