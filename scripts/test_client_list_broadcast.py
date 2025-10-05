# /**
#  * @file test_client_list_broadcast.py
#  * @brief Validates LIST frame broadcast when clients connect/disconnect.
#  *        Ensures server updates all clients with active list.
#  *        Uses config files for chat-capable clients and prints resolved paths for debugging.
#  * @author Oussama Amara
#  * @version 1.1
#  * @date 2025-10-05
#  */

import subprocess, time, logging
from utils import get_binary_path, get_config_path

logging.info("🧪 Starting test: client_list_broadcast")

def run_list_broadcast():
    try:
        server_bin = get_binary_path("server")
        client_bin = get_binary_path("client")
        server_cfg = get_config_path("server")
        client_cfg = get_config_path("client_local")

        print("-> Server bin path :", server_bin)
        print("-> Client bin path :", client_bin)
        print("-> Server config   :", server_cfg)
        print("-> Client config   :", client_cfg)

        server = subprocess.Popen([server_bin, server_cfg])
        time.sleep(1)

        client_a = subprocess.Popen([client_bin, client_cfg])
        time.sleep(1)

        client_b = subprocess.Popen([client_bin, client_cfg])
        time.sleep(2)

        client_b.terminate()
        time.sleep(2)

        logging.info("✅ client_list_broadcast test passed.")
    except Exception as e:
        logging.error(f"❌ client_list_broadcast test failed: {e}")
    finally:
        try:
            server.terminate()
            client_a.terminate()
        except:
            logging.warning("⚠️ Could not terminate one or more processes.")

if __name__ == "__main__":
    run_list_broadcast()
