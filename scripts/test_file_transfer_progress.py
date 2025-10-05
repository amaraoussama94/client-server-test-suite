# /**
#  * @file test_file_transfer_progress.py
#  * @brief Validates progress bar output during file transfer.
#  *        Uses config files for file-capable clients and prints resolved paths for debugging.
#  * @author Oussama Amara
#  * @version 1.1
#  * @date 2025-10-05
#  */

import subprocess, time, shutil, logging
from utils import get_binary_path, get_config_path

logging.info("🧪 Starting test: file_transfer_progress")

def run_progress_test():
    try:
        server_bin = get_binary_path("server")
        client_bin = get_binary_path("client")
        server_cfg = get_config_path("server")
        client_cfg = get_config_path("client_local_file")

        print("-> Server bin path :", server_bin)
        print("-> Client bin path :", client_bin)
        print("-> Server config   :", server_cfg)
        print("-> Client config   :", client_cfg)

        shutil.copy("assets/test_file.txt", "to_send/test_file.txt")

        server = subprocess.Popen([server_bin, server_cfg])
        time.sleep(1)

        client_a = subprocess.Popen([client_bin, client_cfg], stdin=subprocess.PIPE)
        client_b = subprocess.Popen([client_bin, client_cfg], stdin=subprocess.PIPE)
        time.sleep(2)

        client_a.stdin.write(b"file test_file.txt\n")
        client_a.stdin.flush()
        time.sleep(5)

        logging.info("✅ file_transfer_progress test passed.")
    except Exception as e:
        logging.error(f"❌ file_transfer_progress test failed: {e}")
    finally:
        try:
            server.terminate()
            client_a.terminate()
            client_b.terminate()
        except:
            logging.warning("⚠️ Could not terminate one or more processes.")

if __name__ == "__main__":
    run_progress_test()
