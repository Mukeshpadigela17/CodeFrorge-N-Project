from agent.orchestrator import count_tests

def test_count_tests():
    assert count_tests("def test_a():\n    pass\n\ndef test_b():\n    pass") == 2
