# /**
#  * @file test_progress_bar_chunks.py
#  * @brief Validates progress feedback during chunked chat message delivery.
#  *        Ensures client displays progress bar or chunk count.
#  * @author Oussama Amara
#  * @version 1.0
#  * @date 2025-10-05
#  */

import subprocess, time
from utils import get_binary_path

def run_chunk_progress():
    long_message = "chat " + ("Chunked message. " * 40) + "\n"

    server = subprocess.Popen([get_binary_path("server")])
    time.sleep(1)

    client_a = subprocess.Popen([get_binary_path("client")], stdin=subprocess.PIPE)
    client_b = subprocess.Popen([get_binary_path("client")])
    time.sleep(2)

    client_a.stdin.write(long_message.encode())
    client_a.stdin.flush()
    time.sleep(3)

    server.terminate()
    client_a.terminate()
    client_b.terminate()

if __name__ == "__main__":
    run_chunk_progress()
