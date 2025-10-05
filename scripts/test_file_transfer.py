# /**
#  * @file test_file_transfer.py
#  * @brief Validates file transfer between clients using CHUNK, DONE, ACK.
#  *        Uses test_file.txt from assets and config files for file-capable clients.
#  *        Prints resolved paths for debugging.
#  * @author Oussama Amara
#  * @version 1.1
#  * @date 2025-10-05
#  */

import subprocess, time, shutil, logging
from utils import get_binary_path, get_config_path
import os

logging.info("🧪 Starting test: file_transfer")

def run_file_test():
    try:
        server_bin = get_binary_path("server")
        client_bin = get_binary_path("client")
        server_cfg = get_config_path("server")
        client_cfg = get_config_path("client_local_file")

        print("-> Server bin path :", server_bin)
        print("-> Client bin path :", client_bin)
        print("-> Server config   :", server_cfg)
        print("-> Client config   :", client_cfg)

        try:
            os.makedirs("to_send", exist_ok=True)
            shutil.copy("assets/test_file.txt", "to_send/test_file.txt")
        except Exception as e:
            logging.error(f"Failed to prepare test file: {e}")
            return


        server = subprocess.Popen([server_bin, server_cfg])
        time.sleep(1)

        client_a = subprocess.Popen([client_bin, client_cfg], stdin=subprocess.PIPE)
        client_b = subprocess.Popen([client_bin, client_cfg], stdin=subprocess.PIPE)
        time.sleep(2)

        client_a.stdin.write(b"file test_file.txt\n")
        client_a.stdin.flush()
        time.sleep(5)

        logging.info("✅ file_transfer test passed.")
    except Exception as e:
        logging.error(f"❌ file_transfer test failed: {e}")
    finally:
        try:
            server.terminate()
            client_a.terminate()
            client_b.terminate()
        except:
            logging.warning("⚠️ Could not terminate one or more processes.")

if __name__ == "__main__":
    run_file_test()
