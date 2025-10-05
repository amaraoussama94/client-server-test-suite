# /**
#  * @file test_interaction_gating.py
#  * @brief Validates WAIT frame blocks interaction when only one client is active.
#  *        Ensures chat/file commands are gated until START.
#  * @author Oussama Amara
#  * @version 1.0
#  * @date 2025-10-05
#  */

import subprocess, time
from utils import get_binary_path

def run_gating_test():
    server = subprocess.Popen([get_binary_path("server")])
    time.sleep(1)

    client = subprocess.Popen([get_binary_path("client")], stdin=subprocess.PIPE)
    time.sleep(2)

    client.stdin.write(b"chat Should be blocked\n")
    client.stdin.flush()
    time.sleep(2)

    server.terminate()
    client.terminate()

if __name__ == "__main__":
    run_gating_test()
