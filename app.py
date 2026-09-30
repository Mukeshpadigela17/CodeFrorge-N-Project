import streamlit as st
from agent.orchestrator import run_agent

st.set_page_config(page_title="CodeForge-N", page_icon="⚡", layout="wide")
st.title("⚡ CodeForge-N")
st.caption("Autonomous AI coding, testing, and debugging agent powered by NVIDIA Nemotron on Nebius")

with st.sidebar:
    st.header("Configuration")
    model = st.text_input("Nemotron model", value="nvidia/Nemotron-3_5-Lightning")
    max_rounds = st.slider("Maximum repair rounds", 1, 5, 3)
    use_nebius_sandbox = st.toggle("Use Nebius ConTree sandbox", value=True)
    st.info("Set NEBIUS_API_KEY before using Nebius Token Factory.")

default_task = """Write a Python function named longest_unique_substring(s)
that returns the length of the longest substring without repeating characters.
Include a few edge-case tests."""

task = st.text_area("Coding task", value=default_task, height=180)

if st.button("🚀 Build, Test & Repair", type="primary", use_container_width=True):
    if not task.strip():
        st.warning("Enter a coding task first.")
    else:
        with st.spinner("CodeForge-N is working..."):
            result = run_agent(task, model, max_rounds, use_nebius_sandbox)

        st.subheader("Final solution")
        st.code(result["code"], language="python")
        c1, c2, c3 = st.columns(3)
        c1.metric("Rounds", result["rounds"])
        c2.metric("Tests", result["tests"])
        c3.metric("Status", "PASS" if result["passed"] else "REVIEW")

        st.subheader("Generated tests")
        st.code(result["tests_code"], language="python")
        st.subheader("Execution output")
        st.code(result["execution_output"] or "(no output)")
        st.subheader("Agent trace")
        for item in result["trace"]:
            st.write(item)
