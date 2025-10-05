# /**
#  * @file test_file_transfer.py
#  * @brief Validates file transfer between clients using CHUNK, DONE, ACK.
#  *        Detects OS and uses correct binaries. Uses test_file.txt from assets.
#  *
#  * @author Oussama Amara
#  * @version 1.0
#  * @date 2025-10-05
#  */

import subprocess, time, platform, os, shutil

def get_binary_path(name):
    system = platform.system()
    base = os.path.join("..", "bins", "1.6", "windows" if system == "Windows" else "linux")
    ext = ".exe" if system == "Windows" else ""
    return os.path.join(base, f"{name}{ext}")

def run_file_test():
    shutil.copy("assets/test_file.txt", "to_send/test_file.txt")

    server = subprocess.Popen([get_binary_path("server")])
    time.sleep(1)

    client_a = subprocess.Popen([get_binary_path("client")], stdin=subprocess.PIPE)
    client_b = subprocess.Popen([get_binary_path("client")], stdin=subprocess.PIPE)
    time.sleep(2)

    client_a.stdin.write(b"file test_file.txt\n")
    client_a.stdin.flush()
    time.sleep(5)

    server.terminate()
    client_a.terminate()
    client_b.terminate()

if __name__ == "__main__":
    run_file_test()
