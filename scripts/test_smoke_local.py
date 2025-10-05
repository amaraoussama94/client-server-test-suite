# /**
#  * @file test_smoke_local.py
#  * @brief Basic startup test: server + one client, validate launch and command handling.
#  *        No delivery or interaction required.
#  * @author Oussama Amara
#  * @version 1.0
#  * @date 2025-10-05
#  */

import subprocess, time
from utils import get_binary_path

def run_smoke_local():
    server = subprocess.Popen([get_binary_path("server")])
    time.sleep(1)

    client = subprocess.Popen([get_binary_path("client")], stdin=subprocess.PIPE)
    time.sleep(2)

    client.stdin.write(b"ping\n")
    client.stdin.flush()
    time.sleep(1)

    server.terminate()
    client.terminate()

if __name__ == "__main__":
    run_smoke_local()
