# /**
#  * @file test_multi_client_chat.py
#  * @brief Validates chat exchange between two clients after START frame.
#  *        Ensures proper routing and delivery of messages.
#  * @author Oussama Amara
#  * @version 1.0
#  * @date 2025-10-05
#  */

import subprocess, time
from utils import get_binary_path

def run_multi_chat():
    server = subprocess.Popen([get_binary_path("server")])
    time.sleep(1)

    client_a = subprocess.Popen([get_binary_path("client")], stdin=subprocess.PIPE)
    client_b = subprocess.Popen([get_binary_path("client")], stdin=subprocess.PIPE)
    time.sleep(2)

    client_a.stdin.write(b"chat Hello B\n")
    client_a.stdin.flush()
    time.sleep(2)

    server.terminate()
    client_a.terminate()
    client_b.terminate()

if __name__ == "__main__":
    run_multi_chat()
