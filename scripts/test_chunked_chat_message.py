# /**
#  * @file test_chunked_chat_message.py
#  * @brief Sends a long chat message to validate chunking and reassembly.
#  * @author Oussama Amara
#  * @version 1.0
#  * @date 2025-10-05
#  */

import subprocess, time
from utils import get_binary_path

def run_chunked_chat():
    long_message = "chat " + ("This is a long message. " * 50) + "\n"

    server = subprocess.Popen([get_binary_path("server")])
    time.sleep(1)

    client_a = subprocess.Popen([get_binary_path("client")], stdin=subprocess.PIPE)
    client_b = subprocess.Popen([get_binary_path("client")], stdin=subprocess.PIPE)
    time.sleep(2)

    client_a.stdin.write(long_message.encode())
    client_a.stdin.flush()
    time.sleep(3)

    server.terminate()
    client_a.terminate()
    client_b.terminate()

if __name__ == "__main__":
    run_chunked_chat()
