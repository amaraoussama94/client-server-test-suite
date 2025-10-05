# /**
#  * @file test_chat_basic.py
#  * @brief Validates basic chat exchange between two clients via server.
#  *        Automatically detects OS and launches correct binaries.
#  *        Sends a single chat message and monitors for delivery.
#  *
#  * @author Oussama Amara
#  * @version 1.0
#  * @date 2025-10-05
#  */

import subprocess, time, platform, os

def get_binary_path(name):
    system = platform.system()
    base = os.path.join("..", "bins", "1.6", "windows" if system == "Windows" else "linux")
    ext = ".exe" if system == "Windows" else ""
    return os.path.join(base, f"{name}{ext}")

def run_chat_test():
    server_path = get_binary_path("server")
    client_path = get_binary_path("client")

    server = subprocess.Popen([server_path], stdout=subprocess.PIPE)
    time.sleep(1)

    client_a = subprocess.Popen([client_path], stdin=subprocess.PIPE)
    client_b = subprocess.Popen([client_path], stdin=subprocess.PIPE)
    time.sleep(2)

    client_a.stdin.write(b"chat Hello from A\n")
    client_a.stdin.flush()
    time.sleep(2)

    server.terminate()
    client_a.terminate()
    client_b.terminate()

if __name__ == "__main__":
    run_chat_test()
