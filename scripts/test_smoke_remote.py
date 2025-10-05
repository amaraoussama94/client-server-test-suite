# /**
#  * @file test_smoke_remote.py
#  * @brief Validates remote startup: server on local, client connects via remote IP.
#  *        Uses client_remote.cfg for connection parameters.
#  * @author Oussama Amara
#  * @version 1.0
#  * @date 2025-10-05
#  */

import subprocess, time
from utils import get_binary_path

def run_smoke_remote():
    server = subprocess.Popen([get_binary_path("server")])
    time.sleep(1)

    client = subprocess.Popen([get_binary_path("client"), "--config", "configs/client_remote.cfg"], stdin=subprocess.PIPE)
    time.sleep(2)

    client.stdin.write(b"ping\n")
    client.stdin.flush()
    time.sleep(1)

    server.terminate()
    client.terminate()

if __name__ == "__main__":
    run_smoke_remote()
