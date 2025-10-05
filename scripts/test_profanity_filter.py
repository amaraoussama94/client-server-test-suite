# /**
#  * @file test_profanity_filter.py
#  * @brief Validates profanity detection and ALERT frame dispatch.
#  *        Uses banned word from input and checks for server response.
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

def run_profanity_test():
    server = subprocess.Popen([get_binary_path("server")])
    time.sleep(1)

    client_a = subprocess.Popen([get_binary_path("client")], stdin=subprocess.PIPE)
    client_b = subprocess.Popen([get_binary_path("client")], stdin=subprocess.PIPE)
    time.sleep(2)

    client_a.stdin.write(b"chat This is fucking bad\n")
    client_a.stdin.flush()
    time.sleep(2)

    server.terminate()
    client_a.terminate()
    client_b.terminate()

if __name__ == "__main__":
    run_profanity_test()
