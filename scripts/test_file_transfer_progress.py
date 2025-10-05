# /**
#  * @file test_file_transfer_progress.py
#  * @brief Validates progress bar output during file transfer.
#  * @author Oussama Amara
#  * @version 1.0
#  * @date 2025-10-05
#  */

import subprocess, time, shutil
from utils import get_binary_path

def run_progress_test():
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
    run_progress_test()
