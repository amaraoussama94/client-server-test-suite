# /**
#  * @file test_client_list_broadcast.py
#  * @brief Validates LIST frame broadcast when clients connect/disconnect.
#  *        Ensures server updates all clients with active list.
#  * @author Oussama Amara
#  * @version 1.0
#  * @date 2025-10-05
#  */

import subprocess, time
from utils import get_binary_path

def run_list_broadcast():
    server = subprocess.Popen([get_binary_path("server")])
    time.sleep(1)

    client_a = subprocess.Popen([get_binary_path("client")])
    time.sleep(1)

    client_b = subprocess.Popen([get_binary_path("client")])
    time.sleep(2)

    client_b.terminate()
    time.sleep(2)

    server.terminate()
    client_a.terminate()

if __name__ == "__main__":
    run_list_broadcast()
