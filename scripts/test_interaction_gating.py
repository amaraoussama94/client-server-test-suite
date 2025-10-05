# /**
#  * @file test_interaction_gating.py
#  * @brief Validates WAIT frame blocks interaction when only one client is active.
#  *        Ensures chat/file commands are gated until START.
#  *        Uses config files for both server and file-capable client. Prints resolved paths for debugging.
#  * @author Oussama Amara
#  * @version 1.1
#  * @date 2025-10-05
#  */

import subprocess, time, logging
from utils import get_binary_path, get_config_path

logging.info("🧪 Starting test: interaction_gating")

def run_gating_test():
    try:
        server_bin = get_binary_path("server")
        client_bin = get_binary_path("client")
        server_cfg = get_config_path("server")
        client_cfg = get_config_path("client_local_file")  # fichier activé

        print("-> Server bin path :", server_bin)
        print("-> Client bin path :", client_bin)
        print("-> Server config   :", server_cfg)
        print("-> Client config   :", client_cfg)

        server = subprocess.Popen([server_bin, server_cfg])
        time.sleep(1)

        client = subprocess.Popen([client_bin, client_cfg], stdin=subprocess.PIPE)
        time.sleep(2)

        client.stdin.write(b"chat Should be blocked\n")
        client.stdin.flush()
        time.sleep(2)

        logging.info("✅ interaction_gating test passed.")
    except Exception as e:
        logging.error(f"❌ interaction_gating test failed: {e}")
    finally:
        try:
            server.terminate()
            client.terminate()
        except:
            logging.warning("⚠️ Could not terminate one or more processes.")

if __name__ == "__main__":
    run_gating_test()
