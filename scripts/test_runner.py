# /**
#  * @file test_runner.py
#  * @brief Unified runner for all protocol validation tests.
#  *        Supports local execution and CI automation.
#  * @author Oussama Amara
#  * @version 1.0
#  * @date 2025-10-05
#  */

import importlib, os

TESTS = [
    "test_chat_basic",
    "test_file_transfer",
    "test_profanity_filter",
    "test_multi_client_chat",
    "test_chunked_chat_message",
    "test_file_transfer_progress",
    "test_file_transfer_retry_timeout",
    "test_progress_bar_chunks",
    "test_interaction_gating",
    "test_client_list_broadcast",
    "test_smoke_local",
    "test_smoke_remote"
]

def run_all():
    for test in TESTS:
        print(f"\n🔬 Running {test}...")
        try:
            module = importlib.import_module(test)
            module.__dict__[f"run_{test.replace('test_', '')}"]()
            print(f"✅ {test} passed.")
        except Exception as e:
            print(f"❌ {test} failed: {e}")

if __name__ == "__main__":
    run_all()
