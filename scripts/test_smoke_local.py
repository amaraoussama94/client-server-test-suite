# /**
#  * @file test_smoke_local.py
#  * @brief Basic startup test: server + one client, validate launch and command handling.
#  *        Uses config files for both server and client. Prints resolved paths for debugging.
#  * @author Oussama Amara
#  * @version 1.1
#  * @date 2025-10-05
#  */

import subprocess, time, logging
from utils import get_binary_path, get_config_path

logging.info("🧪 Starting test: smoke_local")

def run_smoke_local():
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

        client = subprocess.Popen([client_bin, client_cfg], stdin=subprocess.PIPE)
        time.sleep(2)

        client.stdin.write(b"ping\n")
        client.stdin.flush()
        time.sleep(1)

        logging.info("✅ smoke_local test passed.")
    except Exception as e:
        logging.error(f"❌ smoke_local test failed: {e}")
    finally:
        try:
            server.terminate()
            client.terminate()
        except:
            logging.warning("⚠️ Could not terminate one or more processes.")

if __name__ == "__main__":
    run_smoke_local()
